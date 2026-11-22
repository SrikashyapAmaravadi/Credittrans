# BENNETT UNIVERSITY
## SCHOOL OF COMPUTER SCIENCE ENGINEERING & TECHNOLOGY

### FINAL PROJECT COMPREHENSIVE IMPLEMENTATION REPORT
**SCALABLE FINANCIAL FRAUD DETECTION AND RISK INTELLIGENCE USING APACHE SPARK, HADOOP AND MACHINE LEARNING**

- **Course Code**: CSET371 — Big Data Analytics and Business Intelligence
- **Faculty Guide**: Dr. Aditya Bharadwaj
- **Academic Year**: 2026

**Submitted by:**
- **Srikashyap Amaravadi** (S24CSEU1423)
- **Gitesh Goyal** (S24CSEU0774)
- **Annya Sharma** (S24CSEU1408)
- **Ajitej Singh** (S24CSEU1413)

---

## EXECUTIVE SUMMARY
Financial fraud presents an existential risk to global payment networks due to unprecedented transaction velocities, astronomical data volumes, and subtle evasion tactics deployed by bad actors. Traditional relational database architectures and monolithic statistical engines fail to scale horizontally when processing multi-gigabyte transaction streams in real-time.

This project delivers a complete, production-grade distributed Big Data and Machine Learning pipeline engineered using **Apache Spark 3.5.4**, **Apache Hadoop 3.3.5**, and **Python 3.11**. The system is evaluated on the benchmark **CreditTransAct** dataset (`credit_card_fraud.csv`), encompassing **15,000,000 transaction records across 34 feature dimensions (~5.01 GB uncompressed)**.

The end-to-end architecture integrates:
1. **Automated Schema Discovery & Profiling**: Automated schema inference and verification (`00_inspect_schema.py`).
2. **Columnar Distributed Ingestion**: High-throughput transformation from raw CSV to Snappy-compressed columnar Parquet partitions (`01_ingest.py`).
3. **Data Hygiene & Transformation**: Trimming, deduplication, null-label elimination, and feature isolation (`02_transform.py`).
4. **Explainable Heuristic Risk Scoring**: Multi-factor scoring incorporating empirical 90th percentile transaction amounts and rare merchant profile indicators (`03_risk_analysis.py`).
5. **Distributed Machine Learning Pipeline**: Parallel feature engineering (`StringIndexer`, `OneHotEncoder`, `VectorAssembler`) and training of 5 Spark MLlib classifiers: **Logistic Regression, Decision Tree, Random Forest, Gradient-Boosted Trees (GBT), and Linear SVM** (`04_train_models.py`).
6. **Rigorous Statistical Evaluation**: Calculation of Precision, Recall, F1-Score, ROC-AUC, and generation of full Confusion Matrices and analytical charts (`05_evaluate.py`).
7. **Hybrid Operational Triage Engine**: Integration of ML fraud probabilities with rule-based heuristics into an actionable 4-tier decision matrix for automated clearance and instant blocking (`06_hybrid_inference.py`).

All results documented herein reflect verified empirical outputs computed by the active pipeline on the execution environment.

---

## 1. PROJECT OBJECTIVES & ARCHITECTURE

### 1.1 Core Objectives
1. **Distributed Scalability**: Eliminate single-node I/O bottlenecks by converting raw CSV data into partitioned, snappy-compressed columnar Parquet files.
2. **Feature Engineering Without Leakage**: Enforce strict separation between training and test distributions, isolating customer and transaction identifiers while encoding high-dimensional categorical features.
3. **High-Performance Predictive Modeling**: Benchmark linear, tree-based, and ensemble classifiers in Apache Spark MLlib under heavy class imbalance (~4.90% fraud prevalence).
4. **Explainability & Operationalization**: Provide dual-layer protection combining explainable heuristic reason codes with calibrated ML fraud likelihoods.

### 1.2 Architectural Workflow
```
[ Raw CSV: 15M Rows (~5.01 GB) ]
              │
              ▼  (00_inspect_schema.py)
   [ Schema Discovery & Verification ]
              │
              ▼  (01_ingest.py)
   [ Raw Parquet Layer: results/raw/ ]
              │
              ▼  (02_transform.py)
   [ Cleaned Parquet Layer: results/cleaned/ ]
              │
      ┌───────┴───────────────────────────────┐
      ▼                                       ▼
(03_risk_analysis.py)                   (04_train_models.py)
[ Rule-Based Heuristic Scoring ]       [ Distributed MLlib Training ]
 - Top Decile Amount (+30 pts)          - Feature Pipeline (OHE + Assembler)
 - Rare Merchant Profile (+20 pts)      - 80/20 Train/Test Partitioning
 - LOW / MEDIUM / HIGH Bands            - 5 Scalable Classifiers
      │                                       │
      │                                       ▼  (05_evaluate.py)
      │                                [ Model Metrics & Confusion Plots ]
      │                                       │
      └───────────────────┬───────────────────┘
                          ▼  (06_hybrid_inference.py)
            [ Hybrid Fraud Triage Engine ]
             - Tier 1: Critical Emergency (Instant Block)
             - Tier 2: Machine Learning Alert (Step-Up 2FA)
             - Tier 3: Compliance Audit (Human Review)
             - Tier 4: Automated Clearance (Frictionless)
```

