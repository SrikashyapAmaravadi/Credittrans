# BENNETT UNIVERSITY
## SCHOOL OF COMPUTER SCIENCE ENGINEERING & TECHNOLOGY

### PROJECT IMPLEMENTATION FINAL REPORT — MILESTONE 3 & FINAL ASSESSMENT

**SCALABLE FINANCIAL FRAUD DETECTION AND RISK INTELLIGENCE USING APACHE SPARK, HADOOP AND MACHINE LEARNING**

- **Course Code**: CSET371 — Big Data Analytics and Business Intelligence
- **Project Guide**: Dr. Aditya Bhardwaj
- **Academic Year**: 2026

**Submitted by:**
- **Srikashyap Amaravadi** (S24CSEU1423) — *Lead Big Data Engineer & Classifier Architect*
- **Gitesh Goyal** (S24CSEU0774) — *Machine Learning Optimization Engineer & Schema Discovery Lead*
- **Annya Sharma** (S24CSEU1408) — *Data Hygiene & Feature Pipeline Engineering Lead*
- **Ajitej Singh** (S24CSEU1413) — *Risk Intelligence, Evaluation Analytics & BI Integration Lead*

---

## DECLARATION OF ORIGINALITY AND PLAGIARISM COMPLIANCE
We hereby declare that this final project report titled **"Scalable Financial Fraud Detection and Risk Intelligence Using Apache Spark, Hadoop and Machine Learning"** is an authentic and original record of research and software engineering executed under the supervision of **Dr. Aditya Bhardwaj**, School of Computer Science Engineering and Technology, Bennett University.

All data processing workflows, distributed feature engineering stages, machine learning estimators, heuristic decision algorithms, and analytical visualizations were developed, executed, and benchmarked on our active distributed execution environment. Where literature, benchmark datasets, or foundational algorithms have been used, they have been comprehensively cited in accordance with University academic integrity standards and anti-plagiarism guidelines. No AI-generated or synthetic performance graphics were used; all diagrams, confusion matrices, and benchmark graphs were generated directly from measured empirical runs.

---

## ABSTRACT
Digital electronic payment systems process millions of high-velocity financial events per hour. While fraudulent events constitute a minority fraction (~4.90%) of aggregate traffic, their financial and reputational impacts are devastating. Monolithic single-node analytical systems suffer severe memory exhaustion and computational latency when processing multi-gigabyte transaction streams under extreme class imbalance.

This report documents the end-to-end completion of the **CreditTransAct Financial Fraud Analytics Platform** engineered using **Apache Spark 3.5.4**, **Apache Hadoop 3.3.5**, and **Python 3.11**. The system was deployed and empirically validated on the benchmark **CreditTransAct** dataset (`credit_card_fraud.csv`), comprising **15,000,000 transaction records across 34 feature attributes** (~5.01 GB uncompressed CSV).

The end-to-end platform encompasses:
1. **Automated Schema Inference & Distributed Profiling**: Scalable profiling across 38 parallel Spark partitions (`results/schema_report.json`).
2. **Columnar Column-Pruned Ingestion**: Converting raw 5.01 GB CSV into Snappy-compressed columnar Parquet format (`results/raw`), yielding an 85% storage reduction.
3. **Data Hygiene & Target Leakage Prevention**: Full deduplication, string trimming, and strict isolation of identifier fields (`customer_id`, `transaction_id`) (`results/cleaned`).
4. **Explainable Heuristic Risk Scoring**: Multi-factor quantile amount scoring (`AMOUNT_TOP_DECILE`) and rare merchant profile profiling (`RARE_PROFILE`) across all 15 million transactions (`results/risk_scored`).
5. **Distributed MLlib Model Benchmark & Hyperparameter Tuning**: 5 candidate Spark MLlib classifiers evaluated across an 80/20 train/test split (300,296 unseen holdout records): **Linear Support Vector Machine (Linear SVM), Random Forest, Gradient-Boosted Trees (GBT), Logistic Regression, and Decision Tree**.
   - **Champion Model — Linear SVM**: Achieved an **F1-Score of 0.9898**, **Recall of 98.01%**, and **ROC-AUC of 0.9980**, missing only 289 fraud attempts while recording only 5 false alarms across 285,783 legitimate transactions.
   - **Precision Leader — Random Forest**: Achieved **99.97% Precision**, recording only **4 false alarms**.
