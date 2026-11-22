import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure matplotlib writable temp cache
os.environ['MPLCONFIGDIR'] = str(Path(__file__).resolve().parent / 'results' / '.matplotlib')

PLOTS_DIR = Path(__file__).resolve().parent / 'results' / 'plots'
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

NAVY = '#1B365D'
LIGHT_BLUE = '#EBF3FA'
BORDER_BLUE = '#2A4D7E'
AMBER = '#D97706'
GREEN = '#059669'
PURPLE = '#7C3AED'
DARK = '#1E293B'

def draw_methodology_architecture():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=220)
    ax.axis('off')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.5)

    # Title
    ax.text(7, 8.1, "CreditTransAct: Proposed Scalable Financial Fraud Analytics Methodology",
            ha='center', va='center', fontsize=14, fontweight='bold', color=NAVY)
    ax.text(7, 7.7, "Distributed Ingestion, Hybrid Risk Intelligence & Machine Learning Architecture",
            ha='center', va='center', fontsize=10, style='italic', color='#64748B')

    # Draw Boxes
    def add_box(x, y, w, h, title, items, bg_col, border_col):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor=bg_col, edgecolor=border_col, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.35, title, ha='center', va='center', fontsize=10, fontweight='bold', color=border_col)
        
        y_text = y + h - 0.75
        for item in items:
            ax.text(x + 0.25, y_text, f"• {item}", ha='left', va='center', fontsize=8.2, color=DARK)
            y_text -= 0.32

    # Layer 1: Data Source
    add_box(0.5, 4.8, 2.6, 2.4, "1. Raw Data Source", 
            ["CreditTransAct Benchmark", "15,000,000 Transactions", "~5.01 GB Uncompressed CSV", "34 Feature Attributes", "4.90% Fraud Prevalence"],
            "#F8FAFC", NAVY)

    # Layer 2: Ingestion & Storage
    add_box(3.6, 4.8, 2.8, 2.4, "2. Distributed Ingestion", 
            ["PySpark CSV Reader", "Schema Discovery (00)", "Snappy Parquet Layer", "Columnar Storage (results/raw)", "Eliminates Parsing Bottleneck"],
            LIGHT_BLUE, BORDER_BLUE)

    # Layer 3: Preprocessing & Hygiene
    add_box(6.9, 4.8, 3.1, 2.4, "3. Data Hygiene & Cleaning", 
            ["Whitespace Trimming (F.trim)", "Deduplication (dropDuplicates)", "Target Leakage Isolation", "Zero Null Target Validation", "Output: results/cleaned/"],
            "#ECFDF5", GREEN)

    # Layer 4: Heuristic Scoring
    add_box(10.5, 4.8, 3.0, 2.4, "4. Heuristic Risk Engine", 
            ["Baseline Score: 10 pts", "90th Percentile Amt: +30 pts", "Rare Merchant Share: +20 pts", "Score Bands (LOW/MED/HIGH)", "Output: results/risk_scored/"],
            "#FFFBEB", AMBER)

    # Layer 5: Feature Engineering
    add_box(1.5, 1.2, 3.2, 2.6, "5. Distributed Feature Pipeline", 
            ["Categorical Separation (22 features)", "StringIndexer (Ordinal mapping)", "OneHotEncoder (Sparse vectors)", "VectorAssembler (31 predictors)", "80/20 Stratified Partitioning"],
            LIGHT_BLUE, BORDER_BLUE)

    # Layer 6: Distributed Model Training
    add_box(5.3, 1.2, 3.4, 2.6, "6. Machine Learning Models", 
            ["Linear Support Vector Machine", "Random Forest (50 trees, maxDepth 8)", "Gradient-Boosted Trees (GBT)", "Logistic Regression (L2 Reg)", "Decision Tree Classifier"],
            "#F5F3FF", PURPLE)

    # Layer 7: Evaluation & Hybrid Triage
    add_box(9.3, 1.2, 3.7, 2.6, "7. Evaluation & Hybrid Triage", 
            ["Confusion Matrix & ROC-AUC", "Precision, Recall, F1 Metrics", "Tier 1: Instant Block (p >= 0.85)", "Tier 2: Step-Up 2FA Challenge", "Tier 4: Automated Clearance (95.2%)"],
            "#FEF2F2", '#DC2626')

    # Connecting Arrows
    arrow_props = dict(arrowstyle="->", lw=2, color=NAVY, shrinkA=5, shrinkB=5)
    
    # Horizontal top arrows
    ax.annotate("", xy=(3.6, 6.0), xytext=(3.1, 6.0), arrowprops=arrow_props)
    ax.annotate("", xy=(6.9, 6.0), xytext=(6.4, 6.0), arrowprops=arrow_props)
    ax.annotate("", xy=(10.5, 6.0), xytext=(10.0, 6.0), arrowprops=arrow_props)

    # Downward arrow from Cleaning to Feature Pipeline
    ax.annotate("", xy=(3.1, 3.8), xytext=(8.0, 4.8),
                arrowprops=dict(arrowstyle="->", lw=2, color=NAVY, connectionstyle="arc3,rad=-0.2"))

    # Bottom horizontal arrows
    ax.annotate("", xy=(5.3, 2.5), xytext=(4.7, 2.5), arrowprops=arrow_props)
    ax.annotate("", xy=(9.3, 2.5), xytext=(8.7, 2.5), arrowprops=arrow_props)

    # Downward arrow from Heuristic to Hybrid Triage
    ax.annotate("", xy=(11.5, 3.8), xytext=(11.8, 4.8),
                arrowprops=dict(arrowstyle="->", lw=2, color=AMBER, connectionstyle="arc3,rad=0.1"))

    plt.tight_layout()
    out_path = PLOTS_DIR / 'methodology_architecture.png'
    plt.savefig(out_path, dpi=220)
    plt.close()
    print(f"[+] Generated: {out_path}")