---

## 2. DATASET SPECIFICATION AND SCHEMA

The system was deployed on the full **CreditTransAct** benchmark dataset comprising **15,000,000 records** and **34 columns**.

### 2.1 Key Dataset Attributes
- **Target Label**: `is_fraud` (0 = Legitimate, 1 = Fraudulent).
- **Target Class Distribution**:
  - Legitimate (0): **14,264,776 records (95.10%)**
  - Fraudulent (1): **735,224 records (4.90%)**
  - Total: **15,000,000 records**
- **Excluded Features (Target Leakage Prevention)**: `customer_id`, `transaction_id`.
- **Numerical Predictors (9 features)**: `transaction_amount`, `avg_amount_deviation_sigma`, `geo_velocity_kmh`, `geo_distance_km`, `session_duration_sec`, `cards_on_device_30d`, `failed_attempts_before_success`, `account_age_days`, `chargeback_history_count`.
- **Categorical Predictors (22 features)**: `transaction_amount_bin`, `merchant_category`, `merchant_risk_score`, `merchant_category_vs_history`, `geo_velocity_bin`, `geo_distance_bin`, `merchant_location`, `country_consistency`, `ip_address_type`, `device_fingerprint_match`, `session_duration_bin`, `network_carrier_type`, `cvv_match_status`, `three_ds_auth_result`, `tokenization_used`, `transaction_velocity_1h`, `time_of_transaction`, `account_credential_change_recency`, `card_present_cnp`, `order_shipping_speed`, `segment`, `customer_type`.

---

## 3. HEURISTIC RISK SCORING ENGINE (STAGE 3)

The rule-based layer provides transparent, audit-compliant scoring:
- **Baseline Review Score**: `10.0` points assigned to all transactions (`BASELINE_REVIEW`).
- **Empirical Top Decile Amount**: Evaluates `approxQuantile('transaction_amount', [0.90], 0.01)`. Transactions exceeding the 90th percentile threshold receive `+30.0` points (`AMOUNT_TOP_DECILE`).
- **Rare Merchant Profile**: Computes transaction volume share across all merchant categories. Categories with `< 5.0%` aggregate volume receive `+20.0` points (`RARE_PROFILE`).
- **Composite Score Range**: Capped at `100.0` points.

### Heuristic Scoring Distribution (15,000,000 records)
| Risk Band | Score Range | Record Count | Percentage | Operational Policy |
|:---|:---:|:---:|:---:|:---|
| **LOW** | 0.0 - 34.9 | 13,467,586 | 89.78% | Standard frictionless processing |
| **MEDIUM** | 35.0 - 69.9 | 1,532,414 | 10.22% | Triage queue / automated step-up verification |
| **HIGH** | 70.0 - 100.0 | 0 | 0.00% | Reserved for compounding multi-factor triggers |
| **Total** | | **15,000,000** | **100.00%** | |

---

## 4. MACHINE LEARNING MODEL BENCHMARK (STAGE 4 & 5)

### 4.1 Training & Testing Configuration
- **Total In-Scope Dataset**: 1,501,643 transactions (~10% representative stratified partition).
- **Train Partition (80%)**: 1,201,347 transactions.
- **Test Partition (20%)**: 300,296 transactions.
- **Actual Frauds in Test Set**: 14,513 transactions (~4.83%).
- **Actual Legitimate in Test Set**: 285,783 transactions (~95.17%).
- **Feature Engineering Pipeline**: 22 `StringIndexer` stages + 22 `OneHotEncoder` stages + 9 continuous numeric features aggregated via `VectorAssembler`.

### 4.2 Comprehensive Model Performance Metrics
All metrics were evaluated on the unseen holdout test partition (300,296 records):

| Model Name | Precision | Recall | F1-Score | ROC-AUC | True Positives (TP) | False Positives (FP) | False Negatives (FN) | True Negatives (TN) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Linear SVM** | **0.999649** | **0.980087** | **0.989771** | **0.998022** | **14,224** | **5** | **289** | **285,778** |
| **Logistic Regression** | 0.998805 | 0.979398 | 0.989006 | **0.999019** | 14,214 | 17 | 299 | 285,766 |
| **Random Forest** | **0.999715** | 0.967684 | 0.983439 | 0.996831 | 14,044 | **4** | 469 | **285,779** |
| **Gradient-Boosted Trees (GBT)** | 0.999146 | 0.967477 | 0.983057 | 0.990636 | 14,041 | 12 | 472 | 285,771 |
| **Decision Tree** | 0.994748 | 0.965686 | 0.980001 | 0.886405 | 14,015 | 74 | 498 | 285,709 |

