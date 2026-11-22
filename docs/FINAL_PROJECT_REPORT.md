# BENNETT UNIVERSITY
## SCHOOL OF COMPUTER SCIENCE ENGINEERING & TECHNOLOGY

# COMPREHENSIVE PROJECT IMPLEMENTATION REPORT
## SCALABLE FINANCIAL FRAUD DETECTION AND RISK INTELLIGENCE USING APACHE SPARK, HADOOP AND MACHINE LEARNING

- **Course Code**: CSET371 — Big Data Analytics and Business Intelligence
- **Faculty Guide**: Dr. Aditya Bhardwaj
- **Academic Year**: 2026

**Submitted by:**
- **Srikashyap Amaravadi** (S24CSEU1423) — *Machine Learning Model Engineering, Spark Optimization & Distributed Training*
- **Gitesh Goyal** (S24CSEU0774) — *Deep/ML Architecture Implementation, Hyperparameter Optimization & Model Validation*
- **Annya Sharma** (S24CSEU1408) — *Data Profiling, Quality Assurance, Hygiene & Feature Transformation Pipeline*
- **Ajitej Singh** (S24CSEU1413) — *Heuristic Risk Intelligence, Hybrid Triage Decision Matrix & Report Synthesis*

---

## DECLARATION OF ORIGINALITY AND PLAGIARISM COMPLIANCE
We hereby declare that this project report titled **"Scalable Financial Fraud Detection and Risk Intelligence Using Apache Spark, Hadoop and Machine Learning"** is our original work conducted under the guidance of **Dr. Aditya Bhardwaj**, School of Computer Science Engineering and Technology, Bennett University.

All methodologies, architectures, algorithms, and empirical results presented in this report were developed and executed on the designated distributed computational environment. Wherever literature, benchmarks, or third-party frameworks have been utilized, they have been comprehensively cited adhering to standard academic integrity and anti-plagiarism guidelines. No synthetic or AI-generated visual graphics have been utilized; all diagrams, confusion matrices, and metric plots were generated directly from measured system execution and deterministic mathematical visualizations.

---

## EXECUTIVE SUMMARY
Modern electronic payment infrastructures handle billions of dollars in daily transaction volume across millions of distinct accounts. While fraudulent transactions account for a minority fraction of total traffic (historically between 0.1% and 5.0%), the resulting economic losses, chargeback costs, and reputational damage to banking institutions are catastrophic. Traditional relational database management systems (RDBMS) and single-node machine learning platforms cannot scale to multi-gigabyte transaction streams without encountering prohibitive computational bottlenecks and out-of-memory (OOM) failures.

This project delivers an enterprise-grade, distributed Big Data and Machine Learning pipeline engineered using **Apache Spark 3.5.4**, **Apache Hadoop 3.3.5**, and **Python 3.11**. The platform was deployed and empirically validated on the benchmark **CreditTransAct** dataset (`credit_card_fraud.csv`), encompassing **15,000,000 transaction records across 34 feature dimensions (~5.01 GB uncompressed)**.

### Core Deliverables and Empirical Outcomes:
1. **High-Throughput Distributed Ingestion**: Converted raw 5.01 GB CSV data into snappy-compressed, columnar Apache Parquet partitions (`results/raw`), yielding an 85% compression ratio and eliminating repeated CSV parsing overheads.
2. **Deterministic Data Hygiene & Feature Preprocessing**: Implemented string normalization, deduplication, null-label validation, and isolated identifiers (`customer_id`, `transaction_id`) to strictly prevent target data leakage (`results/cleaned`).
3. **Explainable Rule-Based Heuristic Scoring**: Developed an auditable heuristic risk scoring engine evaluating empirical 90th percentile amount spikes (`AMOUNT_TOP_DECILE`) and rare merchant category profiles (`RARE_PROFILE`) across all 15 million transactions (`results/risk_scored`).
4. **Distributed MLlib Model Benchmark & Hyperparameter Tuning**: Evaluated 5 distributed machine learning and deep learning algorithms on 1.5 million in-scope transactions: **Linear Support Vector Machine (Linear SVM), Random Forest, Gradient-Boosted Trees (GBT), Logistic Regression, and Decision Tree**.
   - **Champion Model — Linear SVM**: Achieved an **F1-Score of 0.9898**, **Recall of 98.01%**, and an **ROC-AUC of 0.9980** on an unseen holdout partition of 300,296 records.
   - **Precision Leader — Random Forest**: Achieved **99.97% Precision**, recording only **4 false alarms** across 285,783 legitimate transactions.
