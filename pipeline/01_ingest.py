from common import config, spark, read_source, output_path
cfg = config(); sp = spark('CreditTransAct-Ingestion')
df = read_source(sp, cfg)
print('Input rows:', df.count(), 'columns:', len(df.columns))
df.write.mode('overwrite').parquet(output_path(cfg, 'raw'))
print('Raw layer written to', output_path(cfg, 'raw'))
sp.stop()