def draw_preprocessing_workflow():
    fig, ax = plt.subplots(figsize=(13, 6.5), dpi=220)
    ax.axis('off')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.5)

    ax.text(6.5, 6.1, "Step-by-Step Data Preprocessing and Feature Engineering Methodology",
            ha='center', va='center', fontsize=13, fontweight='bold', color=NAVY)
    ax.text(6.5, 5.7, "Strict Isolation, Cardinality Thresholding, and Distributed Vector Assembly",
            ha='center', va='center', fontsize=9.5, style='italic', color='#64748B')

    def add_step(x, y, w, h, step_num, title, items, bg_col, border_col):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor=bg_col, edgecolor=border_col, linewidth=1.6)
        ax.add_patch(rect)
        # Step circle
        circle = patches.Circle((x + 0.35, y + h - 0.4), 0.22, facecolor=border_col, edgecolor='none')
        ax.add_patch(circle)
        ax.text(x + 0.35, y + h - 0.4, str(step_num), ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        
        ax.text(x + 0.7, y + h - 0.4, title, ha='left', va='center', fontsize=10, fontweight='bold', color=border_col)
        
        y_text = y + h - 0.85
        for item in items:
            ax.text(x + 0.25, y_text, f"• {item}", ha='left', va='center', fontsize=8.2, color=DARK)
            y_text -= 0.32

    # 4 Steps horizontal
    add_step(0.4, 1.2, 2.7, 3.8, 1, "Data Hygiene & Validation",
             ["String Trimming (F.trim)", "Whitespace normalization", "Deduplication via dropDuplicates()", "Label verification (is_fraud)", "Null record filtering", "Row count integrity check"],
             "#F8FAFC", NAVY)

    add_step(3.5, 1.2, 2.7, 3.8, 2, "Feature Isolation & Selection",
             ["Identifier Isolation:", " - customer_id (Excluded)", " - transaction_id (Excluded)", "Prevents target data leakage", "Type classification via NumericType", "9 continuous numeric attributes"],
             LIGHT_BLUE, BORDER_BLUE)

    add_step(6.6, 1.2, 2.9, 3.8, 3, "Categorical Encoding",
             ["22 Categorical attributes", "Cardinality check (max_cat=100)", "StringIndexer Pipeline:", " - Maps categories to frequency rank", "OneHotEncoder Pipeline:", " - Converts indexes to sparse vectors", "Handles unseen categories via 'keep'"],
             "#ECFDF5", GREEN)

    add_step(9.9, 1.2, 2.7, 3.8, 4, "Vector Assembly & Scaling",
             ["VectorAssembler aggregation", "Combines 9 numerics + 22 OHE", "Generates single 'features' vector", "Random 80/20 train/test split", "Seed=42 for deterministic runs", "Output cached for distributed fit"],
             "#FFFBEB", AMBER)

    # Arrows
    arrow_props = dict(arrowstyle="->", lw=2, color=NAVY, shrinkA=5, shrinkB=5)
    ax.annotate("", xy=(3.5, 3.1), xytext=(3.1, 3.1), arrowprops=arrow_props)
    ax.annotate("", xy=(6.6, 3.1), xytext=(6.2, 3.1), arrowprops=arrow_props)
    ax.annotate("", xy=(9.9, 3.1), xytext=(9.5, 3.1), arrowprops=arrow_props)

    plt.tight_layout()
    out_path = PLOTS_DIR / 'preprocessing_methodology.png'
    plt.savefig(out_path, dpi=220)
    plt.close()
    print(f"[+] Generated: {out_path}")

def draw_hyperparameter_tuning_flow():
    fig, ax = plt.subplots(figsize=(13, 6.5), dpi=220)
    ax.axis('off')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.5)

    ax.text(6.5, 6.1, "Distributed Model Training & Hyperparameter Tuning Framework",
            ha='center', va='center', fontsize=13, fontweight='bold', color=NAVY)
    ax.text(6.5, 5.7, "Optimization Configurations for 5 Machine Learning & Deep Learning Classifiers",
            ha='center', va='center', fontsize=9.5, style='italic', color='#64748B')

    def add_tuning_card(x, y, w, h, model_name, params, metrics_summary, bg_col, border_col):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor=bg_col, edgecolor=border_col, linewidth=1.6)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.35, model_name, ha='center', va='center', fontsize=9.5, fontweight='bold', color=border_col)
        
        y_text = y + h - 0.75
        for p in params:
            ax.text(x + 0.2, y_text, f"- {p}", ha='left', va='center', fontsize=7.8, color=DARK)
            y_text -= 0.28
            
        # Metric tag
        ax.text(x + w/2, y + 0.3, metrics_summary, ha='center', va='center', fontsize=8, fontweight='bold', color=border_col)

    # 5 Model tuning cards
    add_tuning_card(0.3, 1.2, 2.3, 3.8, "Linear SVM (Champion)", 
                    ["maxIter: 50", "regParam: 0.01", "standardization: True", "loss: Hinge loss", "tol: 1e-6", "threshold: 0.0"],
                    "F1: 0.9898 | AUC: 0.9980", "#FEF2F2", '#DC2626')

    add_tuning_card(2.8, 1.2, 2.3, 3.8, "Random Forest", 
                    ["numTrees: 50", "maxDepth: 8", "featureSubset: sqrt", "impurity: gini", "bootstrap: True", "seed: 42"],
                    "F1: 0.9834 | Prec: 99.97%", LIGHT_BLUE, BORDER_BLUE)

    add_tuning_card(5.3, 1.2, 2.3, 3.8, "Gradient-Boosted Trees", 
                    ["maxIter: 30", "maxDepth: 5", "stepSize: 0.1", "lossType: logistic", "subsamplingRate: 1.0", "seed: 42"],
                    "F1: 0.9831 | Prec: 99.91%", "#ECFDF5", GREEN)

    add_tuning_card(7.8, 1.2, 2.3, 3.8, "Logistic Regression", 
                    ["maxIter: 50", "regParam: 0.01", "elasticNet: 0.0 (L2)", "tol: 1e-6", "standardization: True", "threshold: 0.5"],
                    "F1: 0.9890 | AUC: 0.9990", "#FFFBEB", AMBER)

    add_tuning_card(10.3, 1.2, 2.4, 3.8, "Decision Tree", 
                    ["maxDepth: 8", "minInstancesPerNode: 5", "impurity: gini", "maxBins: 32", "seed: 42"],
                    "F1: 0.9783 | Fast Baseline", "#F5F3FF", PURPLE)

    plt.tight_layout()
    out_path = PLOTS_DIR / 'hyperparameter_tuning_flow.png'
    plt.savefig(out_path, dpi=220)
    plt.close()
    print(f"[+] Generated: {out_path}")

if __name__ == '__main__':
    draw_methodology_architecture()
    draw_preprocessing_workflow()
    draw_hyperparameter_tuning_flow()