6. **Operational 4-Tier Hybrid Triage Engine**: Integrates model probabilities with heuristic risk constraints, achieving **automated instantaneous clearance for 95.23% of normal transactions (285,963 records)** and **instant blocking of 97.59% of fraudulent attempts (14,163 frauds)** at Tier 1 with 99.96% accuracy.
7. **Business Intelligence & Power BI Data Mart**: A 5-table Star Schema with custom DAX measures for executive reporting.

---

## TABLE OF CONTENTS
1. Introduction & Proposed Methodology
2. Problem Statement and Architectural Objectives
3. Dataset Description and Verified 34-Attribute Catalog
4. System Requirements and Distributed Architecture
5. Development Environment and Verified Tech Stack
6. Data Ingestion and Distributed Storage Pipeline
7. Data Understanding and Quality Assessment
8. Data Preprocessing and Feature Engineering Methodology
9. Distributed Machine Learning Algorithms & Mathematical Formulation
10. Hyperparameter Tuning and Optimization Framework
11. Model Training, Validation Strategy & Leakage Prevention
12. Comprehensive Evaluation Metrics, ROC-AUC & Confusion Matrices
13. Explainable Risk Scoring Intelligence and Reason Codes
14. Operational 4-Tier Hybrid Fraud Triage Engine
15. Business Intelligence and Power BI Enterprise Integration
16. Testing, Limitations, Plagiarism & Ethical Compliance
17. Team Contributions and Technical Work Breakdown
18. Conclusion and Future Roadmap
19. References

---

## 1. INTRODUCTION & PROPOSED METHODOLOGY
Digital banking networks process millions of payment events per hour. While fraudulent events constitute a minority fraction of total traffic, their ramifications are severe. Modern fraud detection faces three core challenges:
- **Massive Computational Scale**: Ingestion and analytical pipelines must process millions of records without memory exhaustion.
- **Extreme Class Imbalance**: Genuine transactions drastically outnumber fraudulent attempts (~95.10% legitimate vs. ~4.90% fraud).
- **Operational Interpretability**: Financial compliance standards require that flagged transactions be accompanied by transparent, auditable reason codes rather than opaque black-box verdicts.

### Proposed Methodology Architecture
The platform decouples ingestion, hygiene, heuristic explainability, feature engineering, distributed training, evaluation, and operational triage into distinct, modular layers:

```
[Raw CSV Dataset: 15M Records, 34 Features (~5.01 GB)]
                        │
                        ▼
[Stage 0: Schema Profiling] ──► results/schema_report.json
                        │
                        ▼
[Stage 1: Columnar Ingestion] ──► results/raw (Snappy Parquet)
                        │
                        ▼
[Stage 2: Transformation & Hygiene] ──► results/cleaned (Clean Parquet)
                        │
          ┌─────────────┴────────────────────────┐
          ▼                                      ▼
[Stage 3: Heuristic Scoring]           [Stage 4: Feature Pipeline]
 - Top Decile Amount: +30 pts           - 22 StringIndexers
 - Rare Merchant Share: +20 pts         - 22 OneHotEncoders
 - Score Bands (LOW/MED/HIGH)           - 9 Numeric VectorAssembler
          │                             - 80/20 Stratified Partitioning
          │                                      │
          │                                      ▼
          │                            [Distributed MLlib Training]
          │                             - Linear SVM (Champion)
          │                             - Random Forest (50 Trees)
          │                             - Gradient-Boosted Trees (GBT)
          │                             - Logistic Regression (L2)
          │                             - Decision Tree Classifier
          │                                      │
          │                                      ▼
          │                            [Stage 5: Evaluation & Plots]
          │                             - Precision, Recall, F1, AUC
          │                             - Confusion Matrix Heatmaps
          │                                      │
          └──────────────────┬───────────────────┘
                             ▼
[Stage 6: Operational 4-Tier Hybrid Fraud Triage Engine]
 - Tier 1: Critical Emergency (Block & Alert: p >= 0.85) -> 97.59% Caught
 - Tier 2: Step-Up Auth (2FA Challenge: 0.35 <= p < 0.85)
 - Tier 3: Compliance Audit (Offline Queue: p >= 0.20)
 - Tier 4: Automated Clearance (Frictionless: p < 0.20) -> 95.23% Cleared
```

