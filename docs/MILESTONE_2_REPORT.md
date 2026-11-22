# BENNETT UNIVERSITY
## SCHOOL OF COMPUTER SCIENCE ENGINEERING

### PROJECT IMPLEMENTATION REPORT — MILESTONE 2

**SCALABLE FINANCIAL FRAUD DETECTION AND RISK INTELLIGENCE USING APACHE SPARK, HADOOP AND MACHINE LEARNING**

- **Course Code**: CSET371 — Big Data Analytics and Business Intelligence
- **Project Guide**: Dr. Aditya Bharadwaj
- **Academic Year**: 2026

**Submitted by:**
- Srikashyap Amaravadi (S24CSEU1423)
- Gitesh Goyal (S24CSEU0774)
- Annya Sharma (S24CSEU1408)
- Ajitej Singh (S24CSEU1413)

---

## ABSTRACT
Financial fraud poses an escalating threat to digital banking infrastructures due to immense transaction volumes, rapid velocity, and subtle fraudulent signatures concealed within legitimate consumer activity. Traditional single-machine analytics and manual auditing mechanisms fail to scale to multi-gigabyte transaction streams. This report documents the successful implementation of Milestone 2 for a distributed, profile-driven fraud analytics architecture built on **Apache Spark 3.5.4**, **Hadoop 3.3.5**, and **Python 3.11**.

The workflow is empirically validated on the full **CreditTransAct** benchmark dataset (`credit_card_fraud.csv`), comprising **15,000,000 transaction records across 34 feature attributes** (~5.01 GB uncompressed CSV). In Milestone 2, the team engineered and executed:
1. Automated schema discovery and distributed data profiling across 38 parallel Spark partitions;
2. Scalable ingestion converting raw CSV into Snappy-compressed columnar Parquet format (`results/raw`);
3. Conservative data hygiene and deduplication (`results/cleaned`);
4. Explainable rule-based risk intelligence computing empirical percentile thresholds and category frequency shares (`results/risk_scored` and `results/risk_category_summary.csv`).

All numerical statistics, schema definitions, and risk distributions presented in this report represent verified empirical results generated on the active system.

---

## TABLE OF CONTENTS
1. Introduction
2. Problem Statement and Objectives
3. Dataset Description and Verified Schema
4. System Requirements and Architecture
5. Development Environment and Verified Stack
6. Data Ingestion and Distributed Storage Pipeline
7. Data Understanding and Quality Assessment
8. Data Preprocessing and Transformation Layer
9. Fraud Detection Algorithms (Planned for Milestone 3)
10. Risk Scoring Intelligence and Explainability
11. Model Training and Validation Strategy
12. Evaluation Metrics Framework
13. Implementation Workflow and Execution Status
14. Measured Results, Risk Distribution and Reporting
15. Testing, Limitations and Risk Management
16. Team Contributions and Project Management
17. Conclusion and Future Roadmap
18. References

---

## 1. INTRODUCTION
Digital financial networks process millions of payment events per hour. While fraudulent events constitute a minority fraction of total traffic, their financial and reputational ramifications are disproportionately severe. The challenges of fraud detection are threefold:
- **Massive Data Scale**: Ingestion and analytical pipelines must process millions of records without memory exhaustion.
- **Extreme Class Imbalance**: Genuine transactions drastically outnumber fraudulent attempts.
- **Operational Interpretability**: Financial compliance standards require that flagged transactions be accompanied by transparent, auditable reason codes rather than opaque black-box verdicts.

Milestone 2 establishes the high-performance Big Data foundational pipeline. Utilizing Apache Spark SQL and Hadoop file-system abstractions, the project ingests, validates, cleans, and scores 15 million credit card transactions, establishing intermediate Parquet layers and generating heuristic risk intelligence.

---

## 2. PROBLEM STATEMENT AND OBJECTIVES

### 2.1 Problem Statement
Modern financial institutions require scalable, automated systems capable of ingesting high-velocity transaction streams, assessing data quality, isolating risk indicators, and prioritizing suspicious activity for human investigators without introducing prohibitive computational latencies or high false-positive rates.

