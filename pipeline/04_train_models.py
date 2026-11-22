import time
from pathlib import Path
import pandas as pd
from pyspark.sql import functions as F
from pyspark.sql.types import NumericType
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.classification import (
    LogisticRegression,
    DecisionTreeClassifier,
    RandomForestClassifier,
    GBTClassifier,
    LinearSVC
)
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from common import ROOT, config, spark, output_path

cfg = config()
sp = spark('CreditTransAct-Model-Training')

label = cfg.get('label_column', '').strip()
if not label:
    raise ValueError('Set label_column in config/project_config.json after inspecting the dataset schema.')

df = sp.read.parquet(output_path(cfg, 'cleaned'))
if label not in df.columns:
    raise ValueError(f'Label column {label} not found.')

positive = str(cfg.get('positive_label', '1'))
negative = str(cfg.get('negative_label', '0'))

# Normalize label values explicitly
label_str = F.col(label).cast('string')
df = (df.withColumn('label', F.when(label_str == positive, 1.0)
                            .when(label_str == negative, 0.0)
                            .otherwise(None))
        .filter(F.col('label').isNotNull()))

# Optional representative sample for scalable training
sample_fraction = float(cfg.get('sample_fraction', 1.0))
if sample_fraction < 1.0:
    print(f"Applying sample_fraction={sample_fraction} on dataset...")
    df = df.sample(withReplacement=False, fraction=sample_fraction, seed=int(cfg.get('seed', 42)))

exclude = set(cfg.get('exclude_columns', [])) | {label, 'label'}
for optional in ['timestamp_column']:
    v = cfg.get(optional, '').strip()
    if v:
        exclude.add(v)

feature_cols = [c for c in df.columns if c not in exclude]
if not feature_cols:
    raise ValueError('No predictors remain. Review exclude_columns and dataset schema.')

# Numeric predictors are retained; categorical predictors are indexed + one-hot encoded
numeric = []
categorical = []
for field in df.schema.fields:
    if field.name in feature_cols:
        if isinstance(field.dataType, NumericType):
            numeric.append(field.name)
        else:
            categorical.append(field.name)

print(f"Features: {len(numeric)} numeric, {len(categorical)} categorical")

max_cat = int(cfg.get('max_categories', 100))
# Efficient cardinality check using an initial sample
card_sample = df.limit(50000).cache()
indexers = []
indexed = []
enc_inputs = []
for c in categorical:
    distinct_sample = card_sample.select(c).distinct().count()
    if distinct_sample <= max_cat:
        ix = f'idx_{len(indexed)}'
        indexers.append(StringIndexer(inputCol=c, outputCol=ix, handleInvalid='keep'))
        indexed.append(ix)
        enc_inputs.append(ix)

card_sample.unpersist()

encoders = []
encoded = []
if enc_inputs:
    encoders = [OneHotEncoder(inputCols=enc_inputs,
                              outputCols=[f'ohe_{i}' for i in range(len(enc_inputs))],
                              handleInvalid='keep')]
    encoded = [f'ohe_{i}' for i in range(len(enc_inputs))]

if not numeric and not encoded:
    raise ValueError('No usable numeric/categorical predictors. Review schema and config.')

assembler = VectorAssembler(inputCols=numeric + encoded, outputCol='features', handleInvalid='keep')

# Split data
train_ratio = float(cfg.get('train_ratio', 0.8))
seed = int(cfg.get('seed', 42))
train, test = df.randomSplit([train_ratio, 1.0 - train_ratio], seed=seed)

# Build and fit feature pipeline once across the training partition
print("Fitting feature transformation pipeline (StringIndexers, OneHotEncoder, VectorAssembler)...")
t_feat = time.time()
feat_pipe = Pipeline(stages=indexers + encoders + [assembler])
feat_model = feat_pipe.fit(train)

# Transform train and test partitions and cache them
train_vec = feat_model.transform(train).select('label', 'features').cache()
test_vec = feat_model.transform(test).select('label', 'features').cache()

n_train = train_vec.count()
n_test = test_vec.count()
print(f"Feature transformation complete in {time.time()-t_feat:.2f}s (Train: {n_train}, Test: {n_test})")

models = [
    ('LogisticRegression', LogisticRegression(labelCol='label', featuresCol='features', maxIter=50)),
    ('DecisionTree', DecisionTreeClassifier(labelCol='label', featuresCol='features', maxDepth=8)),
    ('RandomForest', RandomForestClassifier(labelCol='label', featuresCol='features', numTrees=50, maxDepth=8, seed=seed)),
    ('GBT', GBTClassifier(labelCol='label', featuresCol='features', maxIter=30, maxDepth=5, seed=seed)),
    ('LinearSVM', LinearSVC(labelCol='label', featuresCol='features', maxIter=50))
]

metrics = []
pred_dir = ROOT / 'results' / 'predictions'
pred_dir.mkdir(parents=True, exist_ok=True)
models_dir = ROOT / 'results' / 'models'
models_dir.mkdir(parents=True, exist_ok=True)

for name, clf in models:
    print(f"\n--- Training {name} ---")
    t0 = time.time()
    try:
        clf_model = clf.fit(train_vec)
        pred = clf_model.transform(test_vec)

        # Materialize predictions to parquet
        keep_cols = ['label', 'prediction', 'rawPrediction'] + (['probability'] if 'probability' in pred.columns else [])
        pred_subset = pred.select(*keep_cols)
        pred_subset.write.mode('overwrite').parquet(str(pred_dir / name))

        # Single-pass confusion matrix computation
        cm_counts = pred.groupBy('label', 'prediction').count().collect()
        cm = {(int(r['label']), int(r['prediction'])): int(r['count']) for r in cm_counts}
        tp = cm.get((1, 1), 0)
        fp = cm.get((0, 1), 0)
        fn = cm.get((1, 0), 0)
        tn = cm.get((0, 0), 0)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

        evaluator = BinaryClassificationEvaluator(labelCol='label', rawPredictionCol='rawPrediction', metricName='areaUnderROC')
        auc = evaluator.evaluate(pred)

        metrics.append({
            'model': name,
            'precision': round(precision, 6),
            'recall': round(recall, 6),
            'f1': round(f1, 6),
            'roc_auc': round(auc, 6),
            'tp': tp,
            'fp': fp,
            'fn': fn,
            'tn': tn,
            'status': 'OK'
        })

        # Save end-to-end PipelineModel
        fitted_pipe = PipelineModel(stages=feat_model.stages + [clf_model])
        fitted_pipe.write().overwrite().save(str(models_dir / name))

        print(f"[{name}] Done in {time.time()-t0:.2f}s | Precision: {precision:.4f} | Recall: {recall:.4f} | F1: {f1:.4f} | ROC-AUC: {auc:.4f}")
        print(f"Confusion Matrix: TP={tp}, FP={fp}, FN={fn}, TN={tn}")

    except Exception as e:
        metrics.append({'model': name, 'status': 'FAILED', 'error': str(e)[:500]})
        print(f"Model failed: {name} - {e}")

# Save metrics CSV
out_metrics = ROOT / 'results' / 'model_metrics.csv'
pd.DataFrame(metrics).to_csv(out_metrics, index=False)
print(f"\nModel training metrics saved to: {out_metrics}")

train_vec.unpersist()
test_vec.unpersist()
sp.stop()
