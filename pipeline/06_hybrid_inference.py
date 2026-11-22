import time
from pathlib import Path
import pandas as pd
from pyspark.sql import functions as F
from common import ROOT, config, spark, output_path

cfg = config()
sp = spark('CreditTransAct-Hybrid-Triage')

print("Loading test predictions and risk intelligence layers...")
pred_path = ROOT / 'results' / 'predictions' / 'LogisticRegression'
if not pred_path.exists():
    raise FileNotFoundError("Run 04_train_models.py first.")

# Read predictions
pred_df = sp.read.parquet(str(pred_path))

# Read risk scored dataset
risk_df = sp.read.parquet(output_path(cfg, 'risk_scored'))

# Sample or align risk dataframe with the test partition
sample_fraction = float(cfg.get('sample_fraction', 0.1))
seed = int(cfg.get('seed', 42))

# We can evaluate triage logic on the predictions partition
# Define hybrid decision matrix
# Probability of fraud (if available) or raw prediction
if 'probability' in pred_df.columns:
    # vector column probability: index 1 is p(fraud)
    from pyspark.ml.functions import vector_to_array
    pred_df = pred_df.withColumn('prob_fraud', vector_to_array('probability')[1])
else:
    pred_df = pred_df.withColumn('prob_fraud', F.when(F.col('prediction') == 1.0, 1.0).otherwise(0.0))

# Quantile heuristic risk proxy for the test partition based on probability thresholds
triage_df = pred_df.withColumn(
    'triage_action',
    F.when((F.col('prediction') == 1.0) & (F.col('prob_fraud') >= 0.85), 'TIER_1_CRITICAL_BLOCK')
     .when((F.col('prediction') == 1.0) & (F.col('prob_fraud') < 0.85), 'TIER_2_STEP_UP_AUTH')
     .when((F.col('prediction') == 0.0) & (F.col('prob_fraud') >= 0.20), 'TIER_3_COMPLIANCE_AUDIT')
     .otherwise('TIER_4_AUTOMATED_CLEARANCE')
)

triage_summary = triage_df.groupBy('triage_action', 'label').count().toPandas()

# Format summary table
print("\n============================================================")
print("HYBRID FRAUD TRIAGE & DECISION ENGINE SUMMARY")
print("============================================================")
print(triage_summary.to_string(index=False))

out_csv = ROOT / 'results' / 'hybrid_triage_summary.csv'
triage_summary.to_csv(out_csv, index=False)
print(f"\nHybrid triage summary saved to: {out_csv}")

# Action volume summary
action_vol = triage_df.groupBy('triage_action').count().orderBy('count', ascending=False).toPandas()
action_vol['percentage'] = (action_vol['count'] / action_vol['count'].sum()) * 100
action_vol.to_csv(ROOT / 'results' / 'hybrid_action_volumes.csv', index=False)
print("\nTriage Action Volume Breakdown:")
print(action_vol.to_string(index=False))

sp.stop()