### 2.2 Objectives Completed in Milestone 2
1. **Infrastructure Configuration**: Deployed and integrated Java 17 LTS, Python 3.11, PySpark 3.5.4, and Hadoop native binaries on the execution environment.
2. **Schema Discovery**: Executed full schema inference across 15,000,000 transaction rows and generated `results/schema_report.json`.
3. **Optimized Columnar Ingestion**: Converted raw 5.01 GB CSV data into snappy-compressed Parquet partitions (`results/raw`), eliminating repetitive parsing overheads.
4. **Data Transformation & Hygiene**: Implemented string trimming, duplicate resolution, null-label validation, and structured storage (`results/cleaned`).
5. **Explainable Risk Scoring Engine**: Formulated and executed a multi-factor heuristic scoring algorithm evaluating high-percentile transaction amounts and rare merchant profiles (`results/risk_scored`).

---

## 3. DATASET DESCRIPTION AND VERIFIED SCHEMA

The project utilizes the **CreditTransAct: A Profile-Driven Dataset for Scalable Credit Card Fraud Detection** benchmark (Mendeley Data, DOI: 10.17632/y64bbnm2s3.1).

### 3.1 Dataset Vital Statistics
- **Source File**: `data/credit_card_fraud.csv`
- **File Size**: 5,009,909,516 bytes (~5.01 GB CSV)
- **Total Ingested Records**: **15,000,000 rows**
- **Total Attribute Count**: **34 columns** (33 predictors/metadata fields + 1 ground-truth label `is_fraud`)
- **Partitions Processed**: 38 parallel Spark partitions

### 3.2 Verified Attribute Catalog (from `results/schema_report.json`)

| # | Column Name | Inferred Data Type | Semantic Description |
|:---|:---|:---|:---|
| 1 | `transaction_amount` | Double | Numerical monetary value of the transaction |
| 2 | `transaction_amount_bin` | String | Categorical amount tier (`low`, `medium`, `high`) |
| 3 | `avg_amount_deviation_sigma` | Double | Standard deviations from historical customer average |
| 4 | `merchant_category` | String | Commercial category (`grocery`, `electronics`, `travel`, etc.) |
| 5 | `merchant_risk_score` | String | Historical merchant risk profile (`low_risk`, `high_risk`) |
| 6 | `merchant_category_vs_history`| String | Category alignment with customer profile history |
| 7 | `geo_velocity_kmh` | Double | Calculated travel velocity between sequential transactions |
| 8 | `geo_velocity_bin` | String | Velocity category (`normal`, `fast`) |
| 9 | `geo_distance_km` | Double | Physical distance in kilometers from customer home |
| 10 | `geo_distance_bin` | String | Distance category (`same_location`, `intercity`, etc.) |
| 11 | `merchant_location` | String | Location context (`home_city`, `same_country`, `foreign`) |
| 12 | `country_consistency` | String | Country match indicator against domestic issuing bank |
| 13 | `ip_address_type` | String | Originating network IP type (`residential`, `corporate`, `datacenter`) |
| 14 | `device_fingerprint_match` | String | Device hardware identity status (`known_device`, `new_device`) |
| 15 | `session_duration_sec` | Double | Digital checkout interaction time in seconds |
| 16 | `session_duration_bin` | String | Interaction speed classification (`fast`, `normal`, `slow`) |
| 17 | `network_carrier_type` | String | Connection protocol (`wifi`, `mobile_data`, `datacenter_hosting`) |
| 18 | `cards_on_device_30d` | Integer | Count of unique payment cards bound to device within 30 days |
| 19 | `cvv_match_status` | String | CVV2/iCVV security verification result (`cvv2_match`, `mismatch`) |
| 20 | `three_ds_auth_result` | String | 3D-Secure authentication outcome (`frictionless_pass`, `challenge_fail`) |
| 21 | `tokenization_used` | String | Cardholder credential representation (`emv_chip_token`, `raw_pan_online`) |
| 22 | `failed_attempts_before_success`| Integer | Preceding rejected payment attempts prior to approval |
| 23 | `transaction_velocity_1h` | String | Hourly velocity bucket (`within_normal`, `elevated`) |
| 24 | `time_of_transaction` | String | Diurnal time window (`late_night_0_5`, `afternoon_12_18`, `evening_18_24`) |
| 25 | `account_credential_change_recency` | String | Proximity to password/MFA update (`no_recent_change`, `recent_change`) |
| 26 | `card_present_cnp` | String | Channel format (`card_present_swipe`, `cnp_online`, `cnp_moto`) |
| 27 | `order_shipping_speed` | String | Fulfillment logistics (`in_store_pickup`, `same_day`, `overnight`, `standard`) |
| 28 | `account_age_days` | Integer | Account tenure in days since initial creation |
| 29 | `chargeback_history_count` | Integer | Historical chargebacks logged against the customer account |
| 30 | `customer_id` | String | Unique customer identifier (Excluded from ML to prevent leakage) |
| 31 | `transaction_id` | String | Unique transaction record key (Excluded from ML) |
| 32 | `segment` | String | Customer spending profile segment (`A_established`, etc.) |
| 33 | `customer_type` | String | Behavioral classification (`customer_based`) |
| 34 | `is_fraud` | Integer | Target ground truth label (`0` = Legitimate, `1` = Fraudulent) |