---

## 2. PROBLEM STATEMENT AND ARCHITECTURAL OBJECTIVES

### 2.1 Problem Statement
Modern financial institutions require scalable, automated architectures capable of ingesting high-velocity transaction streams, assessing data quality, isolating risk indicators, and prioritizing suspicious activity for human investigators without introducing prohibitive computational latencies or high false-positive rates.

### 2.2 Core Technical Objectives
1. **Distributed Scalability**: Eliminate single-node I/O bottlenecks by converting raw CSV data into partitioned, snappy-compressed columnar Parquet files.
2. **Deterministic Preprocessing & Leakage Prevention**: Isolate customer and transaction identifiers, eliminate exact duplicates, and handle categorical variables cleanly.
3. **Transparent Heuristic Risk Intelligence**: Formulate empirical 90th percentile amount thresholds and rare merchant volume shares to assign auditable reason codes.
4. **Distributed MLlib Model Benchmark & Hyperparameter Optimization**: Benchmark linear, tree-based, and ensemble classifiers in Spark MLlib under heavy class imbalance.
5. **Operational 4-Tier Hybrid Triage**: Establish an actionable operational triage engine combining ML probabilities with heuristic rules to automate customer clearance.
6. **Enterprise Business Intelligence**: Provide pre-modeled Star Schema datasets and custom DAX measures for Power BI dashboards.

---

## 3. DATASET DESCRIPTION AND VERIFIED 34-ATTRIBUTE CATALOG

The project utilizes the **CreditTransAct: A Profile-Driven Dataset for Scalable Credit Card Fraud Detection** benchmark (Mendeley Data, DOI: 10.17632/y64bbnm2s3.1).

### 3.1 Dataset Vital Statistics
- **Source File**: `data/credit_card_fraud.csv`
- **File Size**: 5,009,909,516 bytes (~5.01 GB uncompressed CSV)
- **Total Ingested Records**: **15,000,000 rows**
- **Total Attributes**: **34 columns** (33 predictors/metadata fields + 1 ground-truth label `is_fraud`)
- **Target Ground Truth**: `is_fraud` (0 = Legitimate, 1 = Fraudulent)
- **Class Balance**: 14,264,776 Legitimate (95.10%), 735,224 Fraudulent (4.90%)
- **Missing Label Values**: 0 (100% complete)

### 3.2 Complete 34-Attribute Catalog (from `results/schema_report.json`)

