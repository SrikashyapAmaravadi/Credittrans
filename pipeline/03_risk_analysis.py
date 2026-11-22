from pyspark.sql import functions as F
from common import config, spark, output_path
cfg = config(); sp = spark('CreditTransAct-Risk-Analysis')
df = sp.read.parquet(output_path(cfg, 'cleaned'))
amount = cfg.get('amount_column', '').strip()
profile = cfg.get('profile_column', '').strip()
# Explainable baseline score. Only uses amount/profile if explicitly configured and present.
score = F.lit(10.0); reasons = F.array(F.lit('BASELINE_REVIEW'))
if amount and amount in df.columns:
    # Relative amount percentile threshold is computed from the observed dataset, not hard-coded currency limits.
    q = df.approxQuantile(amount, [0.90], 0.01)
    if q:
        score = score + F.when(F.col(amount).cast('double') >= F.lit(q[0]), 30.0).otherwise(0.0)
        reasons = F.when(F.col(amount).cast('double') >= F.lit(q[0]), F.array(F.lit('AMOUNT_TOP_DECILE'))).otherwise(reasons)
if profile and profile in df.columns:
    counts = df.groupBy(profile).count()
    total = df.count()
    rates = counts.withColumn('profile_share', F.col('count') / F.lit(max(total, 1)))
    rare = [r[profile] for r in rates.filter(F.col('profile_share') < 0.05).select(profile).collect()]
    if rare:
        score = score + F.when(F.col(profile).isin(rare), 20.0).otherwise(0.0)
        reasons = F.when(F.col(profile).isin(rare), F.concat(reasons, F.array(F.lit('RARE_PROFILE')))).otherwise(reasons)
scored = (df.withColumn('risk_score', F.least(F.lit(100.0), score))
          .withColumn('risk_category', F.when(F.col('risk_score') >= 70, 'HIGH').when(F.col('risk_score') >= 35, 'MEDIUM').otherwise('LOW'))
          .withColumn('risk_reason_codes', reasons))
scored.write.mode('overwrite').parquet(output_path(cfg, 'risk_scored'))
scored.groupBy('risk_category').count().orderBy('risk_category').toPandas().to_csv('results/risk_category_summary.csv', index=False)
print('Risk-scored output:', output_path(cfg, 'risk_scored'))
sp.stop()
