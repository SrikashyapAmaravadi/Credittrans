from pyspark.sql import functions as F
from common import config, spark, output_path
cfg = config(); sp = spark('CreditTransAct-Transformation')
df = sp.read.parquet(output_path(cfg, 'raw'))
# Conservative generic cleaning: trim string values, preserve original columns and meanings.
for field in df.schema.fields:
    if field.dataType.simpleString() == 'string':
        df = df.withColumn(field.name, F.trim(F.col(field.name)))
# Remove fully duplicate records; do not silently drop columns or impute target labels.
df = df.dropDuplicates()
label = cfg.get('label_column', '').strip()
if label and label not in df.columns:
    raise ValueError(f"Configured label_column '{label}' not found. Available: {df.columns}")
if label:
    df = df.filter(F.col(label).isNotNull())
df.write.mode('overwrite').parquet(output_path(cfg, 'cleaned'))
print('Cleaned rows:', df.count(), 'columns:', len(df.columns))
print('Cleaned layer:', output_path(cfg, 'cleaned'))
sp.stop()