5. **Operational 4-Tier Hybrid Triage Engine**: Formulated an actionable operational policy matrix merging model probabilities with heuristic risk constraints:
   - **Tier 1 (Critical Emergency)**: 14,168 transactions flagged — **14,163 actual frauds halted instantly (99.96% accuracy)**.
   - **Tier 4 (Automated Clearance)**: **95.23% of all transactions (285,963 records)** cleared with zero friction and sub-millisecond latency.
6. **Enterprise Business Intelligence (BI) Integration**: Exported a Star Schema data mart comprising 5 normalized tables with custom DAX measures for instant deployment into **Microsoft Power BI**.

---

## CHAPTER 1: INTRODUCTION & PROPOSED METHODOLOGY

### 1.1 Context and Problem Statement
Financial fraud in digital payment networks presents severe computational and statistical challenges:
- **Massive Computational Scale**: Processing 15 million transaction records with 34 features entails handling hundreds of millions of data points, overwhelming single-machine pandas/scikit-learn workflows.
- **Extreme Class Imbalance**: Genuine transactions drastically outnumber fraudulent events (~95.10% legitimate vs. ~4.90% fraud). Naive classification algorithms biased toward the majority class achieve high nominal accuracy while failing to detect critical fraud occurrences.
- **Strict Latency and Explainability Requirements**: Banking regulations mandate that automated systems provide explainable audit trails (reason codes) rather than uninterpretable black-box decisions, without adding latency to customer checkouts.

### 1.2 Proposed Methodology Architecture
To address these challenges, the team engineered a multi-stage distributed processing and machine learning pipeline. The architecture decouples storage, batch feature transformation, heuristic explainability, model training, and operational inference into distinct layers.

```
+-----------------------------------------------------------------------------+
|                      PROPOSED METHODOLOGY ARCHITECTURE                      |
+-----------------------------------------------------------------------------+
|  1. RAW DATA SOURCE                                                         |
|     CreditTransAct Benchmark | 15,000,000 Rows | 34 Features (~5.01 GB)     |
+--------------------------------------v--------------------------------------+
|  2. DISTRIBUTED INGESTION LAYER (pipeline/01_ingest.py)                     |
|     PySpark CSV Reader -> Schema Discovery -> Snappy Parquet (results/raw)   |
+--------------------------------------v--------------------------------------+
|  3. DATA PREPROCESSING & HYGIENE LAYER (pipeline/02_transform.py)           |
|     String Trimming -> Deduplication -> Null Safety -> Leakage Isolation    |
+-------------------+----------------------------------+----------------------+
                    |                                  |
                    v                                  v
+-----------------------------------+  +--------------------------------------+
| 4. HEURISTIC RISK ENGINE          |  | 5. FEATURE ENGINEERING PIPELINE      |
|    (pipeline/03_risk_analysis.py) |  |    (pipeline/04_train_models.py)     |
|    - Baseline Score: 10 pts       |  |    - 22 StringIndexer stages         |
|    - 90th Pct Amount: +30 pts     |  |    - 22 OneHotEncoder stages         |
|    - Rare Profile: +20 pts        |  |    - 9 Numeric VectorAssembler       |
|    - Bands: LOW / MEDIUM / HIGH   |  |    - 80/20 Stratified Partitioning   |
+-------------------+---------------+  +-------------------+------------------+
                    |                                      |
                    |                                      v
                    |                  +--------------------------------------+
                    |                  | 6. DISTRIBUTED MODEL TRAINING        |
                    |                  |    - Linear SVM (Champion)           |
                    |                  |    - Random Forest (50 Trees)        |
                    |                  |    - Gradient-Boosted Trees (GBT)    |
                    |                  |    - Logistic Regression (L2 Reg)    |
                    |                  |    - Decision Tree Classifier        |
                    |                  +-------------------+------------------+
                    |                                      |
                    |                                      v
                    |                  +--------------------------------------+
                    |                  | 7. EVALUATION & BENCHMARKING         |
                    |                  |    (pipeline/05_evaluate.py)         |
                    |                  |    - Precision, Recall, F1, ROC-AUC  |
                    |                  |    - 5 Confusion Matrix Heatmaps     |
                    |                  +-------------------+------------------+
                    |                                      |
                    +-------------------+------------------+
                                        v
+-----------------------------------------------------------------------------+
| 8. HYBRID OPERATIONAL FRAUD TRIAGE ENGINE (pipeline/06_hybrid_inference.py) |
|    - Tier 1: Critical Emergency (Block & Alert: p >= 0.85) -> 97.59% Caught |
|    - Tier 2: Step-Up Auth (2FA Challenge: 0.35 <= p < 0.85)                 |
|    - Tier 3: Compliance Audit (Offline Queue: p >= 0.20)                    |
|    - Tier 4: Automated Clearance (Frictionless: p < 0.20) -> 95.23% Cleared |
+-----------------------------------------------------------------------------+
```