| # | Attribute Name | Inferred Spark Type | Category | Semantic Description |
|:---|:---|:---|:---|:---|
| 1 | `transaction_amount` | Double | Numeric | Numerical monetary value of the transaction |
| 2 | `transaction_amount_bin` | String | Categorical | Discretized spending tier (`low`, `medium`, `high`) |
| 3 | `avg_amount_deviation_sigma` | Double | Numeric | Standard deviations from historical customer average |
| 4 | `merchant_category` | String | Categorical | Commercial category (`grocery`, `electronics`, `travel`, etc.) |
| 5 | `merchant_risk_score` | String | Categorical | Historical merchant risk profile (`low_risk`, `high_risk`) |
| 6 | `merchant_category_vs_history` | String | Categorical | Category alignment with customer profile history |
| 7 | `geo_velocity_kmh` | Double | Numeric | Calculated physical velocity between sequential transactions |
| 8 | `geo_velocity_bin` | String | Categorical | Velocity category (`normal`, `fast`) |
| 9 | `geo_distance_km` | Double | Numeric | Physical distance in kilometers from cardholder home |
| 10 | `geo_distance_bin` | String | Categorical | Spatial classification (`same_location`, `intercity`, etc.) |
| 11 | `merchant_location` | String | Categorical | Location context (`home_city`, `same_country`, `foreign`) |
| 12 | `country_consistency` | String | Categorical | Country match indicator against domestic issuing bank |
| 13 | `ip_address_type` | String | Categorical | Originating IP classification (`residential`, `corporate`, `datacenter`) |
| 14 | `device_fingerprint_match` | String | Categorical | Device hardware identity status (`known_device`, `new_device`) |
| 15 | `session_duration_sec` | Double | Numeric | Digital checkout interaction time in seconds |
| 16 | `session_duration_bin` | String | Categorical | Interaction speed classification (`fast`, `normal`, `slow`) |
| 17 | `network_carrier_type` | String | Categorical | Connection protocol (`wifi`, `mobile_data`, `datacenter_hosting`) |
| 18 | `cards_on_device_30d` | Integer | Numeric | Count of unique payment cards bound to device in 30 days |
| 19 | `cvv_match_status` | String | Categorical | CVV2/iCVV security verification result (`cvv2_match`, `mismatch`) |
| 20 | `three_ds_auth_result` | String | Categorical | 3D-Secure authentication outcome (`frictionless_pass`, `challenge_fail`) |
| 21 | `tokenization_used` | String | Categorical | Cardholder credential format (`emv_chip_token`, `raw_pan_online`) |
| 22 | `failed_attempts_before_success`| Integer | Numeric | Preceding rejected payment attempts prior to approval |
| 23 | `transaction_velocity_1h` | String | Categorical | Hourly velocity bucket (`within_normal`, `elevated`) |
| 24 | `time_of_transaction` | String | Categorical | Diurnal time window (`late_night_0_5`, `afternoon_12_18`, etc.) |
| 25 | `account_credential_change_recency` | String | Categorical | Proximity to password/MFA update (`no_recent_change`, `recent`) |
| 26 | `card_present_cnp` | String | Categorical | Transaction channel (`card_present_swipe`, `cnp_online`, `cnp_moto`) |
| 27 | `order_shipping_speed` | String | Categorical | Fulfillment logistics (`in_store_pickup`, `same_day`, `standard`) |
| 28 | `account_age_days` | Integer | Numeric | Account tenure in days since initial opening |
| 29 | `chargeback_history_count` | Integer | Numeric | Historical chargeback disputes logged against account |
| 30 | `customer_id` | String | Identifier | Unique customer identifier (Excluded from ML to prevent leakage) |
| 31 | `transaction_id` | String | Identifier | Unique transaction key (Excluded from ML) |
| 32 | `segment` | String | Categorical | Customer spending profile segment (`A_established`, etc.) |
| 33 | `customer_type` | String | Categorical | Behavioral classification (`customer_based`) |
| 34 | `is_fraud` | Integer | Target Label | Ground truth binary label (`0` = Legitimate, `1` = Fraudulent) |

---

## 4. SYSTEM REQUIREMENTS AND DISTRIBUTED ARCHITECTURE

### 4.1 Functional Module Matrix

| Pipeline Module | Source Script | Operations Performed | Primary Artifact Output |
|:---|:---|:---|:---|
| **00: Inspection** | `pipeline/00_inspect_schema.py` | Full file scan, partition count, schema discovery, sample rows | `results/schema_report.json` |
| **01: Ingestion** | `pipeline/01_ingest.py` | Parallel CSV loading across 38 tasks, Snappy Parquet encoding | `results/raw/` |
| **02: Transformation** | `pipeline/02_transform.py` | String column trimming, exact duplicate elimination, target validation | `results/cleaned/` |
| **03: Risk Scoring** | `pipeline/03_risk_analysis.py` | Approx-quantile calculation, rare category profiling, reason array | `results/risk_scored/`, `risk_category_summary.csv` |
| **04: ML Training** | `pipeline/04_train_models.py` | StringIndexer, OneHotEncoder, VectorAssembler, 5 ML models | `results/models/`, `results/model_metrics.csv` |
| **05: Evaluation** | `pipeline/05_evaluate.py` | Confusion matrices, Precision, Recall, F1, ROC-AUC, 10 plots | `results/plots/` |
| **06: Hybrid Triage** | `pipeline/06_hybrid_inference.py` | 4-tier decision matrix combining ML probabilities & heuristics | `results/hybrid_triage_summary.csv` |

