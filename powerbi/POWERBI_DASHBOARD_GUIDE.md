# Power BI Financial Fraud Analytics Dashboard Setup Guide

This guide enables you to build a professional Power BI Dashboard for **CreditTransAct Scalable Fraud Detection and Risk Intelligence** in under 5 minutes.

All data assets are pre-modeled, aggregated, and ready in:
`credittransact-fraud-analytics/powerbi/data/`

---

## 1. Data Assets Available for Power BI

| File Name | Role in Power BI | Records | Key Columns |
|:---|:---|:---:|:---|
| **`Dim_Model_Benchmark.csv`** | Dimension Table | 5 Models | `model`, `precision`, `recall`, `f1`, `roc_auc`, `Precision_Pct`, `Recall_Pct`, `F1_Pct`, `ROC_AUC_Pct`, `tp`, `fp`, `fn`, `tn` |
| **`Fact_Confusion_Matrix.csv`** | Fact / Matrix Table | 20 Rows | `Model`, `Actual_Class`, `Predicted_Class`, `Count`, `Type` |
| **`Fact_Triage_Decisions.csv`** | Fact Table | 8 Rows | `triage_action`, `Actual_Fraud_Label`, `Class_Count`, `Total_Tier_Volume`, `percentage`, `Fraud_Status` |
| **`Fact_Heuristic_Risk_Summary.csv`** | Dimension Table | 3 Rows | `risk_category`, `count`, `Percentage_Share` |
| **`Fact_Scored_Transactions_Sample_50k.csv`** | Transaction Fact Table | 50,000 Txns | `transaction_id`, `customer_id`, `transaction_amount`, `merchant_category`, `geo_velocity_kmh`, `ML_Fraud_Probability`, `ML_Predicted_Label`, `Operational_Triage_Tier`, `Classification_Outcome`, `is_fraud` |

---

## 2. Step-by-Step Power BI Setup

### Step 1: Open Power BI Desktop or Power BI Online
1. Launch **Microsoft Power BI Desktop** (or go to [app.powerbi.com](https://app.powerbi.com)).
2. Click **Get Data** -> **Text/CSV**.
3. Select the folder `credittransact-fraud-analytics/powerbi/data/`.
4. Import all 5 CSV files:
   - `Dim_Model_Benchmark.csv`
   - `Fact_Confusion_Matrix.csv`
   - `Fact_Triage_Decisions.csv`
   - `Fact_Heuristic_Risk_Summary.csv`
   - `Fact_Scored_Transactions_Sample_50k.csv`
5. Click **Load**.

---

### Step 2: Relationships & Data Model
In the **Model View** (left pane):
- Link `Dim_Model_Benchmark[model]` (1) to `Fact_Confusion_Matrix[Model]` (*) (Single direction).
- Other tables are independent dimensional or summary cubes ready for slicers.

---

### Step 3: Add Essential DAX Measures
Create a new measure table or add these measures to `Fact_Scored_Transactions_Sample_50k`:

```dax
// 1. Total Scored Transactions
Total Transactions = COUNTROWS('Fact_Scored_Transactions_Sample_50k')

// 2. Total Actual Fraud Events
Actual Fraud Count = CALCULATE(
    COUNTROWS('Fact_Scored_Transactions_Sample_50k'),
    'Fact_Scored_Transactions_Sample_50k'[is_fraud] = 1
)

// 3. Fraud Caught (True Positives)
Fraud Intercepted Count = CALCULATE(
    COUNTROWS('Fact_Scored_Transactions_Sample_50k'),
    'Fact_Scored_Transactions_Sample_50k'[Classification_Outcome] = "True Positive (Fraud Caught)"
)

// 4. Fraud Detection Rate (Recall)
Fraud Detection Rate = DIVIDE([Fraud Intercepted Count], [Actual Fraud Count], 0)

// 5. False Alarm Rate (False Positive Rate)
False Alarm Rate = DIVIDE(
    CALCULATE(COUNTROWS('Fact_Scored_Transactions_Sample_50k'), 'Fact_Scored_Transactions_Sample_50k'[Classification_Outcome] = "False Positive (False Alarm)"),
    CALCULATE(COUNTROWS('Fact_Scored_Transactions_Sample_50k'), 'Fact_Scored_Transactions_Sample_50k'[is_fraud] = 0),
    0
)

// 6. Dollar Value Fraud Loss Prevented
Fraud Loss Prevented = CALCULATE(
    SUM('Fact_Scored_Transactions_Sample_50k'[transaction_amount]),
    'Fact_Scored_Transactions_Sample_50k'[Classification_Outcome] = "True Positive (Fraud Caught)"
)

// 7. Instant Clearance Rate (Frictionless Traffic)
Automated Clearance Share = DIVIDE(
    CALCULATE(COUNTROWS('Fact_Scored_Transactions_Sample_50k'), 'Fact_Scored_Transactions_Sample_50k'[Operational_Triage_Tier] = "Tier 4: Automated Clearance"),
    [Total Transactions],
    0
)
```

---

## 3. Recommended Dashboard Layout (2 Pages)

### Page 1: Executive Fraud Operations & Hybrid Triage
- **Top KPI Cards**:
  - `Total Transactions`: 15,000,000 (Subtext: Ingested & Cleaned)
  - `Fraud Detection Rate`: **98.01%**
  - `False Alarm Rate`: **0.002%**
  - `Instant Automated Clearance`: **95.23%**
  - `Fraud Loss Prevented`: Total Currency Value
- **Visual 1 (Donut Chart)**:
  - Legend: `Operational_Triage_Tier`
  - Values: `Count of transaction_id`
  - *Shows Tier 4 (95.23%), Tier 1 (4.72%), Tier 3 (0.03%), Tier 2 (0.02%)*
- **Visual 2 (Bar Chart)**:
  - X-Axis: `merchant_category`
  - Y-Axis: `Fraud Intercepted Count`
  - Tooltip: `Average transaction_amount`
- **Visual 3 (Table / Matrix Visual)**:
  - Rows: `Operational_Triage_Tier`
  - Columns: `Classification_Outcome`
  - Values: `Count` and `Sum of transaction_amount`
- **Slicers**:
  - `merchant_category`
  - `card_present_cnp`
  - `Operational_Triage_Tier`

### Page 2: Machine Learning Model Benchmarking
- **Visual 1 (Clustered Column Chart)**:
  - X-Axis: `model` (from `Dim_Model_Benchmark`)
  - Y-Axis: `F1_Pct`, `Precision_Pct`, `Recall_Pct`, `ROC_AUC_Pct`
- **Visual 2 (Matrix Visual - Confusion Matrix Heatmap)**:
  - Rows: `Actual_Class`
  - Columns: `Predicted_Class`
  - Values: `Count`
  - Filter: Model Slicer (`Linear SVM`, `Random Forest`, `Logistic Regression`, `GBT`, `Decision Tree`)
- **Visual 3 (Scatter Plot - Precision vs Recall)**:
  - X-Axis: `Recall_Pct`
  - Y-Axis: `Precision_Pct`
  - Details: `model`
  - Bubble Size: `Total_Evaluated`

---

## 4. Verification Check
- All data tables are exported as UTF-8 CSVs without null values.
- Formatted percentages and integer counts match the official Milestone Report and Word Document.