---

## CHAPTER 2: THEORETICAL FOUNDATION & BIG DATA DISTRIBUTED FRAMEWORK

### 2.1 Apache Spark 3.5.4 Distributed Execution Architecture
Apache Spark provides a distributed general-purpose cluster-computing framework built around Resilient Distributed Datasets (RDDs) and the Catalyst Query Optimizer. The runtime model operates under a Driver-Executor topology:
- **Driver Node**: Manages the `SparkSession`, translates high-level PySpark code into a Directed Acyclic Graph (DAG) of logical execution stages, optimizes execution plans via the Catalyst optimizer, and schedules tasks across executor cores.
- **Executors**: Background worker JVM processes allocated with dedicated heap memory (`spark.driver.memory=6g`, `spark.executor.memory=6g`) executing task partitions concurrently across 16 logical cores.
- **Tungsten Execution Engine**: Manages memory off-heap directly in raw binary format, eliminating JVM garbage collection overhead and leveraging hardware-level CPU cache locality.

### 2.2 Storage Optimization: CSV vs. Snappy-Compressed Columnar Parquet
Reading raw uncompressed CSV requires intensive CPU overhead on every execution because:
1. Every numeric value must be parsed from ASCII strings into binary float/integer representations.
2. In relational queries selecting only a subset of features (e.g., amount, merchant category, label), the execution engine must perform full row-by-row disk reads across the entire 5.01 GB file.
3. CSV provides zero native schema metadata, requiring expensive schema inference passes (`inferSchema=true`).

In contrast, **Apache Parquet** delivers:
- **Columnar Layout**: Data is organized by column rather than row. When computing feature subsets, entire blocks of irrelevant columns are skipped on disk (I/O pruning).
- **Dictionary & Bit-Packed Encoding**: Categorical attributes with repetitive string values (e.g., merchant categories, transaction types) are stored as compact integer indices.
- **Snappy Compression**: High-throughput compression codec offering rapid decompression speeds with minimal CPU overhead, reducing the storage footprint from 5.01 GB to ~450 MB (an 85% storage reduction).
- **Embedded Statistics**: Parquet file footers maintain column-level min/max statistics, enabling dictionary pruning before partitions are loaded into memory.

---

## CHAPTER 3: DATASET SPECIFICATION, PROFILING & PREPROCESSING METHODOLOGY

### 3.1 CreditTransAct Dataset Profiling
The system was validated on the full **CreditTransAct** dataset (`credit_card_fraud.csv`), characterized as follows:
- **Total Records**: 15,000,000 transactions.
- **Total Feature Dimensions**: 34 columns.
- **Class Label**: `is_fraud` (Binary: 0 = Legitimate, 1 = Fraudulent).
- **Target Distribution**:
  - Legitimate (0): **14,264,776 transactions (95.10%)**
  - Fraudulent (1): **735,224 transactions (4.90%)**
  - Missing Label Entries: **0 (100% complete)**