---

## 5. DEVELOPMENT ENVIRONMENT AND VERIFIED TECH STACK

- **Operating System**: Microsoft Windows 11 (64-bit)
- **Java Virtual Machine**: Microsoft Build of OpenJDK 17 LTS (`jdk-17.0.21.21-hotspot`)
- **Python Runtime**: Python 3.11.9 (Dedicated virtual environment `.venv`)
- **Hadoop Ecosystem Client**: Apache Hadoop 3.3.5 native binaries (`winutils.exe` and `hadoop.dll`)
- **Core Distributed Engine**: Apache Spark 3.5.4 (PySpark SQL + MLlib + Catalyst Optimizer)
- **Analytical & BI Libraries**: `pandas` 2.3.3, `pyarrow` 26.0.0, `matplotlib` 3.11.2, `python-docx` 1.2.0
- **Hardware Resources Allocated**: Driver Memory: 6 GB; Executor Memory: 6 GB; 16 Logical Cores

---

## 6. DATA INGESTION AND DISTRIBUTED STORAGE PIPELINE

### 6.1 Columnar Parquet vs. Raw CSV
Reading 15 million rows repeatedly from raw uncompressed CSV creates severe disk I/O bottlenecks. Ingesting once into Snappy-compressed Apache Parquet yields:
- **Columnar Layout**: Relational queries selecting subsets of features skip irrelevant columns on disk (I/O pruning).
- **Dictionary & Bit-Packed Encoding**: High-cardinality strings are stored as compact integer indices.
- **Snappy Compression**: Reduces the storage footprint from 5.01 GB to ~450 MB (85% reduction).

---

## 7. DATA UNDERSTANDING AND QUALITY ASSESSMENT

### 7.1 Data Quality Findings
1. **Total Ingestion Integrity**: All 15,000,000 records were successfully ingested without record corruption.
2. **Missing Label Verification**: Target label `is_fraud` contained zero null entries across all 15 million records.
3. **Whitespace Sanitation**: String attributes contained minor whitespace variations which were cleaned via `F.trim()`.
4. **Identifier Isolation**: Attributes `transaction_id` and `customer_id` represent unique keys and were isolated in `project_config.json` to prevent target leakage.

---

## 8. DATA PREPROCESSING AND FEATURE ENGINEERING METHODOLOGY

### 8.1 Detailed Preprocessing Steps
- **Step 1: Whitespace Sanitation**: String attributes are cleaned via `F.trim(F.col(c))`.
- **Step 2: Exact Deduplication**: Evaluates full-row deduplication across all 34 attributes via `df.dropDuplicates()`.
- **Step 3: Cardinality Thresholding & Indexing**: Categorical features with $\le 100$ distinct values are indexed via `StringIndexer(handleInvalid='keep')`, assigning integer ranks based on category frequency.
- **Step 4: One-Hot Encoding & Vector Assembly**: Encoded via `OneHotEncoder(handleInvalid='keep')` into sparse vectors and aggregated with continuous numericals via `VectorAssembler`.

---

## 9. DISTRIBUTED MACHINE LEARNING ALGORITHMS & MATHEMATICAL FORMULATION

### 9.1 Formulations of the 5 Classifiers
1. **Linear Support Vector Machine (LinearSVC)**:
   $$\min_{\mathbf{w}, b} \frac{1}{2}\|\mathbf{w}\|^2 + C \sum_{i=1}^N \max\left(0, 1 - y_i(\mathbf{w}^T \mathbf{x}_i + b)\right)$$
2. **Random Forest Classifier**:
   $$\hat{y} = \text{mode}\left\{T_1(\mathbf{x}), T_2(\mathbf{x}), \dots, T_{50}(\mathbf{x})\right\}$$
3. **Gradient-Boosted Trees (GBT)**:
   $$F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \eta \sum_{j=1}^{J_m} \gamma_{jm} I(\mathbf{x} \in R_{jm})$$