### 4.3 Key Analytical Insights
1. **Champion Model — Linear SVM & Random Forest**:
   - **Linear SVM** achieved the highest overall balance of F1-Score (**0.9898**) and Recall (**98.01%**), missing only 289 fraud attempts while misclassifying only 5 legitimate transactions out of 285,783.
   - **Random Forest** achieved the lowest False Positive count (**4 false alarms out of 285,783 legitimate transactions**), yielding a Precision of **99.97%**.
2. **Logistic Regression Excellence**:
   - Logistic Regression achieved an exceptional ROC-AUC of **0.9990**, proving that the one-hot encoded interaction features and normalized continuous signals provide sharp linear separability.
3. **Execution Efficiency**:
   - Feature engineering completed in 106.46 seconds.
   - Model training runtimes: Decision Tree (12.6s), Linear SVM (23.1s), Logistic Regression (27.5s), Random Forest (36.6s), GBT (46.7s).

---

## 5. HYBRID FRAUD TRIAGE & DECISION ENGINE (STAGE 6)

In enterprise banking environments, binary classifications are insufficient for operational fraud teams. The system incorporates a 4-tier decision engine combining model probabilities with heuristic risk policies:

| Triage Tier | Operational Action | Criteria | Volume Count | Volume Share (%) | Fraud Capture | Legitimate Flow |
|:---|:---|:---|:---:|:---:|:---:|:---:|
| **Tier 1: Critical Emergency** | Immediate card freeze & security SMS | Pred = 1 & Prob $\ge 0.85$ | 14,168 | 4.72% | 14,163 (99.96%) | 5 (0.04%) |
| **Tier 2: Step-Up Auth** | 2FA Challenge (Biometric / OTP) | Pred = 1 & Prob $< 0.85$ | 63 | 0.02% | 51 (80.95%) | 12 (19.05%) |
| **Tier 3: Compliance Audit** | Asynchronous investigation queue | Pred = 0 & Prob $\ge 0.20$ | 102 | 0.03% | 14 (13.73%) | 88 (86.27%) |
| **Tier 4: Automated Clearance** | Instant frictionless clearance | Pred = 0 & Prob $< 0.20$ | 285,963 | 95.23% | 285 (0.10%) | 285,678 (99.90%) |
| **Total Evaluated** | | | **300,296** | **100.00%** | **14,513** | **285,783** |

### Operational Impact
- **95.23% of transactions** pass automatically with zero friction and zero latency.
- **97.59% of all fraud cases** (14,163 out of 14,513) are halted instantly at Tier 1 with an unprecedented precision of **99.96%**.
- Borderline transactions (165 total cases across Tiers 2 and 3) are routed to step-up authentication or analyst queues without inconveniencing normal cardholders.

---

## 6. PROJECT ARTIFACTS INVENTORY

| Directory / File | Description | Status |
|:---|:---|:---|
| `data/credit_card_fraud.csv` | Raw CreditTransAct dataset (~5.01 GB, 15M records) | Complete |
| `results/raw/` | Raw ingested Parquet layer (Snappy compressed) | Complete |
| `results/cleaned/` | Sanitized, deduplicated, null-validated Parquet layer | Complete |
| `results/risk_scored/` | Heuristic scored dataset with explainable reason codes | Complete |
| `results/risk_category_summary.csv` | Empirical risk category distribution summary | Complete |
| `results/models/` | Serialized Spark ML PipelineModels (5 models) | Complete |
| `results/predictions/` | Parquet test predictions with probabilities (5 models) | Complete |
| `results/model_metrics.csv` | Full benchmark metrics table (Precision, Recall, F1, AUC, Confusion Matrix) | Complete |
| `results/plots/` | 10 high-resolution analytical charts and confusion matrices | Complete |
| `results/hybrid_triage_summary.csv` | Hybrid multi-tier triage decision breakdown | Complete |
| `results/hybrid_action_volumes.csv` | Tier-wise transaction volume shares | Complete |

---

## 7. TEAM CONTRIBUTIONS & PROJECT GOVERNANCE

| Team Member | Roll Number | Key Responsibilities & Final Deliverables |
|:---|:---|:---|
| **Srikashyap Amaravadi** | S24CSEU1423 | System architecture, Spark session tuning, ML pipeline optimization, report compilation |
| **Gitesh Goyal** | S24CSEU0774 | Distributed schema profiling, raw Parquet ingestion layer, memory optimization |
| **Annya Sharma** | S24CSEU1408 | Data hygiene layer, feature isolation, StringIndexer/OneHotEncoder design |
| **Ajitej Singh** | S24CSEU1413 | Heuristic risk engine, hybrid triage matrix implementation, visual analytics |

---

## 8. CONCLUSION
The CreditTransAct Financial Fraud Analytics project has achieved 100% of its planned objectives. By combining the distributed computational scale of **Apache Spark 3.5.4** and **Hadoop 3.3.5** with state-of-the-art machine learning classifiers, the system successfully processes millions of records, achieves a peak **F1-Score of 0.9898**, a precision of **99.97%**, and establishes a production-grade 4-tier decision triage engine for modern financial institutions.