### 3.2 Feature Taxonomy & Isolation
Attributes are partitioned into three functional categories:
1. **Isolated Identifiers (Target Leakage Elimination)**:
   - `customer_id`: Unique alphanumeric customer token.
   - `transaction_id`: Unique transaction identifier.
   *Methodology*: Explicitly excluded via `exclude_columns` in `project_config.json`. Retaining customer or transaction IDs allows tree models to memorize specific individuals rather than generalizable behavioral patterns.
2. **Continuous Numerical Features (9 Attributes)**:
   - `transaction_amount`: Transaction currency value.
   - `avg_amount_deviation_sigma`: Standard deviation deviation from customer historical mean.
   - `geo_velocity_kmh`: Calculated physical velocity between consecutive transactions.
   - `geo_distance_km`: Spatial distance between terminal location and cardholder home address.
   - `session_duration_sec`: Duration of the checkout interaction session.
   - `cards_on_device_30d`: Count of distinct payment cards associated with the device in 30 days.
   - `failed_attempts_before_success`: Unsuccessful PIN/CVV entry attempts prior to approval.
   - `account_age_days`: Age of the customer banking account in days.
   - `chargeback_history_count`: Cumulative lifetime chargeback disputes logged.
3. **Categorical Behavioral Features (22 Attributes)**:
   - `transaction_amount_bin`, `merchant_category`, `merchant_risk_score`, `merchant_category_vs_history`, `geo_velocity_bin`, `geo_distance_bin`, `merchant_location`, `country_consistency`, `ip_address_type`, `device_fingerprint_match`, `session_duration_bin`, `network_carrier_type`, `cvv_match_status`, `three_ds_auth_result`, `tokenization_used`, `transaction_velocity_1h`, `time_of_transaction`, `account_credential_change_recency`, `card_present_cnp`, `order_shipping_speed`, `segment`, `customer_type`.

### 3.3 Detailed Preprocessing Steps
The data preparation methodology follows four rigorous, deterministic steps:
- **Step 1: Whitespace Sanitation & Type Normalization**: Iterates through all string fields applying `F.trim()` to eliminate leading/trailing whitespace variations that cause false categorical splits.
- **Step 2: Deduplication & Null Validation**: Evaluates full-row deduplication across all 34 attributes via `df.dropDuplicates()`, followed by strict null-safety filtering (`filter(F.col('label').isNotNull())`).
- **Step 3: Cardinality Thresholding & StringIndexing**: For each categorical attribute, distinct cardinality is verified against `max_categories=100`. Features with distinct counts $\le 100$ are indexed via `StringIndexer(inputCol=c, outputCol=idx_c, handleInvalid='keep')`, mapping distinct strings to integer frequency ranks ($0, 1, \dots, k-1$). Unseen categories in test partitions are routed to a dedicated bucket index via `handleInvalid='keep'`.
- **Step 4: One-Hot Encoding & Vector Assembly**: Indexed features are transformed into sparse binary vectors via `OneHotEncoder(inputCols=idx_cols, outputCols=ohe_cols, handleInvalid='keep')`. Continuous numericals and sparse one-hot encoded vectors are concatenated into a single unified vector column via `VectorAssembler(inputCols=numeric + ohe_cols, outputCol='features')`.

---

## CHAPTER 4: DISTRIBUTED MACHINE LEARNING IMPLEMENTATION & HYPERPARAMETER TUNING

*(Engineered and Validated by Srikashyap Amaravadi and Gitesh Goyal)*

### 4.1 Algorithms Evaluated
To provide comprehensive benchmarking across linear, margin-maximizing, and ensemble tree architectures, 5 distributed algorithms from **Spark MLlib** were implemented:

1. **Linear Support Vector Machine (LinearSVC)**:
   - Formulates maximum-margin hyperplane separation:
     $$\min_{\mathbf{w}, b} \frac{1}{2}\|\mathbf{w}\|^2 + C \sum_{i=1}^N \max\left(0, 1 - y_i(\mathbf{w}^T \mathbf{x}_i + b)\right)$$
   - Solved via Accelerated Gradient Descent (L-BFGS).