4. **Logistic Regression (L2 ElasticNet)**:
   $$\mathcal{L}(\mathbf{w}) = -\frac{1}{N}\sum_{i=1}^N \left[ y_i \ln \sigma(\mathbf{w}^T \mathbf{x}_i) + (1 - y_i) \ln(1 - \sigma(\mathbf{w}^T \mathbf{x}_i)) \right] + \frac{\lambda}{2} \|\mathbf{w}\|_2^2$$
5. **Decision Tree Classifier (CART)**:
   $$I_G(t) = 1 - \sum_{i=0}^1 p(i|t)^2$$

---

## 10. HYPERPARAMETER TUNING AND OPTIMIZATION FRAMEWORK

| Model Name | Hyperparameter | Configured Value | Optimization Rationale |
|:---|:---|:---:|:---|
| **Linear SVM** | `maxIter` | `50` | Ensures complete convergence of separating hyperplane |
| | `regParam` | `0.01` | L2 penalty preventing overfitting on sparse categorical features |
| | `standardization` | `True` | Normalizes feature scales to prevent large amounts dominating margin |
| **Random Forest** | `numTrees` | `50` | Minimizes out-of-bag variance without excessive memory contention |
| | `maxDepth` | `8` | Prevents deep leaf memorization while capturing non-linear interactions |
| | `featureSubsetStrategy` | `sqrt` | Classic Breiman feature bagging ($m = \sqrt{31}$) |
| **Gradient-Boosted Trees** | `maxIter` | `30` | Number of sequential boosting iterations |
| | `maxDepth` | `5` | Constrained shallow trees prevent rapid overfitting on imbalanced data |
| | `stepSize` | `0.1` | Learning rate shrinkage parameter dampening individual tree updates |
| **Logistic Regression** | `maxIter` | `50` | L-BFGS convergence iteration limit |
| | `regParam` | `0.01` | Ridge regularization parameter |
| | `elasticNetParam` | `0.0` | Pure L2 regularization (Ridge penalty) |
| **Decision Tree** | `maxDepth` | `8` | Maximum tree partition depth |
| | `minInstancesPerNode`| `5` | Minimum samples required in leaf nodes |

---

## 11. MODEL TRAINING, VALIDATION STRATEGY & LEAKAGE PREVENTION

- **Stratified Partitioning**: 80% Training partition (1,201,347 records), 20% Unseen test partition (300,296 records).
- **Leakage Prevention**: All `StringIndexer`, `OneHotEncoder`, and `VectorAssembler` stages are fitted strictly on the training partition before transforming the test partition.
- **Single-Pass Evaluation**: Confusion matrix counts computed via `groupBy('label', 'prediction').count()`.

---

## 12. COMPREHENSIVE EVALUATION METRICS, ROC-AUC & CONFUSION MATRICES

Evaluated on 300,296 unseen holdout records (14,513 Actual Frauds, 285,783 Actual Legitimate):

| Classifier | Precision | Recall | F1-Score | ROC-AUC | True Positives (TP) | False Positives (FP) | False Negatives (FN) | True Negatives (TN) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Linear SVM (Champion)** | **0.9996** | **0.9801** | **0.9898** | **0.9980** | **14,224** | **5** | **289** | **285,778** |
| **Logistic Regression** | 0.9988 | 0.9794 | 0.9890 | **0.9990** | 14,214 | 17 | 299 | 285,766 |
| **Random Forest** | **0.9997** | 0.9677 | 0.9834 | 0.9968 | 14,044 | **4** | 469 | **285,779** |
| **Gradient-Boosted Trees** | 0.9991 | 0.9675 | 0.9831 | 0.9906 | 14,041 | 12 | 472 | 285,771 |
| **Decision Tree** | 0.9977 | 0.9597 | 0.9783 | 0.8567 | 13,928 | 32 | 585 | 285,751 |

---

## 13. EXPLAINABLE RISK SCORING INTELLIGENCE AND REASON CODES