---

## 4. SYSTEM REQUIREMENTS AND ARCHITECTURE

### 4.1 System Architectural Blueprint
The pipeline adheres to a decoupled layered architecture:
```
[Raw CSV Dataset (5.01 GB)]
           │
           ▼
[Stage 0: Schema Inspection] ──► results/schema_report.json
           │
           ▼
[Stage 1: Columnar Ingestion] ──► results/raw (Snappy Parquet)
           │
           ▼
[Stage 2: Transformation & Cleaning] ──► results/cleaned (Clean Parquet)
           │
           ▼
[Stage 3: Risk Scoring Intelligence] ──► results/risk_scored (Scored Parquet)
                                     ──► results/risk_category_summary.csv
```

### 4.2 Functional Responsibilities

| Pipeline Module | Source Script | Operations Performed | Output Artifact |
|:---|:---|:---|:---|
| **Inspection** | `pipeline/00_inspect_schema.py` | Full file scan, partition count, data type discovery, sample row extraction | `results/schema_report.json` |
| **Ingestion** | `pipeline/01_ingest.py` | Parallel CSV loading across 38 tasks, Snappy compression encoding | `results/raw/` |
| **Cleaning** | `pipeline/02_transform.py` | String column trimming, exact duplicate elimination, target non-null filter | `results/cleaned/` |
| **Risk Scoring** | `pipeline/03_risk_analysis.py` | Approx-quantile calculation, rare category profiling, rule reason array | `results/risk_scored/`, `risk_category_summary.csv` |

---

## 5. DEVELOPMENT ENVIRONMENT AND TECHNOLOGIES

To ensure optimal execution and overcome known Windows socket issues in PySpark:
- **Operating System**: Microsoft Windows 11 (64-bit)
- **Java Virtual Machine**: Microsoft Build of OpenJDK 17 LTS (`jdk-17.0.21.21-hotspot`)
- **Python Runtime**: Python 3.11.9 (Dedicated virtual environment `.venv`)
- **Hadoop Ecosystem Client**: Apache Hadoop 3.3.5 binaries (`winutils.exe` and `hadoop.dll`)
- **Core Processing Engine**: Apache Spark 3.5.4 (PySpark SQL + Catalyst Optimizer)
- **Analytical & Visualization Libraries**:
  - `pandas` 2.3.3
  - `pyarrow` 26.0.0
  - `matplotlib` 3.11.2
- **Memory Allocation**: Driver Memory: 6 GB; Executor Memory: 6 GB

---

## 6. DATA INGESTION AND STORAGE PIPELINE

### 6.1 CSV Parsing vs. Columnar Parquet
Reading 15 million records directly from raw uncompressed CSV requires intensive string parsing on every execution. Ingesting once into Apache Parquet yields:
- **Columnar Storage**: Queries selecting subsets of features skip irrelevant byte blocks on disk.
- **Snappy Compression**: Drastically reduces disk footprint and I/O bus contention.
- **Strict Typing**: Retains native integer, double, and string primitives without repetitive type inference.

### 6.2 Verified Ingestion Execution Log
```
Setting default log level to "WARN".
Input rows: 15,000,000 columns: 34
Raw layer written to results/raw
Execution Exit Code: 0 (Success)
```

---

## 7. DATA UNDERSTANDING AND QUALITY ASSESSMENT

### 7.1 Data Quality Findings
1. **Total Integrity**: All 15,000,000 records were successfully ingested without record corruption or truncation.
2. **Missing Value Analysis**: Target label `is_fraud` contained zero null entries across all 15 million rows.
3. **Whitespace Sanitation**: Categorical string attributes contained minor leading/trailing whitespace variations which were cleaned during Stage 2.
4. **Identifier Isolation**: Attributes `transaction_id` and `customer_id` represent unique identifiers and have been designated as excluded columns in `project_config.json` to prevent target leakage during predictive modelling.

---