2. **Random Forest Classifier**:
   - Bagging ensemble constructing $B = 50$ independent randomized decision trees:
     $$\hat{y} = \text{mode}\left\{T_1(\mathbf{x}), T_2(\mathbf{x}), \dots, T_{50}(\mathbf{x})\right\}$$
   - Evaluates a random feature subset of size $m = \sqrt{p}$ at each split candidate, reducing correlation among trees.

3. **Gradient-Boosted Trees (GBT)**:
   - Sequential boosting optimizing binomial log-likelihood loss by iteratively fitting trees to pseudo-residuals:
     $$F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \eta \sum_{j=1}^{J_m} \gamma_{jm} I(\mathbf{x} \in R_{jm})$$

4. **Logistic Regression with ElasticNet (L2 Regularization)**:
   - Calibrated probabilistic classification optimizing log-loss with Ridge penalty:
     $$\mathcal{L}(\mathbf{w}) = -\frac{1}{N}\sum_{i=1}^N \left[ y_i \ln \sigma(\mathbf{w}^T \mathbf{x}_i) + (1 - y_i) \ln(1 - \sigma(\mathbf{w}^T \mathbf{x}_i)) \right] + \frac{\lambda}{2} \|\mathbf{w}\|_2^2$$

5. **Decision Tree Classifier (CART)**:
   - Rule-based binary partitioner maximizing Gini impurity reduction:
     $$I_G(t) = 1 - \sum_{i=0}^1 p(i|t)^2$$

### 4.2 Hyperparameter Tuning Specifications
Tuning parameters were established based on distributed cross-validation sweeps balancing variance, bias, and execution runtime:

| Classifier | Hyperparameter | Configured Value | Tuning Rationale |
|:---|:---|:---:|:---|
| **Linear SVM** | `maxIter` | `50` | Ensures complete convergence of margin hyperplane |
| | `regParam` ($\lambda$) | `0.01` | L2 penalty preventing overfitting on sparse categorical features |
| | `standardization` | `True` | Normalizes feature scales to prevent large amounts dominating margin |
| | `tol` | `1e-6` | Stopping tolerance criterion |
| **Random Forest** | `numTrees` | `50` | Minimizes out-of-bag variance without excessive memory contention |
| | `maxDepth` | `8` | Prevents deep leaf memorization while capturing non-linear interactions |
| | `featureSubsetStrategy` | `sqrt` | Classic Breiman feature bagging ($m = \sqrt{31}$) |
| | `impurity` | `gini` | Standard node split purity metric |
| **Gradient-Boosted Trees** | `maxIter` | `30` | Number of sequential boosting iterations |
| | `maxDepth` | `5` | Constrained shallow trees prevent rapid overfitting on imbalanced data |
| | `stepSize` ($\eta$) | `0.1` | Learning rate shrinkage parameter dampening individual tree updates |
| | `lossType` | `logistic` | Binomial log-likelihood for binary classification |
| **Logistic Regression** | `maxIter` | `50` | L-BFGS convergence iteration limit |
| | `regParam` | `0.01` | Ridge regularization parameter |
| | `elasticNetParam` | `0.0` | Pure L2 regularization (Ridge penalty) |
| | `threshold` | `0.50` | Base classification decision threshold |
| **Decision Tree** | `maxDepth` | `8` | Maximum tree partition depth |
| | `minInstancesPerNode`| `5` | Minimum samples required in leaf nodes |
| | `maxBins` | `32` | Discretization bin count for continuous features |

---

## CHAPTER 5: EMPIRICAL RESULTS, CONFUSION MATRICES & BENCHMARK ANALYSIS

### 5.1 Experimental Setup
- **Dataset Partitioning**: 80% Training partition (1,201,347 transactions), 20% Unseen holdout test partition (300,296 transactions).
- **Test Class Ground Truth**: 14,513 Actual Frauds (~4.83%), 285,783 Actual Legitimate (~95.17%).

### 5.2 Comprehensive Benchmark Performance Metrics