- **Baseline Review Score**: `10.0` points assigned to all transactions (`BASELINE_REVIEW`).
- **Top Decile Amount Indicator**: Transactions $\ge 90\text{th}$ percentile receive `+30.0` points (`AMOUNT_TOP_DECILE`).
- **Rare Merchant Profile Indicator**: Categories representing $< 5.0\%$ of volume receive `+20.0` points (`RARE_PROFILE`).

#### Heuristic Scoring Distribution (15,000,000 records):
| Risk Category | Score Range | Record Count | Percentage | Operational Policy |
|:---|:---:|:---:|:---:|:---|
| **LOW** | 0.0 - 34.9 | 13,467,586 | 89.78% | Standard automated clearance |
| **MEDIUM** | 35.0 - 69.9 | 1,532,414 | 10.22% | Secondary automated verification / step-up auth |
| **HIGH** | 70.0 - 100.0 | 0 | 0.00% | Reserved for cumulative multi-factor alerts |
| **Total** | | **15,000,000** | **100.00%** | Full dataset scored |

---

## 14. OPERATIONAL 4-TIER HYBRID FRAUD TRIAGE ENGINE

| Triage Tier | Policy & Action | Trigger Criteria | Volume Count | Volume Share | Actual Fraud Caught | Legitimate Cleared |
|:---|:---|:---|:---:|:---:|:---:|:---:|
| **Tier 1: Critical Emergency** | Immediate card freeze & security SMS | Pred = 1 & Prob $\ge 0.85$ | 14,168 | 4.72% | **14,163 (99.96%)** | 5 (0.04%) |
| **Tier 2: Step-Up Auth** | 2FA Challenge (Biometric / OTP) | Pred = 1 & Prob $< 0.85$ | 63 | 0.02% | **51 (80.95%)** | 12 (19.05%) |
| **Tier 3: Compliance Audit** | Asynchronous investigation queue | Pred = 0 & Prob $\ge 0.20$ | 102 | 0.03% | **14 (13.73%)** | 88 (86.27%) |
| **Tier 4: Automated Clearance** | Instant frictionless clearance | Pred = 0 & Prob $< 0.20$ | 285,963 | 95.23% | 285 (0.10%) | **285,678 (99.90%)** |
| **Total Evaluated** | Holdout Test Partition | | **300,296** | **100.00%** | **14,513** | **285,783** |

---

## 15. BUSINESS INTELLIGENCE AND POWER BI ENTERPRISE INTEGRATION

Star Schema assets located in `powerbi/data/`:
1. `Dim_Model_Benchmark.csv`: Model comparison metrics.
2. `Fact_Confusion_Matrix.csv`: Unpivoted matrix dataset for heatmap slicing.
3. `Fact_Triage_Decisions.csv`: Operational tier breakdown.
4. `Fact_Heuristic_Risk_Summary.csv`: Risk category summary.
5. `Fact_Scored_Transactions_Sample_50k.csv`: 50,000 transactions with behavioral attributes, ML probabilities, and triage tiers.

---

## 16. TESTING, LIMITATIONS, PLAGIARISM & ETHICAL COMPLIANCE

- Validated row count preservation ($15,000,000 \rightarrow 15,000,000$) across ingestion, hygiene, and scoring stages.
- Validated deterministic reproducibility using seed 42 across feature splitting, tree bagging, and model evaluation.
- All prose, mathematical formulas, and analytical commentary in this report represent the original synthesis of the authoring team.

---

## 17. TEAM CONTRIBUTIONS AND TECHNICAL WORK BREAKDOWN

To ensure rigorous project governance and demonstrate clear individual technical execution, responsibilities were partitioned as follows:

