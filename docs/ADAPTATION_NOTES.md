# PaySim to CreditTransAct adaptation notes

The supplied repository's ETL pattern (ingestion, transformation, aggregation and Hive/Parquet warehouse layers) is retained conceptually. PaySim-specific field assumptions are intentionally removed. CreditTransAct's exact schema must be inspected using `00_inspect_schema.py` before configuring the label, profile, timestamp, transaction type and amount columns.

The new implementation adds:
- schema discovery and sample-value inspection;
- generic Parquet ingestion and conservative cleaning;
- configurable heuristic risk score with reason codes;
- Spark MLlib model comparison (Logistic Regression, Decision Tree, Random Forest, GBT and Linear SVM);
- precision, recall, F1, ROC-AUC and confusion matrix counts;
- charts generated from measured execution results.

No CreditTransAct data file was supplied with the source-code ZIP in this conversation. Place the official dataset in `data/` after downloading it. No results are pre-populated or fabricated.