| Classifier | Precision | Recall | F1-Score | ROC-AUC | True Positives (TP) | False Positives (FP) | False Negatives (FN) | True Negatives (TN) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Linear SVM** *(Champion)* | **0.9996** | **0.9801** | **0.9898** | **0.9980** | **14,224** | **5** | **289** | **285,778** |
| **Logistic Regression** | 0.9988 | 0.9794 | 0.9890 | **0.9990** | 14,214 | 17 | 299 | 285,766 |
| **Random Forest** | **0.9997** | 0.9677 | 0.9834 | 0.9968 | 14,044 | **4** | 469 | **285,779** |
| **Gradient-Boosted Trees (GBT)**| 0.9991 | 0.9675 | 0.9831 | 0.9906 | 14,041 | 12 | 472 | 285,771 |
| **Decision Tree** | 0.9977 | 0.9597 | 0.9783 | 0.8567 | 13,928 | 32 | 585 | 285,751 |

### 5.3 Comparative Analysis & Key Findings
1. **Linear SVM Superiority**: Linear SVM emerged as the champion classifier, achieving an **F1-Score of 0.9898** and the highest **Recall of 98.01%**. It caught 14,224 out of 14,513 fraud occurrences, misidentifying only 5 legitimate transactions out of 285,783.
2. **False Positive Minimization**: In banking operations, false alarms cause customer friction and account abandonment. **Random Forest** achieved the lowest false positive tally (**4 false alarms**), delivering an exceptional Precision of **99.97%**.
3. **Linear Separability**: Both Linear SVM (AUC 0.9980) and Logistic Regression (AUC 0.9990) achieved near-perfect area under the ROC curve. This proves that high-dimensional one-hot expansion creates linear separability between fraudulent and legitimate clusters.

---

## CHAPTER 6: EXPLAINABLE HEURISTIC RISK SCORING & HYBRID TRIAGE ENGINE

*(Engineered by Annya Sharma and Ajitej Singh)*

### 6.1 Multi-Component Heuristic Scoring Engine
Stage 03 (`pipeline/03_risk_analysis.py`) formulates an explainable, auditable heuristic scoring engine:
- **Baseline Allocation**: Every transaction receives `10.0` points (`BASELINE_REVIEW`).
- **Empirical Amount Quantile Threshold**: Evaluates `approxQuantile('transaction_amount', [0.90], 0.01)`. Transactions exceeding the 90th percentile threshold receive `+30.0` points (`AMOUNT_TOP_DECILE`).
- **Rare Profile Anomaly**: Computes merchant category transaction shares. Categories representing $< 5.0\%$ of transaction volume receive `+20.0` points (`RARE_PROFILE`).
- **Score Cap**: Score is capped at `100.0` points.

#### Heuristic Scoring Distribution (15,000,000 Transactions Scored):
| Risk Category | Score Range | Record Count | Percentage | Operational Policy |
|:---|:---:|:---:|:---:|:---|
| **LOW** | 0.0 - 34.9 | 13,467,586 | 89.78% | Standard automated clearance |
| **MEDIUM** | 35.0 - 69.9 | 1,532,414 | 10.22% | Triage queue / secondary authentication |
| **HIGH** | 70.0 - 100.0 | 0 | 0.00% | Reserved for compounding multi-factor triggers |
| **Total** | | **15,000,000** | **100.00%** | Full dataset scored |

### 6.2 Operational 4-Tier Hybrid Triage Decision Matrix
Stage 06 (`pipeline/06_hybrid_inference.py`) combines machine learning predicted probabilities with rule-based heuristic constraints to route transactions into specialized banking queues:

| Triage Tier | Policy & Action | Trigger Criteria | Volume Count | Volume Share | Actual Fraud Caught | Legitimate Cleared |
|:---|:---|:---|:---:|:---:|:---:|:---:|
| **Tier 1: Critical Emergency** | Immediate card freeze & security SMS | Pred = 1 & Prob $\ge 0.85$ | 14,168 | 4.72% | **14,163 (99.96%)** | 5 (0.04%) |
| **Tier 2: Step-Up Auth** | 2FA Challenge (Biometric / OTP) | Pred = 1 & Prob $< 0.85$ | 63 | 0.02% | **51 (80.95%)** | 12 (19.05%) |
| **Tier 3: Compliance Audit** | Asynchronous investigation queue | Pred = 0 & Prob $\ge 0.20$ | 102 | 0.03% | **14 (13.73%)** | 88 (86.27%) |
| **Tier 4: Automated Clearance** | Instant frictionless clearance | Pred = 0 & Prob $< 0.20$ | 285,963 | 95.23% | 285 (0.10%) | **285,678 (99.90%)** |
| **Total Evaluated** | Holdout Test Partition | | **300,296** | **100.00%** | **14,513** | **285,783** |

---

## CHAPTER 7: BUSINESS INTELLIGENCE & POWER BI INTEGRATION

### 7.1 Star Schema Data Mart
To support executive oversight, `export_for_powerbi.py` transforms the Spark layers into a 5-table Star Schema:
1. `Dim_Model_Benchmark.csv`: Model comparison metrics.
2. `Fact_Confusion_Matrix.csv`: Unpivoted matrix dataset for heatmap slicing.
3. `Fact_Triage_Decisions.csv`: Operational tier breakdown.
4. `Fact_Heuristic_Risk_Summary.csv`: Risk category summary.
5. `Fact_Scored_Transactions_Sample_50k.csv`: 50,000 transactions with behavioral attributes, ML probabilities, and triage tiers.

---

## CHAPTER 8: TESTING, LIMITATIONS & PLAGIARISM / ETHICS COMPLIANCE

### 8.1 Verification and Testing
- Verified Spark worker socket connectivity on Windows with Microsoft OpenJDK 17 and Python 3.11.
- Validated row count preservation ($15,000,000 \rightarrow 15,000,000$) across ingestion, hygiene, and scoring stages.
- Validated deterministic reproducibility using seed 42 across feature splitting, tree bagging, and model evaluation.

### 8.2 Academic Integrity & Plagiarism Statement
All prose, mathematical formulas, and analytical commentary in this report represent the original synthesis of the authoring team. Direct citations are provided for the CreditTransAct benchmark dataset, Apache Spark documentation, and relevant machine learning algorithms.

---

## CHAPTER 9: TEAM CONTRIBUTIONS AND GOVERNANCE

In alignment with project directives:

| Candidate Name | Roll Number | Specific Responsibilities & Deliverables |
|:---|:---|:---|
| **Srikashyap Amaravadi** | S24CSEU1423 | Architecture design, PySpark session tuning, Linear SVM / Random Forest implementation, full-stack server development (`server.py`) |
| **Gitesh Goyal** | S24CSEU0774 | Deep/ML model validation (GBT, Logistic Regression, Decision Tree), hyperparameter optimization, schema discovery (`00_inspect_schema.py`) |
| **Annya Sharma** | S24CSEU1408 | End-to-end data preprocessing, missing value analysis, feature engineering pipeline (`02_transform.py`, `StringIndexer`, `OneHotEncoder`), data hygiene |
| **Ajitej Singh** | S24CSEU1413 | Heuristic risk engine (`03_risk_analysis.py`), operational hybrid triage engine (`06_hybrid_inference.py`), Power BI modeling, report synthesis |

---

## REFERENCES
1. CreditTransAct: A Profile-Driven Dataset for Scalable Credit Card Fraud Detection, Mendeley Data, Version 1, 9 May 2026. DOI: 10.17632/y64bbnm2s3.1.
2. Apache Spark 3.5.4 Documentation: https://spark.apache.org/docs/3.5.4/
3. Apache Hadoop 3.3.5 Documentation: https://hadoop.apache.org/docs/r3.3.5/
4. Apache Spark MLlib Programming Guide: https://spark.apache.org/docs/3.5.4/ml-guide.html
5. Python 3.11 Documentation: https://docs.python.org/3.11/
6. Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5-32.
7. Friedman, J. H. (2001). Greedy Function Approximation: A Gradient Boosting Machine. Annals of Statistics, 29(5), 1189-1232.
8. Cortes, C., & Vapnik, V. (1995). Support-Vector Networks. Machine Learning, 20(3), 273-297.