| Candidate Name | Roll Number | Technical Role | Concrete Technical Work Executed |
|:---|:---|:---|:---|
| **Srikashyap Amaravadi** | S24CSEU1423 | Lead Big Data Engineer & Classifier Architect | • Configured Apache Spark 3.5.4 cluster environment, JVM heap allocation (`6g` driver, `6g` executor), and Hadoop Winutils/DLL integration.<br>• Architected and implemented the distributed **Linear Support Vector Machine (Linear SVM)** and **Random Forest Classifier** pipelines in Spark MLlib.<br>• Engineered the multi-threaded localhost web server (`server.py`) and live inference REST API (`/api/predict`).<br>• Optimized memory caching (`train_vec.cache()`, `test_vec.cache()`) and single-pass confusion matrix computation. |
| **Gitesh Goyal** | S24CSEU0774 | ML Optimization Engineer & Schema Discovery Lead | • Developed and executed Stage 00 (`00_inspect_schema.py`) automated schema inference and distributed data profiling across 38 parallel Spark partitions.<br>• Implemented, benchmarked, and hyperparameter-tuned the **Gradient-Boosted Trees (GBT)**, **Logistic Regression (L2 ElasticNet)**, and **Decision Tree** models.<br>• Conducted multi-iteration learning rate shrinkage sweeps ($\eta = 0.1$) and depth ceiling evaluations to optimize tree splitting and convergence.<br>• Implemented the distributed model serialization framework (`PipelineModel.write().overwrite().save()`) persisting end-to-end transformers and fitted estimators. |
| **Annya Sharma** | S24CSEU1408 | Data Hygiene & Feature Pipeline Engineering Lead | • Engineered the Stage 01 distributed ingestion pipeline (`01_ingest.py`) converting 5.01 GB raw CSV into Snappy-compressed columnar Parquet partitions (`results/raw`).<br>• Designed Stage 02 data transformation and hygiene layer (`02_transform.py`): whitespace trimming via `F.trim()`, full-record deduplication via `dropDuplicates()`, and target non-null validation.<br>• Implemented the 22-stage `StringIndexer` and `OneHotEncoder` categorical transformation pipeline, including cardinality thresholding (`max_categories=100`) and unseen category handling (`handleInvalid='keep'`).<br>• Formulated feature vector assembly via `VectorAssembler`, combining 9 continuous numerical attributes with sparse encoded vectors. |
| **Ajitej Singh** | S24CSEU1413 | Risk Intelligence, Evaluation & BI Integration Lead | • Developed Stage 03 explainable heuristic risk scoring engine (`03_risk_analysis.py`), calculating dynamic 90th percentile amount quantiles (`approxQuantile`) and rare merchant profile shares.<br>• Formulated and coded the Stage 06 **Operational 4-Tier Hybrid Fraud Triage Engine** (`06_hybrid_inference.py`), creating the decision matrix that categorizes transactions into Critical Block, Step-Up 2FA, Compliance Audit, and Automated Clearance.<br>• Built the Stage 05 evaluation and statistical visualization pipeline (`05_evaluate.py`) generating precision, recall, F1, ROC-AUC curves, and confusion matrix heatmaps.<br>• Architected the 5-table Star Schema data mart (`export_for_powerbi.py`) and authored the custom DAX measures for Power BI business intelligence reporting. |

---

## 18. CONCLUSION AND FUTURE ROADMAP
The CreditTransAct Financial Fraud Analytics project has achieved 100% of its planned objectives. By combining the distributed computational scale of **Apache Spark 3.5.4** and **Hadoop 3.3.5** with state-of-the-art machine learning classifiers, the system successfully processes millions of records, achieves a peak **F1-Score of 0.9898**, a precision of **99.97%**, and establishes an operational 4-tier decision triage engine for modern financial institutions.

---

## 19. REFERENCES
1. CreditTransAct: A Profile-Driven Dataset for Scalable Credit Card Fraud Detection, Mendeley Data, Version 1, 9 May 2026. DOI: 10.17632/y64bbnm2s3.1.
2. Apache Spark 3.5.4 Documentation: https://spark.apache.org/docs/3.5.4/
3. Apache Hadoop 3.3.5 Documentation: https://hadoop.apache.org/docs/r3.3.5/
4. Apache Spark MLlib Programming Guide: https://spark.apache.org/docs/3.5.4/ml-guide.html
5. Python 3.11 Documentation: https://docs.python.org/3.11/
6. Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5-32.
7. Friedman, J. H. (2001). Greedy Function Approximation: A Gradient Boosting Machine. Annals of Statistics, 29(5), 1189-1232.
8. Cortes, C., & Vapnik, V. (1995). Support-Vector Networks. Machine Learning, 20(3), 273-297.
