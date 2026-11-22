-- Optional Hive starter. Replace the location and columns with the verified dataset schema.
-- Do not execute this template unchanged: CreditTransAct column names/types must be confirmed first.
CREATE DATABASE IF NOT EXISTS credittransact;
-- Example external table pattern:
-- CREATE EXTERNAL TABLE credittransact.raw_transactions (...)
-- STORED AS PARQUET LOCATION 'hdfs:///fraud-project/raw/';
