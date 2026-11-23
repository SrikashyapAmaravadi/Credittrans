import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

ROOT = Path(__file__).resolve().parent
PLOTS_DIR = ROOT / 'results' / 'plots'

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def style_table(table, col_widths=None, header_bg="1B365D", alt_bg="F4F6F9"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if i == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            for cell in row.cells:
                set_cell_background(cell, header_bg)
                set_cell_margins(cell, top=140, bottom=140, left=160, right=160)
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for run in p.runs:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)
                        run.font.size = Pt(9.5)
                        run.font.name = "Calibri"
        else:
            bg = alt_bg if i % 2 == 1 else "FFFFFF"
            for cell in row.cells:
                if bg != "FFFFFF":
                    set_cell_background(cell, bg)
                set_cell_margins(cell, top=100, bottom=100, left=160, right=160)
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.font.size = Pt(9)
                        run.font.name = "Calibri"
                        run.font.color.rgb = RGBColor(40, 40, 40)
        
        if col_widths:
            for c_idx, width in enumerate(col_widths):
                if c_idx < len(row.cells):
                    row.cells[c_idx].width = Inches(width)

def build_docx(output_path):
    doc = Document()
    
    # Page setup - 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = f_p.add_run("CSET371: Big Data Analytics & BI | Final Project Report | Bennett University")
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = RGBColor(128, 128, 128)

    NAVY = RGBColor(27, 54, 93)      # #1B365D
    SLATE = RGBColor(74, 85, 104)    # #4A5568
    DARK = RGBColor(30, 41, 59)      # #1E293B

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(20)
        p.paragraph_format.space_after = Pt(10)
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(20)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = SLATE
        return p

    def add_body(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Calibri"
            r_pre.font.size = Pt(10)
            r_pre.font.bold = True
            r_pre.font.color.rgb = DARK
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        run.font.color.rgb = DARK
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Calibri"
            r_pre.font.size = Pt(10)
            r_pre.font.bold = True
            r_pre.font.color.rgb = DARK
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        run.font.color.rgb = DARK
        return p

    def add_callout(text, title="NOTE"):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.right_indent = Inches(0.4)
        r_title = p.add_run(f"[{title}] ")
        r_title.font.name = "Calibri"
        r_title.font.size = Pt(9.5)
        r_title.font.bold = True
        r_title.font.color.rgb = NAVY
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.italic = True
        run.font.color.rgb = SLATE

    def add_image_safe(img_path, caption=None, width=Inches(6.0)):
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            doc.add_picture(str(img_path), width=width)
            if caption:
                p_cap = doc.add_paragraph()
                p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_cap.paragraph_format.space_after = Pt(8)
                r = p_cap.add_run(caption)
                r.font.name = "Calibri"
                r.font.size = Pt(9)
                r.font.italic = True
                r.font.color.rgb = SLATE

    # ==========================
    # COVER PAGE
    # ==========================
    logo_path = ROOT / 'results' / 'bennett_logo.png'
    if logo_path.exists():
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(8)
        p_logo.paragraph_format.space_after = Pt(8)
        doc.add_picture(str(logo_path), width=Inches(1.6))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("BENNETT UNIVERSITY\n")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(17)
    r_inst.font.bold = True
    r_inst.font.color.rgb = NAVY

    r_dept = p_inst.add_run("SCHOOL OF COMPUTER SCIENCE ENGINEERING & TECHNOLOGY\n\n")
    r_dept.font.name = "Calibri"
    r_dept.font.size = Pt(12)
    r_dept.font.bold = True
    r_dept.font.color.rgb = SLATE

    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_badge = p_badge.add_run("PROJECT IMPLEMENTATION FINAL REPORT — MILESTONE 3 & FINAL ASSESSMENT\n\n")
    r_badge.font.name = "Calibri"
    r_badge.font.size = Pt(12)
    r_badge.font.bold = True
    r_badge.font.color.rgb = RGBColor(197, 48, 48)

    add_title("SCALABLE FINANCIAL FRAUD DETECTION AND RISK INTELLIGENCE USING APACHE SPARK, HADOOP AND MACHINE LEARNING")

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(16)
    r_course = p_course.add_run("Course Code: CSET371 — Big Data Analytics and Business Intelligence\nAcademic Year: 2026\nProject Guide: Dr. Aditya Bhardwaj")
    r_course.font.name = "Calibri"
    r_course.font.size = Pt(11)
    r_course.font.italic = True
    r_course.font.color.rgb = SLATE

    # Submitter box
    sub_table = doc.add_table(rows=6, cols=2)
    sub_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    submit_data = [
        ("Submitted by:", ""),
        ("• Srikashyap Amaravadi", "S24CSEU1423 (Lead Big Data Engineer & Classifier Architect)"),
        ("• Gitesh Goyal", "S24CSEU0774 (ML Optimization Engineer & Schema Discovery Lead)"),
        ("• Annya Sharma", "S24CSEU1408 (Data Hygiene & Feature Pipeline Engineering Lead)"),
        ("• Ajitej Singh", "S24CSEU1413 (Risk Intelligence, Evaluation Analytics & BI Lead)"),
        ("Project Faculty Guide:", "Dr. Aditya Bhardwaj")
    ]
    for row_idx, (col0, col1) in enumerate(submit_data):
        row = sub_table.rows[row_idx]
        p0 = row.cells[0].paragraphs[0]
        p1 = row.cells[1].paragraphs[0]
        r0 = p0.add_run(col0)
        r1 = p1.add_run(col1)
        r0.font.name = "Calibri"
        r1.font.name = "Calibri"
        r0.font.size = Pt(10)
        r1.font.size = Pt(10)
        if row_idx in (0, 5):
            r0.font.bold = True
            r1.font.bold = True
            r0.font.color.rgb = NAVY
            r1.font.color.rgb = NAVY
        else:
            r0.font.color.rgb = DARK
            r1.font.color.rgb = DARK
        set_cell_margins(row.cells[0], top=50, bottom=50, left=80, right=80)
        set_cell_margins(row.cells[1], top=50, bottom=50, left=80, right=80)

    doc.add_page_break()

    # ==========================
    # DECLARATION
    # ==========================
    add_heading_1("DECLARATION OF ORIGINALITY AND PLAGIARISM COMPLIANCE")
    add_body(
        "We hereby declare that this final project report titled 'Scalable Financial Fraud Detection and Risk Intelligence Using Apache Spark, "
        "Hadoop and Machine Learning' is an authentic record of our own research and software engineering executed under the supervision of "
        "Dr. Aditya Bhardwaj, School of Computer Science Engineering and Technology, Bennett University."
    )
    add_body(
        "All data pipelines, distributed transformations, estimators, heuristic risk scoring rules, and analytical visualizations were executed and "
        "benchmarked on our active distributed execution environment. Where benchmark datasets or third-party frameworks have been utilized, they have been "
        "comprehensively cited adhering to University academic integrity and plagiarism guidelines. No synthetic AI-generated illustrations were used; "
        "all figures represent deterministic mathematical diagrams and measured empirical results."
    )

    # ==========================
    # ABSTRACT
    # ==========================
    add_heading_1("ABSTRACT")
    add_body(
        "Digital financial networks process millions of payment events per hour under extreme class imbalance (~4.90% fraud). Single-machine workflows "
        "suffer memory exhaustion and computational latency when processing multi-gigabyte transaction streams. This report documents the complete implementation "
        "of the CreditTransAct Financial Fraud Analytics Platform built on Apache Spark 3.5.4, Apache Hadoop 3.3.5, and Python 3.11, validated on the 5.01 GB "
        "CreditTransAct benchmark dataset (15,000,000 transaction records across 34 feature attributes)."
    )
    add_callout(
        "Core Empirical Achievement: Linear SVM achieved an F1-Score of 0.9898 and Recall of 98.01% on an unseen holdout partition of 300,296 records. "
        "Random Forest achieved 99.97% Precision with only 4 false alarms across 285k legitimate transactions. The 4-tier hybrid triage engine clears 95.23% "
        "of normal traffic automatically while halting 97.59% of fraudulent attempts instantly.",
        title="EMPIRICAL HIGHLIGHT"
    )

    # ==========================
    # TABLE OF CONTENTS
    # ==========================
    add_heading_1("TABLE OF CONTENTS")
    toc_items = [
        "1. Introduction & Proposed Methodology",
        "2. Problem Statement and Architectural Objectives",
        "3. Dataset Description and Verified 34-Attribute Catalog",
        "4. System Requirements and Distributed Architecture",
        "5. Development Environment and Verified Tech Stack",
        "6. Data Ingestion and Distributed Storage Pipeline",
        "7. Data Understanding and Quality Assessment",
        "8. Data Preprocessing and Feature Engineering Methodology",
        "9. Distributed Machine Learning Algorithms & Mathematical Formulation",
        "10. Hyperparameter Tuning and Optimization Framework",
        "11. Model Training, Validation Strategy & Leakage Prevention",
        "12. Comprehensive Evaluation Metrics, ROC-AUC & Confusion Matrices",
        "13. Explainable Risk Scoring Intelligence and Reason Codes",
        "14. Operational 4-Tier Hybrid Fraud Triage Engine",
        "15. Business Intelligence and Power BI Enterprise Integration",
        "16. Testing, Limitations, Plagiarism & Ethical Compliance",
        "17. Team Contributions and Technical Work Breakdown",
        "18. Conclusion and Future Roadmap",
        "19. References"
    ]
    for item in toc_items:
        add_body(item)

    doc.add_page_break()

    # ==========================
    # 1. INTRODUCTION & PROPOSED METHODOLOGY
    # ==========================
    add_heading_1("1. INTRODUCTION & PROPOSED METHODOLOGY")
    add_body(
        "Electronic payment networks require fraud defense systems that combine high recall with minimal false positives. "
        "Our proposed architecture decouples raw ingestion, columnar Parquet caching, hygiene, heuristic scoring, feature vectorization, "
        "distributed classifier training, and multi-tier triage into distinct layers."
    )
    add_heading_2("1.1 Proposed Methodology Architecture Diagram")
    add_image_safe(PLOTS_DIR / 'methodology_architecture.png', "Figure 1.1: Proposed Scalable Financial Fraud Analytics Methodology Architecture", width=Inches(6.2))

    # ==========================
    # 2. PROBLEM STATEMENT & OBJECTIVES
    # ==========================
    add_heading_1("2. PROBLEM STATEMENT AND ARCHITECTURAL OBJECTIVES")
    add_body(
        "Financial institutions require scalable automated systems capable of ingesting high-velocity streams, assessing quality, isolating risk indicators, "
        "and prioritizing suspicious activity for human investigators without prohibitive latencies or high false-alarm rates."
    )
    add_bullet(" Distributed Scalability: Eliminate I/O bottlenecks by converting raw CSV to Snappy Parquet partitions.", "1.")
    add_bullet(" Data Hygiene & Leakage Isolation: Eliminate identifiers (customer_id, transaction_id) while preserving 31 predictive features.", "2.")
    add_bullet(" Transparent Heuristic Risk Scoring: Compute empirical 90th percentile amounts and rare merchant volume shares.", "3.")
    add_bullet(" Distributed ML Classification: Train and evaluate 5 candidate Spark MLlib models on 1.5 million transactions.", "4.")
    add_bullet(" Operational 4-Tier Hybrid Triage: Establish an actionable operational triage engine combining ML probabilities with heuristic rules.", "5.")
    add_bullet(" Business Intelligence Integration: Provide pre-modeled Star Schema datasets for Power BI dashboards.", "6.")

    # ==========================
    # 3. DATASET DESCRIPTION & ATTRIBUTE CATALOG
    # ==========================
    add_heading_1("3. DATASET DESCRIPTION AND VERIFIED 34-ATTRIBUTE CATALOG")
    add_body(
        "The project utilizes the CreditTransAct benchmark dataset (Mendeley Data, DOI: 10.17632/y64bbnm2s3.1), comprising 15,000,000 records (~5.01 GB CSV) "
        "with 34 feature attributes. Class distribution: 14,264,776 Legitimate (95.10%), 735,224 Fraudulent (4.90%)."
    )

    # Full 34-column attribute catalog
    schema_data = [
        ("#", "Attribute Name", "Inferred Type", "Category", "Semantic Description"),
        ("1", "transaction_amount", "Double", "Numeric", "Monetary currency value of transaction"),
        ("2", "transaction_amount_bin", "String", "Categorical", "Discretized spending tier (low, medium, high)"),
        ("3", "avg_amount_deviation_sigma", "Double", "Numeric", "Std deviations from historical customer average"),
        ("4", "merchant_category", "String", "Categorical", "Commercial category (grocery, electronics, travel)"),
        ("5", "merchant_risk_score", "String", "Categorical", "Historical merchant risk profile (low, high)"),
        ("6", "merchant_category_vs_history", "String", "Categorical", "Category alignment with customer spending history"),
        ("7", "geo_velocity_kmh", "Double", "Numeric", "Calculated physical velocity between sequential txns"),
        ("8", "geo_velocity_bin", "String", "Categorical", "Velocity classification (normal, fast)"),
        ("9", "geo_distance_km", "Double", "Numeric", "Distance in km from customer billing residence"),
        ("10", "geo_distance_bin", "String", "Categorical", "Spatial bucket (same_location, intercity)"),
        ("11", "merchant_location", "String", "Categorical", "Location context (home_city, same_country, foreign)"),
        ("12", "country_consistency", "String", "Categorical", "Match against domestic issuing bank country"),
        ("13", "ip_address_type", "String", "Categorical", "Originating IP type (residential, corporate, datacenter)"),
        ("14", "device_fingerprint_match", "String", "Categorical", "Hardware identity status (known_device, new_device)"),
        ("15", "session_duration_sec", "Double", "Numeric", "Digital checkout interaction time in seconds"),
        ("16", "session_duration_bin", "String", "Categorical", "Interaction speed (fast, normal, slow)"),
        ("17", "network_carrier_type", "String", "Categorical", "Connection protocol (wifi, mobile_data, datacenter)"),
        ("18", "cards_on_device_30d", "Integer", "Numeric", "Count of cards bound to device within 30 days"),
        ("19", "cvv_match_status", "String", "Categorical", "CVV2 verification result (cvv2_match, mismatch)"),
        ("20", "three_ds_auth_result", "String", "Categorical", "3D-Secure outcome (frictionless_pass, challenge_fail)"),
        ("21", "tokenization_used", "String", "Categorical", "Cardholder credential format (emv_chip, raw_pan)"),
        ("22", "failed_attempts_before_success", "Integer", "Numeric", "Preceding rejected payment attempts prior to approval"),
        ("23", "transaction_velocity_1h", "String", "Categorical", "Hourly velocity bucket (normal, elevated)"),
        ("24", "time_of_transaction", "String", "Categorical", "Diurnal time window (late_night, afternoon, evening)"),
        ("25", "account_credential_change_recency", "String", "Categorical", "Proximity to password/MFA update (recent, no_change)"),
        ("26", "card_present_cnp", "String", "Categorical", "Transaction channel (card_present_swipe, cnp_online)"),
        ("27", "order_shipping_speed", "String", "Categorical", "Fulfillment logistics (in_store, same_day, standard)"),
        ("28", "account_age_days", "Integer", "Numeric", "Account tenure in days since initial opening"),
        ("29", "chargeback_history_count", "Integer", "Numeric", "Historical chargeback disputes logged against account"),
        ("30", "customer_id", "String", "Identifier", "Customer ID (Excluded from ML to prevent leakage)"),
        ("31", "transaction_id", "String", "Identifier", "Transaction Key (Excluded from ML to prevent leakage)"),
        ("32", "segment", "String", "Categorical", "Customer profile segment (A_established, etc.)"),
        ("33", "customer_type", "String", "Categorical", "Behavioral classification (customer_based)"),
        ("34", "is_fraud", "Integer", "Target Label", "Ground truth binary label (0=Legitimate, 1=Fraudulent)")
    ]
    t_schema = doc.add_table(rows=len(schema_data), cols=5)
    for r_idx, row in enumerate(schema_data):
        for c_idx, val in enumerate(row):
            t_schema.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_schema, col_widths=[0.4, 2.0, 1.0, 1.1, 2.0])

    # ==========================
    # 4. SYSTEM REQUIREMENTS & ARCHITECTURE
    # ==========================
    add_heading_1("4. SYSTEM REQUIREMENTS AND DISTRIBUTED ARCHITECTURE")
    sys_modules = [
        ("Pipeline Module", "Script Source", "Technical Operations Performed", "Primary Artifact"),
        ("00: Schema Profiling", "pipeline/00_inspect_schema.py", "Full file scan across 38 partitions, schema discovery, row count", "results/schema_report.json"),
        ("01: Parquet Ingestion", "pipeline/01_ingest.py", "Parallel CSV loading across 38 tasks, Snappy Parquet encoding", "results/raw/ (Snappy Parquet)"),
        ("02: Data Hygiene", "pipeline/02_transform.py", "Whitespace trimming (F.trim), dropDuplicates(), null label filter", "results/cleaned/ (15M records)"),
        ("03: Risk Scoring", "pipeline/03_risk_analysis.py", "Approx-quantile calculation, rare merchant profiling, reason array", "results/risk_scored/"),
        ("04: ML Training", "pipeline/04_train_models.py", "StringIndexer, OneHotEncoder, VectorAssembler, 5 ML models", "results/models/, model_metrics.csv"),
        ("05: Evaluation", "pipeline/05_evaluate.py", "Precision, Recall, F1, ROC-AUC, 10 plots & confusion matrices", "results/plots/"),
        ("06: Hybrid Triage", "pipeline/06_hybrid_inference.py", "4-tier decision matrix combining ML probabilities & heuristics", "results/hybrid_triage_summary.csv")
    ]
    t_sys = doc.add_table(rows=len(sys_modules), cols=4)
    for r_idx, row in enumerate(sys_modules):
        for c_idx, val in enumerate(row):
            t_sys.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_sys, col_widths=[1.5, 1.8, 2.0, 1.2])

    # ==========================
    # 5. DEVELOPMENT ENVIRONMENT
    # ==========================
    add_heading_1("5. DEVELOPMENT ENVIRONMENT AND VERIFIED TECH STACK")
    add_bullet(" Operating System: Microsoft Windows 11 (64-bit)", "OS:")
    add_bullet(" Java Virtual Machine: Microsoft Build of OpenJDK 17 LTS (jdk-17.0.21.21-hotspot)", "JVM:")
    add_bullet(" Python Runtime: Python 3.11.9 (Dedicated virtual environment .venv)", "Python:")
    add_bullet(" Hadoop Ecosystem: Apache Hadoop 3.3.5 native binaries (winutils.exe, hadoop.dll)", "Hadoop:")
    add_bullet(" Core Processing Engine: Apache Spark 3.5.4 (PySpark SQL + MLlib + Catalyst Optimizer)", "Spark:")
    add_bullet(" Memory & Hardware Allocation: Driver Memory: 6 GB; Executor Memory: 6 GB; 16 Cores", "Resources:")

    # ==========================
    # 6. DATA INGESTION & PARQUET PIPELINE
    # ==========================
    add_heading_1("6. DATA INGESTION AND DISTRIBUTED STORAGE PIPELINE")
    add_body(
        "Ingesting raw CSV into Snappy-compressed Apache Parquet yielded an 85% storage reduction (from 5.01 GB to ~450 MB). "
        "Queries selecting subsets of features perform column pruning on disk, skipping irrelevant byte blocks and eliminating repeated parsing overheads."
    )

    # ==========================
    # 7. DATA UNDERSTANDING & QUALITY ASSESSMENT
    # ==========================
    add_heading_1("7. DATA UNDERSTANDING AND QUALITY ASSESSMENT")
    add_body(
        "Quality audit confirmed 100% record integrity across all 15,000,000 transactions. The target label is_fraud had zero null values. "
        "Unique identifiers (customer_id, transaction_id) were designated as excluded attributes to prevent target data leakage."
    )

    # ==========================
    # 8. DATA PREPROCESSING & FEATURE ENGINEERING
    # ==========================
    add_heading_1("8. DATA PREPROCESSING AND FEATURE ENGINEERING METHODOLOGY")
    add_body(
        "The data preparation methodology follows four rigorous steps: (1) Whitespace sanitation via F.trim(), (2) Deduplication via dropDuplicates(), "
        "(3) Categorical indexing via StringIndexer with handleInvalid='keep' and OneHotEncoder sparse representation, and (4) VectorAssembler aggregation."
    )
    add_image_safe(PLOTS_DIR / 'preprocessing_methodology.png', "Figure 8.1: Step-by-Step Data Preprocessing and Feature Engineering Workflow", width=Inches(6.2))

    # ==========================
    # 9. DISTRIBUTED MACHINE LEARNING ALGORITHMS
    # ==========================
    add_heading_1("9. DISTRIBUTED MACHINE LEARNING ALGORITHMS & MATHEMATICAL FORMULATION")
    add_body(
        "Five distributed classifiers were implemented in Spark MLlib: (1) Linear Support Vector Machine (Linear SVM) formulating maximum-margin hyperplane separation, "
        "(2) Random Forest Classifier using 50 randomized bagging trees, (3) Gradient-Boosted Trees (GBT) optimizing binomial log-likelihood via sequential boosting, "
        "(4) Logistic Regression with L2 ElasticNet regularization, and (5) Decision Tree Classifier (CART) maximizing Gini impurity reduction."
    )

    # ==========================
    # 10. HYPERPARAMETER TUNING
    # ==========================
    add_heading_1("10. HYPERPARAMETER TUNING AND OPTIMIZATION FRAMEWORK")
    add_body(
        "Hyperparameter sweeps balanced variance, bias, and execution latency across all 5 estimators. Linear SVM was tuned with L2 regParam=0.01; "
        "Random Forest with 50 trees, maxDepth=8, featureSubset=sqrt; GBT with 30 iterations, stepSize=0.1, maxDepth=5; Logistic Regression with L2 penalty; "
        "and Decision Tree with maxDepth=8."
    )
    add_image_safe(PLOTS_DIR / 'hyperparameter_tuning_flow.png', "Figure 10.1: Distributed Model Training and Hyperparameter Tuning Framework", width=Inches(6.2))

    # ==========================
    # 11. MODEL TRAINING & VALIDATION STRATEGY
    # ==========================
    add_heading_1("11. MODEL TRAINING, VALIDATION STRATEGY & LEAKAGE PREVENTION")
    add_body(
        "The dataset was partitioned into an 80% training partition (1,201,347 records) and a 20% unseen test partition (300,296 records). "
        "Feature pipelines were fitted strictly on the training partition before transforming the test set, preventing information leakage."
    )

    # ==========================
    # 12. EVALUATION METRICS & CONFUSION MATRICES
    # ==========================
    add_heading_1("12. COMPREHENSIVE EVALUATION METRICS, ROC-AUC & CONFUSION MATRICES")
    add_body("Evaluated on 300,296 unseen holdout records (14,513 Actual Frauds, 285,783 Actual Legitimate):")

    perf_data = [
        ("Classifier", "Precision", "Recall", "F1-Score", "ROC-AUC", "TP", "FP", "FN", "TN"),
        ("Linear SVM (Champion)", "0.9996", "0.9801", "0.9898", "0.9980", "14,224", "5", "289", "285,778"),
        ("Logistic Regression", "0.9988", "0.9794", "0.9890", "0.9990", "14,214", "17", "299", "285,766"),
        ("Random Forest", "0.9997", "0.9677", "0.9834", "0.9968", "14,044", "4", "469", "285,779"),
        ("Gradient-Boosted Trees", "0.9991", "0.9675", "0.9831", "0.9906", "14,041", "12", "472", "285,771"),
        ("Decision Tree", "0.9977", "0.9597", "0.9783", "0.8567", "13,928", "32", "585", "285,751")
    ]
    t_perf = doc.add_table(rows=len(perf_data), cols=9)
    for r_idx, row in enumerate(perf_data):
        for c_idx, val in enumerate(row):
            t_perf.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_perf, col_widths=[1.5, 0.7, 0.7, 0.7, 0.7, 0.6, 0.5, 0.5, 0.8])

    add_heading_2("12.1 Performance Comparison Curves")
    add_image_safe(PLOTS_DIR / 'overall_model_comparison.png', "Figure 12.1: Overall Model Benchmark across Precision, Recall, F1 and ROC-AUC", width=Inches(5.8))
    add_image_safe(PLOTS_DIR / 'roc_auc_comparison.png', "Figure 12.2: Area Under ROC Curve (ROC-AUC) Comparison", width=Inches(5.2))
    add_image_safe(PLOTS_DIR / 'f1_comparison.png', "Figure 12.3: F1-Score Harmonic Mean Performance", width=Inches(5.2))

    add_heading_2("12.2 Confusion Matrix Heatmaps")
    add_image_safe(PLOTS_DIR / 'confusion_LinearSVM.png', "Figure 12.4: Linear SVM Confusion Matrix (14,224 TP, 5 FP, 289 FN, 285,778 TN)", width=Inches(4.4))
    add_image_safe(PLOTS_DIR / 'confusion_RandomForest.png', "Figure 12.5: Random Forest Confusion Matrix (14,044 TP, 4 FP, 469 FN, 285,779 TN)", width=Inches(4.4))
    add_image_safe(PLOTS_DIR / 'confusion_LogisticRegression.png', "Figure 12.6: Logistic Regression Confusion Matrix", width=Inches(4.4))

    # ==========================
    # 13. HEURISTIC RISK SCORING
    # ==========================
    add_heading_1("13. EXPLAINABLE RISK SCORING INTELLIGENCE AND REASON CODES")
    add_body(
        "Every transaction receives a baseline of 10 points. Amounts exceeding the empirical 90th percentile receive +30 points (AMOUNT_TOP_DECILE), "
        "and transactions in rare merchant categories (<5% share) receive +20 points (RARE_PROFILE). Scores are capped at 100 points."
    )
    risk_summary_data = [
        ("Risk Category", "Score Threshold", "Transaction Count", "Percentage (%)", "Operational Recommendation"),
        ("LOW", "Score < 35.0", "13,467,586", "89.78%", "Automated standard clearance; zero intervention"),
        ("MEDIUM", "35.0 <= Score < 70.0", "1,532,414", "10.22%", "Secondary verification / step-up auth queue"),
        ("HIGH", "Score >= 70.0", "0", "0.00%", "Reserved for concurrent multi-factor alerts"),
        ("Total", "Full Scope", "15,000,000", "100.00%", "Full dataset scored and stored at results/risk_scored")
    ]
    t_risk = doc.add_table(rows=len(risk_summary_data), cols=5)
    for r_idx, row in enumerate(risk_summary_data):
        for c_idx, val in enumerate(row):
            t_risk.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_risk, col_widths=[1.1, 1.4, 1.4, 1.1, 1.5])

    # ==========================
    # 14. OPERATIONAL 4-TIER TRIAGE
    # ==========================
    add_heading_1("14. OPERATIONAL 4-TIER HYBRID FRAUD TRIAGE ENGINE")
    triage_data = [
        ("Triage Tier", "Action & Policy", "Volume Count", "Volume Share (%)", "Fraud Caught", "Legitimate Cleared"),
        ("Tier 1: Critical Block", "Immediate card freeze & security SMS", "14,168", "4.72%", "14,163 (99.96%)", "5 (0.04%)"),
        ("Tier 2: Step-Up Auth", "Prompt for 2FA biometric / OTP challenge", "63", "0.02%", "51 (80.95%)", "12 (19.05%)"),
        ("Tier 3: Compliance Audit", "Route to asynchronous investigation queue", "102", "0.03%", "14 (13.73%)", "88 (86.27%)"),
        ("Tier 4: Automated Clearance", "Frictionless, instantaneous clearance", "285,963", "95.23%", "285 (0.10%)", "285,678 (99.90%)"),
        ("Total Evaluated", "Holdout Test Partition", "300,296", "100.00%", "14,513", "285,783")
    ]
    t_triage = doc.add_table(rows=len(triage_data), cols=6)
    for r_idx, row in enumerate(triage_data):
        for c_idx, val in enumerate(row):
            t_triage.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_triage, col_widths=[1.5, 1.8, 0.9, 1.0, 1.1, 1.2])

    # ==========================
    # 15. POWER BI INTEGRATION
    # ==========================
    add_heading_1("15. BUSINESS INTELLIGENCE AND POWER BI ENTERPRISE INTEGRATION")
    add_body(
        "A 5-table Star Schema was exported into powerbi/data/ (Dim_Model_Benchmark, Fact_Confusion_Matrix, Fact_Triage_Decisions, "
        "Fact_Heuristic_Risk_Summary, Fact_Scored_Transactions_Sample_50k) with complete DAX formulas for Recall, False Alarm Rate, and Prevented Loss."
    )

    # ==========================
    # 16. TESTING, LIMITATIONS & ETHICS
    # ==========================
    add_heading_1("16. TESTING, LIMITATIONS, PLAGIARISM & ETHICAL COMPLIANCE")
    add_body(
        "Testing validated worker process spawning, row count preservation (15M -> 15M), and deterministic reproducibility across runs. "
        "All prose and analysis represent original academic work adhering to plagiarism guidelines."
    )

    # ==========================
    # 17. TEAM CONTRIBUTIONS & TECHNICAL BREAKDOWN
    # ==========================
    add_heading_1("17. TEAM CONTRIBUTIONS AND TECHNICAL WORK BREAKDOWN")
    add_body(
        "To ensure rigorous project governance, each team member executed distinct technical deliverables across the pipeline:"
    )

    contrib_data = [
        ("Candidate Name", "Roll Number", "Technical Role", "Concrete Technical Work Executed"),
        ("Srikashyap Amaravadi", "S24CSEU1423", "Lead Big Data Engineer & Classifier Architect", 
         "• Configured Apache Spark 3.5.4 cluster environment, JVM heap allocation (6g driver, 6g executor), and Hadoop Winutils/DLL integration.\n"
         "• Architected and implemented the distributed Linear Support Vector Machine (Linear SVM) and Random Forest Classifier pipelines in Spark MLlib.\n"
         "• Engineered the multi-threaded localhost web server (server.py) and live inference REST API (/api/predict).\n"
         "• Optimized memory caching (train_vec.cache(), test_vec.cache()) and single-pass confusion matrix computation."),
        
        ("Gitesh Goyal", "S24CSEU0774", "ML Optimization Engineer & Schema Discovery Lead", 
         "• Developed and executed Stage 00 (00_inspect_schema.py) automated schema inference and distributed data profiling across 38 parallel Spark partitions.\n"
         "• Implemented, benchmarked, and hyperparameter-tuned the Gradient-Boosted Trees (GBT), Logistic Regression (L2 ElasticNet), and Decision Tree models.\n"
         "• Conducted multi-iteration learning rate shrinkage sweeps (eta = 0.1) and depth ceiling evaluations to optimize tree splitting and convergence.\n"
         "• Implemented the distributed model serialization framework (PipelineModel.write().overwrite().save()) persisting end-to-end transformers and fitted estimators."),
        
        ("Annya Sharma", "S24CSEU1408", "Data Hygiene & Feature Pipeline Engineering Lead", 
         "• Engineered the Stage 01 distributed ingestion pipeline (01_ingest.py) converting 5.01 GB raw CSV into Snappy-compressed columnar Parquet partitions (results/raw).\n"
         "• Designed Stage 02 data transformation and hygiene layer (02_transform.py): whitespace trimming via F.trim(), full-record deduplication via dropDuplicates(), and target non-null validation.\n"
         "• Implemented the 22-stage StringIndexer and OneHotEncoder categorical transformation pipeline, including cardinality thresholding (max_categories=100) and unseen category handling (handleInvalid='keep').\n"
         "• Formulated feature vector assembly via VectorAssembler, combining 9 continuous numerical attributes with sparse encoded vectors."),
        
        ("Ajitej Singh", "S24CSEU1413", "Risk Intelligence, Evaluation & BI Integration Lead", 
         "• Developed Stage 03 explainable heuristic risk scoring engine (03_risk_analysis.py), calculating dynamic 90th percentile amount quantiles (approxQuantile) and rare merchant profile shares.\n"
         "• Formulated and coded the Stage 06 Operational 4-Tier Hybrid Fraud Triage Engine (06_hybrid_inference.py), creating the decision matrix that categorizes transactions into Critical Block, Step-Up 2FA, Compliance Audit, and Automated Clearance.\n"
         "• Built the Stage 05 evaluation and statistical visualization pipeline (05_evaluate.py) generating precision, recall, F1, ROC-AUC curves, and confusion matrix heatmaps.\n"
         "• Architected the 5-table Star Schema data mart (export_for_powerbi.py) and authored the custom DAX measures for Power BI business intelligence reporting.")
    ]
    t_contrib = doc.add_table(rows=len(contrib_data), cols=4)
    for r_idx, row in enumerate(contrib_data):
        for c_idx, val in enumerate(row):
            t_contrib.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_contrib, col_widths=[1.5, 1.1, 1.5, 2.5])

    # ==========================
    # 18. CONCLUSION
    # ==========================
    add_heading_1("18. CONCLUSION AND FUTURE ROADMAP")
    add_body(
        "The CreditTransAct Financial Fraud Analytics project has achieved 100% of its planned deliverables. "
        "The distributed Big Data pipeline seamlessly processed 15,000,000 transactions, achieved an F1-Score of 0.9898 with Linear SVM, "
        "and established an operational 4-tier decision triage engine for modern financial institutions."
    )

    # ==========================
    # 19. REFERENCES
    # ==========================
    add_heading_1("19. REFERENCES")
    refs = [
        "1. CreditTransAct: A Profile-Driven Dataset for Scalable Credit Card Fraud Detection, Mendeley Data, Version 1, 9 May 2026. DOI: 10.17632/y64bbnm2s3.1.",
        "2. Apache Spark 3.5.4 Documentation: https://spark.apache.org/docs/3.5.4/",
        "3. Apache Hadoop 3.3.5 Documentation: https://hadoop.apache.org/docs/r3.3.5/",
        "4. Apache Spark MLlib Programming Guide: https://spark.apache.org/docs/3.5.4/ml-guide.html",
        "5. Python 3.11 Documentation: https://docs.python.org/3.11/",
        "6. Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5-32.",
        "7. Friedman, J. H. (2001). Greedy Function Approximation: A Gradient Boosting Machine. Annals of Statistics, 29(5), 1189-1232.",
        "8. Cortes, C., & Vapnik, V. (1995). Support-Vector Networks. Machine Learning, 20(3), 273-297."
    ]
    for ref in refs:
        add_body(ref)

    # Save
    doc.save(output_path)
    print(f"Final Report Document successfully created and saved to: {output_path}")

if __name__ == "__main__":
    docs_file = ROOT / "docs" / "CreditTransAct_Fraud_Analytics_Final_Report.docx"
    build_docx(str(docs_file))

    try:
        desktop_file = Path(r"C:\Users\kashy\OneDrive\Desktop\CreditTransAct_Fraud_Analytics_Final_Report.docx")
        import shutil
        shutil.copy2(docs_file, desktop_file)
        print(f"Copied final report to Desktop: {desktop_file}")
    except Exception as e:
        print(f"Desktop copy skipped: {e}")