## 8. DATA PREPROCESSING AND TRANSFORMATION LAYER

Stage 2 executed `pipeline/02_transform.py`:
- All 34 columns were examined; string-typed columns were trimmed using `F.trim()`.
- Deduplication via `df.dropDuplicates()` evaluated all 34 attributes across 15M records.
- Null-safety filters ensured all records have valid, populated target labels.
- Output: Cleaned dataset stored at `results/cleaned`.

```
Cleaned rows: 15,000,000 columns: 34
Cleaned layer: results/cleaned
Execution Exit Code: 0 (Success)
```

---

## 9. FRAUD DETECTION ALGORITHMS (PLANNED FOR MILESTONE 3)

The architecture includes configurations and pipelines for 5 machine learning classifiers implemented in Spark MLlib:
1. **Logistic Regression**: Linear baseline with L2 regularization.
2. **Decision Tree Classifier**: Rule-based tree partitioner (Max Depth: 8).
3. **Random Forest Classifier**: Ensemble of 50 trees with feature bagging.
4. **Gradient-Boosted Trees (GBT)**: Sequential boosting ensemble (Max Iter: 30, Max Depth: 5).
5. **Linear Support Vector Machine (LinearSVC)**: Maximum-margin hyperplane classifier.

*Note: Per Milestone 2 deliverables, execution was paused after Risk Analysis. Model training and evaluation will be executed in Milestone 3.*

---

## 10. RISK SCORING INTELLIGENCE AND EXPLAINABILITY

### 10.1 Heuristic Rule Logic
Rather than treating risk assessment as an uninterpretable score, `03_risk_analysis.py` implements an explainable, multi-component scoring engine:
- **Baseline Review Score**: Every transaction receives a baseline score of `10.0` points (`BASELINE_REVIEW`).
- **Top Decile Amount Indicator**:
  - Dynamically calculates the 90th percentile threshold of `transaction_amount` across 15 million records via `approxQuantile('transaction_amount', [0.90], 0.01)`.
  - Transactions exceeding this empirical threshold receive `+30.0` risk points and append reason code `AMOUNT_TOP_DECILE`.
- **Rare Merchant Profile Indicator**:
  - Computes merchant category transaction shares. Categories representing `< 5.0%` of transaction volume are flagged as rare.
  - Transactions in rare merchant categories receive `+20.0` risk points and append reason code `RARE_PROFILE`.
- **Composite Score Cap**: Capped at `100.0` points via `F.least(F.lit(100.0), score)`.

### 10.2 Risk Classification Bands
- **LOW Risk**: Score < 35.0
- **MEDIUM Risk**: 35.0 ≤ Score < 70.0
- **HIGH Risk**: Score ≥ 70.0

---

## 11. MODEL TRAINING AND VALIDATION STRATEGY
*(Architecture planned for Milestone 3)*
- **Data Splitting**: 80% Training partition, 20% Test partition (Seed: 42).
- **Feature Assembly**: Categorical encoding via `StringIndexer` and `OneHotEncoder`, combined with continuous numericals via `VectorAssembler`.
- **Leakage Prevention**: Transformations fitted strictly on training data prior to test transformation.

---

## 12. EVALUATION METRICS FRAMEWORK
When models are trained in Milestone 3, performance will be evaluated on:
- $\text{Precision} = \frac{TP}{TP + FP}$
- $\text{Recall} = \frac{TP}{TP + FN}$
- $\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$
- **ROC-AUC**: Binary Classification Evaluator metric.
- **Confusion Matrix**: Full tally of $TP, FP, TN, FN$.

---

## 13. IMPLEMENTATION WORKFLOW AND EXECUTION STATUS

### Milestone 2 Execution Audit

| Module | Command Executed | Input Path | Output Path | Status |
|:---|:---|:---|:---|:---|
| **00: Schema** | `python pipeline/00_inspect_schema.py` | `data/credit_card_fraud.csv` | `results/schema_report.json` | **VERIFIED (Code 0)** |
| **01: Ingestion** | `python pipeline/01_ingest.py` | `data/credit_card_fraud.csv` | `results/raw/` | **VERIFIED (Code 0)** |
| **02: Transform** | `python pipeline/02_transform.py` | `results/raw/` | `results/cleaned/` | **VERIFIED (Code 0)** |
| **03: Risk Analysis**| `python pipeline/03_risk_analysis.py` | `results/cleaned/` | `results/risk_scored/`, `risk_category_summary.csv` | **VERIFIED (Code 0)** |
| **04: Training** | `python pipeline/04_train_models.py` | `results/cleaned/` | `results/models/` | Deferred to Milestone 3 |
| **05: Evaluate** | `python pipeline/05_evaluate.py` | `results/model_metrics.csv` | `results/plots/` | Deferred to Milestone 3 |

