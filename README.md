# CreditTransAct Financial Fraud Analytics (CSV edition)

Adaptation of the supplied PaySim data-warehouse project for the CreditTransAct dataset. This project reads **CSV** input with PySpark and writes intermediate/final analytical data as Parquet for efficient processing. The actual CreditTransAct dataset is not bundled: it was not supplied in this conversation and is approximately 4.67 GB in CSV form.

## Stack
- Python + PySpark (Spark SQL and Spark MLlib)
- Optional HDFS input/output when Hadoop client configuration is available
- CSV input; Parquet intermediate outputs
- pandas + matplotlib for evaluation tables and charts

## 1. Place the dataset
Create a `data` directory in the project root and place the downloaded CSV there. The default expected path is:

```text
data/CreditTransAct.csv
```

If the downloaded filename differs, either rename it to `CreditTransAct.csv` or edit `input_path` in `config/project_config.json`.

## 2. Install and inspect
Use a Python version supported by your Spark installation (Python 3.10/3.11 is a practical choice for Spark 3.5.x). Install Java compatible with Spark, then:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python pipeline/00_inspect_schema.py
```

The first schema inspection reads the CSV and may take time for a multi-GB file because `inferSchema=true` scans data. Inspect `results/schema_report.json` and set the exact `label_column`, `positive_label`, and optional profile/time/transaction/amount columns in `config/project_config.json`. Do not guess these fields. Exclude transaction IDs, customer IDs, post-outcome fields and any other leakage columns in `exclude_columns`.

## 3. Run the pipeline
After configuring the true dataset column names and label values, run:

```powershell
python pipeline/01_ingest.py
python pipeline/02_transform.py
python pipeline/03_risk_analysis.py
python pipeline/04_train_models.py
python pipeline/05_evaluate.py
```

The ingestion step reads CSV and writes a raw Parquet copy. Subsequent stages read the Parquet intermediate data. This avoids repeatedly parsing the large CSV.

## 4. CSV settings
Default settings in `config/project_config.json` are:
- `header=true`
- `inferSchema=true`
- `mode=PERMISSIVE`
- quote and escape character: `"`

Change `csv_options` only if the dataset's actual CSV format requires it. For a multi-file dataset, `input_path` can point to a directory containing CSV part files, provided they share a compatible schema.

## 5. HDFS usage
For HDFS input, set `input_path` to an HDFS URI such as `hdfs:///fraud-project/raw/CreditTransAct.csv`. Ensure Spark has the Hadoop configuration and permissions to access the cluster. For HDFS outputs, set `output_base` to an HDFS URI. Local Windows Spark does not automatically gain access to a remote Cloudera HDFS cluster; configure the Hadoop client or run the pipeline within the cluster environment.

## 6. Project files
- `pipeline/00_inspect_schema.py`: inspect columns, data types, counts and sample values
- `pipeline/01_ingest.py`: load CSV and write raw Parquet
- `pipeline/02_transform.py`: basic validation, null handling and feature assembly
- `pipeline/03_risk_analysis.py`: configurable heuristic risk score and reason codes
- `pipeline/04_train_models.py`: Logistic Regression, Decision Tree, Random Forest, GBT and Linear SVM where supported by the installed Spark version
- `pipeline/05_evaluate.py`: metrics, confusion matrices and visualizations
- `sql/`: optional Hive external-table starter DDL

## Important limitations and validation
- The exact CreditTransAct column names and fraud-label values must be confirmed by running schema inspection. Configure them before training.
- The project ZIP does not contain the dataset. Download it separately from https://data.mendeley.com/datasets/y64bbnm2s3/1.
- The rule-based risk score is a transparent heuristic, not a calibrated fraud probability.
- Check the feature list for target leakage before accepting model metrics. A random train/test split is a baseline; use a chronological split if a valid timestamp is available and appropriate.
- Some Spark ML algorithms may be unavailable or behave differently on older Spark versions. Verify `spark-submit --version` and `pyspark --version`.
- Do not report metrics until the pipeline has actually run successfully on CreditTransAct. No results are pre-filled or fabricated.
