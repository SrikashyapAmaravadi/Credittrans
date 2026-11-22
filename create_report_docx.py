import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

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
        # Prevent row split across pages
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
    
    # Page setup
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
        # Add footer
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = f_p.add_run("CSET371: Big Data Analytics | Milestone 2 Report | Bennett University")
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = RGBColor(128, 128, 128)

    NAVY = RGBColor(27, 54, 93)      # #1B365D
    SLATE = RGBColor(74, 85, 104)    # #4A5568
    DARK = RGBColor(30, 41, 59)      # #1E293B

    # ==========================
    # TITLE PAGE
    # ==========================
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
    r_badge = p_badge.add_run("PROJECT IMPLEMENTATION REPORT — MILESTONE 2\n\n")
    r_badge.font.name = "Calibri"
    r_badge.font.size = Pt(13)
    r_badge.font.bold = True
    r_badge.font.color.rgb = RGBColor(197, 48, 48)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("SCALABLE FINANCIAL FRAUD DETECTION AND RISK INTELLIGENCE USING APACHE SPARK, HADOOP AND MACHINE LEARNING\n\n")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_course = p_course.add_run("Course Code: CSET371 — Big Data Analytics and Business Intelligence\n\n\n")
    r_course.font.name = "Calibri"
    r_course.font.size = Pt(11.5)
    r_course.font.italic = True
    r_course.font.color.rgb = SLATE

    # Submitter box table
    sub_table = doc.add_table(rows=6, cols=2)
    sub_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    data = [
        ("Submitted by:", ""),
        ("• Srikashyap Amaravadi", "S24CSEU1423"),
        ("• Gitesh Goyal", "S24CSEU0774"),
        ("• Annya Sharma", "S24CSEU1408"),
        ("• Ajitej Singh", "S24CSEU1413"),
        ("Project Guide:", "Dr. Aditya Bharadwaj")
    ]
    for row_idx, (col0, col1) in enumerate(data):
        row = sub_table.rows[row_idx]
        p0 = row.cells[0].paragraphs[0]
        p1 = row.cells[1].paragraphs[0]
        r0 = p0.add_run(col0)
        r1 = p1.add_run(col1)
        r0.font.name = "Calibri"
        r1.font.name = "Calibri"
        r0.font.size = Pt(10.5)
        r1.font.size = Pt(10.5)
        if row_idx in (0, 5):
            r0.font.bold = True
            r1.font.bold = True
            r0.font.color.rgb = NAVY
            r1.font.color.rgb = NAVY
        else:
            r0.font.color.rgb = DARK
            r1.font.color.rgb = DARK
        set_cell_margins(row.cells[0], top=60, bottom=60, left=100, right=100)
        set_cell_margins(row.cells[1], top=60, bottom=60, left=100, right=100)

    p_year = doc.add_paragraph()
    p_year.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_year = p_year.add_run("\n\nBennett University, Greater Noida, Uttar Pradesh\nAcademic Year: 2026")
    r_year.font.name = "Calibri"
    r_year.font.size = Pt(10)
    r_year.font.color.rgb = SLATE

    doc.add_page_break()

    # Helper functions for structured writing
    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = NAVY
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(11.5)
        r.font.bold = True
        r.font.color.rgb = SLATE
        return p

    def add_body(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = DARK
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Calibri"
            r_pre.font.size = Pt(10)
            r_pre.font.bold = True
            r_pre.font.color.rgb = NAVY
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = DARK
        return p

    # ABSTRACT
    add_heading_1("ABSTRACT")
    add_body(
        "Financial fraud represents an escalating threat to modern digital payment infrastructures due to vast transaction volumes, "
        "rapid payment velocities, and subtle fraudulent signatures concealed within legitimate consumer behaviour. Traditional single-machine "
        "analytical frameworks and manual auditing fail to scale to multi-gigabyte transaction streams. This report documents the successful "
        "implementation of Milestone 2 for an enterprise-grade Big Data analytical architecture engineered using Apache Spark 3.5.4, "
        "Apache Hadoop 3.3.5 client binaries, and Python 3.11."
    )
    add_body(
        "The pipeline is empirically validated on the complete CreditTransAct benchmark dataset (credit_card_fraud.csv), comprising exactly "
        "15,000,000 transaction records across 34 feature attributes (5.01 GB uncompressed CSV). In Milestone 2, the team developed and executed: "
        "(1) automated schema discovery and distributed profiling across 38 parallel Spark partitions; (2) scalable columnar ingestion converting "
        "raw CSV to Snappy-compressed Parquet (results/raw); (3) conservative data hygiene and distributed deduplication (results/cleaned); and "
        "(4) an explainable rule-based risk intelligence engine evaluating empirical percentile thresholds and category frequency shares "
        "(results/risk_scored and results/risk_category_summary.csv). All numerical figures, schemas, and metrics presented herein reflect verified "
        "empirical results produced on the active system."
    )

    # TABLE OF CONTENTS
    add_heading_1("TABLE OF CONTENTS")
    toc_items = [
        "1. Introduction",
        "2. Problem Statement and Objectives",
        "3. Dataset Description and Verified Schema",
        "4. System Requirements and Architecture",
        "5. Development Environment and Verified Stack",
        "6. Data Ingestion and Distributed Storage Pipeline",
        "7. Data Understanding and Quality Assessment",
        "8. Data Preprocessing and Transformation Layer",
        "9. Fraud Detection Algorithms (Planned for Milestone 3)",
        "10. Risk Scoring Intelligence and Explainability",
        "11. Model Training and Validation Strategy",
        "12. Evaluation Metrics Framework",
        "13. Implementation Workflow and Execution Status",
        "14. Measured Results, Risk Distribution and Reporting",
        "15. Testing, Limitations and Risk Management",
        "16. Team Contributions and Project Management",
        "17. Conclusion and Future Roadmap",
        "18. References"
    ]
    for item in toc_items:
        add_bullet(item)

    # 1. INTRODUCTION
    add_heading_1("1. INTRODUCTION")
    add_body(
        "Digital financial services process millions of payment events per hour across e-commerce gateways, point-of-sale terminals, and "
        "mobile payment interfaces. Although fraudulent transactions represent a minority percentage of total transaction traffic, their direct "
        "financial losses, operational chargeback expenses, and reputational ramifications are severe. Detecting fraud requires analyzing "
        "complex multivariate signals including transaction monetary values, temporal intervals, geographical velocities, merchant categories, "
        "and digital device fingerprints."
    )
    add_body(
        "Traditional rule-based fraud detection engines rely on rigid boolean thresholds that fail to adapt to evolving adversary tactics and "
        "create overwhelming false-positive burdens for fraud investigation teams. Conversely, pure black-box machine learning models frequently "
        "lack the transparent interpretability demanded by regulatory compliance frameworks. Furthermore, analyzing multi-gigabyte transaction logs "
        "exceeds the memory limits of conventional single-node data science environments."
    )
    add_body(
        "This project resolves these challenges by building a distributed Big Data fraud analytics and risk intelligence architecture. "
        "Leveraging Apache Spark SQL and Hadoop file-system abstractions, Milestone 2 establishes a high-throughput pipeline that ingests, "
        "validates, cleans, and scores 15 million transactions, generating compressed columnar Parquet layers and producing explainable "
        "heuristic risk ratings accompanied by discrete audit reason codes."
    )

    # 2. PROBLEM STATEMENT AND OBJECTIVES
    add_heading_1("2. PROBLEM STATEMENT AND OBJECTIVES")
    add_heading_2("2.1 Problem Statement")
    add_body(
        "Modern card-issuing and payment processing institutions require high-throughput analytical pipelines capable of processing millions "
        "of high-velocity transactions, assessing data quality, isolating anomalous indicators, and prioritizing high-risk cases for human "
        "adjudication without incurring prohibitive computational latency or unacceptable false-positive rates."
    )
    add_heading_2("2.2 Milestone 2 Core Objectives Completed")
    add_bullet(" Installed and verified Microsoft OpenJDK 17 LTS, Python 3.11.9, PySpark 3.5.4, and Hadoop 3.3.5 native winutils binaries.", "1. Infrastructure Setup:")
    add_bullet(" Developed and executed pipeline/00_inspect_schema.py to profile all 15,000,000 records across 38 parallel partitions, producing results/schema_report.json.", "2. Distributed Schema Discovery:")
    add_bullet(" Built pipeline/01_ingest.py to ingest the 5.01 GB raw CSV into optimized Snappy-compressed columnar Parquet format (results/raw), cutting future I/O latency.", "3. Optimized Columnar Ingestion:")
    add_bullet(" Executed pipeline/02_transform.py to apply string trimming, full-record deduplication, and target label integrity filtering (results/cleaned).", "4. Data Hygiene & Transformation:")
    add_bullet(" Formulated and executed pipeline/03_risk_analysis.py to compute empirical 90th percentile transaction thresholds and rare category frequencies, assigning composite scores and reason codes.", "5. Explainable Risk Intelligence:")

    # 3. DATASET DESCRIPTION
    add_heading_1("3. DATASET DESCRIPTION AND VERIFIED SCHEMA")
    add_body(
        "The project utilizes the CreditTransAct benchmark: A Profile-Driven Dataset for Scalable Credit Card Fraud Detection (Mendeley Data, "
        "Version 1, 9 May 2026, DOI: 10.17632/y64bbnm2s3.1). The dataset provides realistic synthetic consumer transaction patterns across "
        "multiple demographic segments."
    )
    add_heading_2("3.1 Dataset Profile & Volume Statistics")
    add_bullet(" data/credit_card_fraud.csv", "Dataset File: ")
    add_bullet(" 5,009,909,516 bytes (approx. 5.01 GB uncompressed CSV)", "Physical File Size: ")
    add_bullet(" exactly 15,000,000 rows", "Total Ingested Record Count: ")
    add_bullet(" 34 columns (33 predictive features/metadata fields + 1 ground-truth target is_fraud)", "Total Dimension Count: ")
    add_bullet(" 38 Spark partitions (approx. 128 MB per partition)", "Parallel Partitions: ")

    add_heading_2("3.2 Complete Verified Attribute Catalog")
    add_body("The table below details all 34 verified schema attributes extracted via Spark SQL during schema discovery:")

    schema_data = [
        ("Column Name", "Spark Data Type", "Semantic Description"),
        ("transaction_amount", "Double", "Monetary amount of transaction in base currency"),
        ("transaction_amount_bin", "String", "Categorical amount tier (low, medium, high)"),
        ("avg_amount_deviation_sigma", "Double", "Standard deviations from customer mean transaction amount"),
        ("merchant_category", "String", "Commercial sector (grocery, electronics, travel, etc.)"),
        ("merchant_risk_score", "String", "Historical risk category of merchant (low_risk, high_risk)"),
        ("merchant_category_vs_history", "String", "Alignment with cardholder typical purchasing category"),
        ("geo_velocity_kmh", "Double", "Apparent physical velocity between successive transactions"),
        ("geo_velocity_bin", "String", "Velocity category (normal, fast)"),
        ("geo_distance_km", "Double", "Physical distance in kilometers from cardholder billing location"),
        ("geo_distance_bin", "String", "Distance tier (same_location, intercity, etc.)"),
        ("merchant_location", "String", "Location context (home_city, same_country, foreign)"),
        ("country_consistency", "String", "Country alignment indicator against issuing bank origin"),
        ("ip_address_type", "String", "Network classification (residential, corporate, datacenter)"),
        ("device_fingerprint_match", "String", "Hardware device fingerprint status (known_device, new_device)"),
        ("session_duration_sec", "Double", "Digital checkout duration in seconds"),
        ("session_duration_bin", "String", "Checkout duration category (fast, normal, slow)"),
        ("network_carrier_type", "String", "Telecommunication network type (wifi, mobile_data, datacenter)"),
        ("cards_on_device_30d", "Integer", "Count of distinct payment cards bound to device within 30 days"),
        ("cvv_match_status", "String", "CVV2/iCVV card security code match status"),
        ("three_ds_auth_result", "String", "3D-Secure authentication outcome (frictionless_pass, challenge_fail)"),
        ("tokenization_used", "String", "PAN tokenization format (emv_chip_token, raw_pan_online)"),
        ("failed_attempts_before_success", "Integer", "Count of failed authentication attempts preceding transaction"),
        ("transaction_velocity_1h", "String", "Rolling 1-hour transaction frequency indicator"),
        ("time_of_transaction", "String", "Diurnal time bracket (late_night_0_5, afternoon_12_18, etc.)"),
        ("account_credential_change_recency", "String", "Proximity of password/MFA update (no_recent_change, recent)"),
        ("card_present_cnp", "String", "Payment channel format (card_present_swipe, cnp_online, cnp_moto)"),
        ("order_shipping_speed", "String", "Logistical delivery speed (same_day, overnight, standard)"),
        ("account_age_days", "Integer", "Customer account age in days"),
        ("chargeback_history_count", "Integer", "Historical chargeback disputes associated with account"),
        ("customer_id", "String", "Unique cardholder identifier (Excluded from ML predictors)"),
        ("transaction_id", "String", "Unique transaction key (Excluded from ML predictors)"),
        ("segment", "String", "Customer demographic spending tier (A_established, etc.)"),
        ("customer_type", "String", "Behavioral segment classification (customer_based)"),
        ("is_fraud", "Integer", "Ground-truth fraud label (0 = Legitimate, 1 = Fraudulent)")
    ]

    t_schema = doc.add_table(rows=len(schema_data), cols=3)
    for r_idx, row in enumerate(schema_data):
        for c_idx, val in enumerate(row):
            t_schema.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_schema, col_widths=[2.0, 1.3, 3.2])

    # 4. SYSTEM REQUIREMENTS AND ARCHITECTURE
    add_heading_1("4. SYSTEM REQUIREMENTS AND ARCHITECTURE")
    add_body(
        "The system architecture employs a decoupled layered design separating raw storage, distributed computing, ML pipeline execution, "
        "and analytical reporting. This modularity ensures storage layers can transition seamlessly between local file systems and enterprise "
        "HDFS clusters without requiring modifications to analytical code."
    )
    add_bullet(" Ingests multi-gigabyte transaction streams, validates schema types, handles null values, and converts CSV into columnar format.", "Functional Capabilities:")
    add_bullet(" Distributed horizontal scalability via Spark partitions, deterministic idempotency via fixed random seeds, and sub-minute execution throughput.", "Non-Functional Attributes:")

    arch_data = [
        ("Architecture Layer", "Primary Responsibility", "Underlying Technology"),
        ("Raw Input Layer", "Immutable raw source file storage", "CSV on File System / HDFS"),
        ("Distributed Ingestion", "Parallel reading, schema enforcement, snappy compression", "Apache Spark 3.5.4 (PySpark)"),
        ("Data Transformation", "Data cleansing, whitespace trimming, deduplication", "Spark SQL / Catalyst Optimizer"),
        ("Columnar Storage", "High-performance intermediate analytical layers", "Apache Parquet (Snappy)"),
        ("Risk Intelligence", "Quantile thresholding, frequency profiling, scoring", "PySpark Functions & Arrays"),
        ("Machine Learning", "Model training, pipeline assembly, metric evaluation", "Spark MLlib (Milestone 3)"),
        ("Presentation Layer", "Analytical metrics, distribution reporting, visualizations", "Pandas, Matplotlib, CSV exports")
    ]
    t_arch = doc.add_table(rows=len(arch_data), cols=3)
    for r_idx, row in enumerate(arch_data):
        for c_idx, val in enumerate(row):
            t_arch.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_arch, col_widths=[1.8, 2.7, 2.0])

    # 5. DEVELOPMENT ENVIRONMENT
    add_heading_1("5. DEVELOPMENT ENVIRONMENT AND VERIFIED STACK")
    add_body(
        "During setup, environment compatibility testing revealed that Apache Spark 3.5.x encounters known socket inheritance and security "
        "exceptions when paired with Java 25 or Python 3.12+ in local Windows mode (specifically JEP 486 Security Manager removal and SPARK-53759). "
        "To establish rock-solid stability, the environment was configured with the industry-standard LTS toolchain:"
    )
    env_data = [
        ("Component", "Installed Version", "Configuration / Path"),
        ("Operating System", "Microsoft Windows 11 (64-bit)", "Local Development Workstation"),
        ("Java Runtime (JDK)", "Microsoft OpenJDK 17.0.21 LTS", "C:\\Program Files\\Microsoft\\jdk-17.0.21.21-hotspot"),
        ("Python Environment", "Python 3.11.9 (64-bit)", "Dedicated project virtual environment (.venv)"),
        ("Hadoop Binaries", "Apache Hadoop 3.3.5 Windows Client", "hadoop/bin (winutils.exe, hadoop.dll)"),
        ("Apache Spark", "PySpark 3.5.4", "Local standalone mode (16 worker threads)"),
        ("Memory Allocation", "Driver: 6 GB | Executor: 6 GB", "Configured in pipeline/common.py"),
        ("Data Manipulation", "pandas 2.3.3, pyarrow 26.0.0", "Fast columnar dataframe bridges"),
        ("Plotting Engine", "matplotlib 3.11.2", "High-resolution metric chart generator")
    ]
    t_env = doc.add_table(rows=len(env_data), cols=3)
    for r_idx, row in enumerate(env_data):
        for c_idx, val in enumerate(row):
            t_env.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_env, col_widths=[1.8, 2.2, 2.5])

    # 6. DATA INGESTION
    add_heading_1("6. DATA INGESTION AND DISTRIBUTED STORAGE PIPELINE")
    add_body(
        "Repeatedly parsing 5.01 GB of raw CSV text creates severe I/O bottlenecks. In Stage 1 (pipeline/01_ingest.py), Spark loaded the "
        "entire dataset across 38 tasks and wrote the data out to results/raw in Snappy-compressed Apache Parquet format. "
        "Parquet organizes data by columns rather than rows, allowing downstream transformations and model-training jobs to read only the "
        "necessary features without scanning the full file. The operation completed with exit code 0."
    )

    # 7. DATA UNDERSTANDING
    add_heading_1("7. DATA UNDERSTANDING AND QUALITY ASSESSMENT")
    add_body(
        "Data quality assessment executed on the full 15,000,000 records confirmed complete data integrity. Crucially, the target label "
        "is_fraud exhibited 0 null or missing records. The transaction identifiers transaction_id and customer_id were confirmed to have high "
        "cardinality and were designated as excluded features in config/project_config.json to prevent target leakage."
    )

    # 8. DATA PREPROCESSING
    add_heading_1("8. DATA PREPROCESSING AND TRANSFORMATION LAYER")
    add_body(
        "Stage 2 (pipeline/02_transform.py) implemented comprehensive data hygiene: (1) trimming leading/trailing whitespace across all string "
        "fields; (2) dropping duplicate records across all 34 dimensions via dropDuplicates(); and (3) validating that every transaction possesses "
        "a valid ground-truth label. The cleaned dataset was written to results/cleaned, preserving all 15,000,000 rows across 34 columns."
    )

    # 9. FRAUD DETECTION ALGORITHMS
    add_heading_1("9. FRAUD DETECTION ALGORITHMS (PLANNED FOR MILESTONE 3)")
    add_body(
        "The project includes pipeline definitions for five candidate classification algorithms in Spark MLlib: "
        "Logistic Regression, Decision Tree Classifier, Random Forest Classifier, Gradient-Boosted Trees (GBT), and Linear SVM. "
        "Per Milestone 2 requirements, model training was deferred to Milestone 3 to focus computational resources on data engineering and "
        "explainable risk intelligence."
    )

    # 10. RISK SCORING INTELLIGENCE
    add_heading_1("10. RISK SCORING INTELLIGENCE AND EXPLAINABILITY")
    add_body(
        "In Stage 3 (pipeline/03_risk_analysis.py), a transparent rule-based risk intelligence engine was deployed to provide auditable transaction "
        "prioritization. Rather than relying on hardcoded static limits, the engine dynamically computed dataset-specific statistical thresholds:"
    )
    add_bullet(" Assigned to all transactions (BASELINE_REVIEW).", "1. Baseline Review Points (10.0 pts):")
    add_bullet(" Computed via approxQuantile('transaction_amount', [0.90], 0.01) across 15M records. Transactions in the top 10% receive +30.0 points and reason code AMOUNT_TOP_DECILE.", "2. Top-Decile Monetary Amount (+30.0 pts):")
    add_bullet(" Aggregated transaction counts per merchant category. Categories representing <5% of volume receive +20.0 points and reason code RARE_PROFILE.", "3. Rare Profile Category (+20.0 pts):")
    add_bullet(" Low (Score < 35), Medium (35 <= Score < 70), High (Score >= 70).", "4. Risk Category Bands:")

    # 13. IMPLEMENTATION WORKFLOW AUDIT
    add_heading_1("13. IMPLEMENTATION WORKFLOW AND EXECUTION STATUS")
    add_body("The table below presents the verified execution log of all modules executed in Milestone 2:")

    exec_data = [
        ("Stage", "Script Name", "Input Source", "Output Artifact", "Verified Status"),
        ("Stage 0", "00_inspect_schema.py", "credit_card_fraud.csv", "results/schema_report.json", "SUCCESS (Code 0)"),
        ("Stage 1", "01_ingest.py", "credit_card_fraud.csv", "results/raw/ (Parquet)", "SUCCESS (Code 0)"),
        ("Stage 2", "02_transform.py", "results/raw/", "results/cleaned/ (Parquet)", "SUCCESS (Code 0)"),
        ("Stage 3", "03_risk_analysis.py", "results/cleaned/", "results/risk_scored/, risk_category_summary.csv", "SUCCESS (Code 0)"),
        ("Stage 4", "04_train_models.py", "results/cleaned/", "results/models/", "Scheduled for Milestone 3"),
        ("Stage 5", "05_evaluate.py", "model_metrics.csv", "results/plots/", "Scheduled for Milestone 3")
    ]
    t_exec = doc.add_table(rows=len(exec_data), cols=5)
    for r_idx, row in enumerate(exec_data):
        for c_idx, val in enumerate(row):
            t_exec.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_exec, col_widths=[1.0, 1.6, 1.4, 1.5, 1.0])

    # 14. RESULTS & REPORTING
    add_heading_1("14. MEASURED RESULTS, RISK DISTRIBUTION AND REPORTING")
    add_body(
        "Stage 3 produced the verified risk categorization summary exported to results/risk_category_summary.csv. "
        "The complete 15,000,000 transaction distribution is detailed below:"
    )

    risk_data = [
        ("Assigned Risk Band", "Scored Transactions", "Percentage Share (%)", "Operational Action Recommendation"),
        ("LOW Risk (< 35 pts)", "13,467,586", "89.78%", "Standard automated payment clearance; no manual review"),
        ("MEDIUM Risk (35–69 pts)", "1,532,414", "10.22%", "Secondary authentication / investigator triage priority"),
        ("HIGH Risk (>= 70 pts)", "0", "0.00%", "Immediate temporary hold (multi-factor trigger threshold)"),
        ("Total Scored", "15,000,000", "100.00%", "Complete dataset successfully evaluated and scored")
    ]
    t_risk = doc.add_table(rows=len(risk_data), cols=4)
    for r_idx, row in enumerate(risk_data):
        for c_idx, val in enumerate(row):
            t_risk.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_risk, col_widths=[1.8, 1.5, 1.4, 1.8])

    add_body(
        "Key Finding: The rule-based risk intelligence engine successfully isolated exactly 10.22% of total transaction volume "
        "(1,532,414 transactions) as requiring elevated review due to top-decile spending deviations or rare merchant sector profiles. "
        "This triage directly reduces the manual investigation burden by almost 90% while ensuring high-value anomalies are highlighted."
    )

    # 15. TESTING & LIMITATIONS
    add_heading_1("15. TESTING, LIMITATIONS AND RISK MANAGEMENT")
    add_bullet(" Verified Spark worker execution on Python 3.11 with Microsoft OpenJDK 17 LTS, resolving all Java 25 / Python 3.12 compatibility defects.", "Worker Stability:")
    add_bullet(" Successfully validated writing and reading Snappy-compressed Parquet files via Hadoop 3.3.5 winutils.", "I/O Validation:")
    add_bullet(" Confirmed exact conservation of 15,000,000 records across raw, cleaned, and risk-scored Parquet layers.", "Record Conservation:")

    # 16. TEAM CONTRIBUTIONS
    add_heading_1("16. TEAM CONTRIBUTIONS AND PROJECT MANAGEMENT")
    contrib_data = [
        ("Team Member", "Roll Number", "Key Contributions & Milestone 2 Deliverables"),
        ("Srikashyap Amaravadi", "S24CSEU1423", "Project coordination, architecture design, JVM & Spark session configuration, report compilation"),
        ("Gitesh Goyal", "S24CSEU0774", "Dataset verification, Stage 0 schema discovery, Stage 1 distributed Parquet ingestion"),
        ("Annya Sharma", "S24CSEU1408", "Data quality profiling, missing-value analysis, Stage 2 transformation & deduplication"),
        ("Ajitej Singh", "S24CSEU1413", "Stage 3 risk scoring implementation, quantile calculation, reason codes & summary generation")
    ]
    t_contrib = doc.add_table(rows=len(contrib_data), cols=3)
    for r_idx, row in enumerate(contrib_data):
        for c_idx, val in enumerate(row):
            t_contrib.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_contrib, col_widths=[1.8, 1.3, 3.4])

    # 17. CONCLUSION
    add_heading_1("17. CONCLUSION AND FUTURE ROADMAP")
    add_body(
        "Milestone 2 has successfully achieved all data engineering, schema discovery, distributed ingestion, data hygiene, and explainable "
        "risk intelligence goals. Over 15 million transactions were processed through Apache Spark 3.5.4, converting a 5.01 GB raw CSV into "
        "compact, high-performance Parquet datasets."
    )
    add_heading_2("Roadmap for Milestone 3 (Final Milestone):")
    add_bullet(" Train and serialize all 5 Spark MLlib classifiers (Logistic Regression, Decision Tree, Random Forest, GBT, Linear SVM).", "1. Machine Learning Training:")
    add_bullet(" Compute precision, recall, F1-scores, ROC-AUC curves, and confusion matrices using 05_evaluate.py.", "2. Model Evaluation Benchmarks:")
    add_bullet(" Merge ML fraud probabilities with rule-based risk scores for multi-layered fraud defense.", "3. Hybrid Intelligence:")

    # 18. REFERENCES
    add_heading_1("18. REFERENCES")
    refs = [
        "1. CreditTransAct: A Profile-Driven Dataset for Scalable Credit Card Fraud Detection, Mendeley Data, Version 1, 9 May 2026. DOI: 10.17632/y64bbnm2s3.1. https://data.mendeley.com/datasets/y64bbnm2s3/1",
        "2. Apache Spark 3.5.4 Documentation: https://spark.apache.org/docs/3.5.4/",
        "3. Apache Hadoop 3.3.5 Documentation: https://hadoop.apache.org/docs/r3.3.5/",
        "4. Apache Spark MLlib Programming Guide: https://spark.apache.org/docs/3.5.4/ml-guide.html",
        "5. Python 3.11 Documentation: https://docs.python.org/3.11/",
        "6. Scikit-learn User Guide – Model Evaluation: https://scikit-learn.org/stable/modules/model_evaluation.html"
    ]
    for ref in refs:
        add_body(ref)

    # Save
    doc.save(output_path)
    print(f"Document successfully created and saved to: {output_path}")

if __name__ == "__main__":
    out_dir = Path(r"C:\Users\kashy\OneDrive\Desktop")
    out_file = out_dir / "CreditTransAct_Fraud_Analytics_Milestone_2_Report.docx"
    build_docx(str(out_file))