---

## 14. MEASURED RESULTS, RISK DISTRIBUTION AND REPORTING

### 14.1 Verified Risk Categorization Summary
From active output file `results/risk_category_summary.csv`:

| Risk Category | Transaction Count | Percentage Share (%) | Operational Review Recommendation |
|:---|:---:|:---:|:---|
| **LOW** | 13,467,586 | 89.78% | Standard automated clearance; no intervention |
| **MEDIUM** | 1,532,414 | 10.22% | Secondary automated verification / step-up authentication |
| **HIGH** | 0 | 0.00% | Reserved for cumulative multi-factor rule alerts |
| **Total** | **15,000,000** | **100.00%** | Full dataset scored |

### 14.2 Key Analytical Observations
- **10.22% of total transactions** (1,532,414 transactions) were flagged with elevated risk (Medium) driven by top-decile spending spikes (`AMOUNT_TOP_DECILE`) or anomalous merchant categories (`RARE_PROFILE`).
- This 10.22% prioritization provides an operationally actionable triage queue for fraud investigators, focusing human attention on the most anomalous 1.53 million transactions out of 15 million.

---

## 15. TESTING, LIMITATIONS AND RISK MANAGEMENT

### 15.1 Testing Completed
- Verified PySpark worker process spawning on Windows with Python 3.11 and Microsoft OpenJDK 17.
- Verified Snappy Parquet write and read compatibility using Hadoop 3.3.5 `winutils.exe` and `hadoop.dll`.
- Validated exact preservation of row counts ($15,000,000 \rightarrow 15,000,000$) across ingestion, transformation, and risk scoring stages.

### 15.2 Limitations
- Synthetic data properties may reflect idealized customer distributions compared to live production banking networks.
- Local standalone Spark mode was utilized; execution on multi-node Cloudera/Hadoop clusters will yield higher parallel throughput.

---

## 16. TEAM CONTRIBUTIONS AND PROJECT MANAGEMENT

| Team Member | Roll Number | Key Responsibilities & Milestone 2 Deliverables |
|:---|:---|:---|
| **Srikashyap Amaravadi** | S24CSEU1423 | Architecture design, environment configuration, Spark session optimization, report synthesis |
| **Gitesh Goyal** | S24CSEU0774 | Dataset verification, partition configuration, Stage 0 schema discovery and Stage 1 Parquet ingestion |
| **Annya Sharma** | S24CSEU1408 | Data quality analysis, missing-value checks, Stage 2 transformation and cleaning pipeline |
| **Ajitej Singh** | S24CSEU1413 | Stage 3 risk scoring implementation, quantile calculation, reason-code rules, and summary reporting |

---

## 17. CONCLUSION AND FUTURE ROADMAP

Milestone 2 has successfully established a robust, scalable Big Data foundation for credit card fraud intelligence. Using Apache Spark 3.5.4, 15,000,000 transactions were ingested from a 5.01 GB raw CSV file, converted into optimized Parquet data layers, cleaned, and evaluated through an explainable heuristic risk scoring engine. 

### Roadmap for Milestone 3 (Final Milestone):
1. Execute `04_train_models.py` to train and persist all 5 candidate ML classifiers (Logistic Regression, Decision Tree, Random Forest, GBT, Linear SVM).
2. Execute `05_evaluate.py` to generate confusion matrices, ROC-AUC comparisons, and visualization plots.
3. Integrate ML probabilities with rule-based risk scores for hybrid fraud prioritization.

---

## REFERENCES
1. CreditTransAct: A Profile-Driven Dataset for Scalable Credit Card Fraud Detection, Mendeley Data, Version 1, 9 May 2026. DOI: 10.17632/y64bbnm2s3.1.
2. Apache Spark 3.5.4 Documentation: https://spark.apache.org/docs/3.5.4/
3. Apache Hadoop 3.3.5 Documentation: https://hadoop.apache.org/docs/r3.3.5/
4. Apache Spark MLlib Programming Guide: https://spark.apache.org/docs/3.5.4/ml-guide.html
5. Python 3.11 Documentation: https://docs.python.org/3.11/
