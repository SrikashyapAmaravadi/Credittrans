import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

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
    
    # Page setup
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
        p.paragraph_format.space_before = Pt(30)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(22)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(15)
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
        run.font.size = Pt(12.5)
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
    # TITLE PAGE
    # ==========================
    logo_path = ROOT / 'results' / 'bennett_logo.png'
    if logo_path.exists():
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(12)
        doc.add_picture(str(logo_path), width=Inches(1.8))
        # Center the picture
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("BENNETT UNIVERSITY\n")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(18)
    r_inst.font.bold = True
    r_inst.font.color.rgb = NAVY

    r_dept = p_inst.add_run("SCHOOL OF COMPUTER SCIENCE ENGINEERING & TECHNOLOGY\n\n")
    r_dept.font.name = "Calibri"
    r_dept.font.size = Pt(12)
    r_dept.font.bold = True
    r_dept.font.color.rgb = SLATE

    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_badge = p_badge.add_run("COMPREHENSIVE PROJECT REPORT — MILESTONE 3 & FINAL ASSESSMENT\n\n")
    r_badge.font.name = "Calibri"
    r_badge.font.size = Pt(13)
    r_badge.font.bold = True
    r_badge.font.color.rgb = RGBColor(197, 48, 48)

    add_title("SCALABLE FINANCIAL FRAUD DETECTION AND RISK INTELLIGENCE USING APACHE SPARK, HADOOP AND MACHINE LEARNING")

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(20)
    r_course = p_course.add_run("Course: CSET371 — Big Data Analytics and Business Intelligence\nAcademic Year: 2026\nProject Faculty Guide: Dr. Aditya Bhardwaj")
    r_course.font.name = "Calibri"
    r_course.font.size = Pt(11)
    r_course.font.italic = True
    r_course.font.color.rgb = SLATE

    # Student table with role specialization as per guide instructions
    team_data = [
        ("Candidate Name", "Roll Number", "Specialized Responsibilities & Deliverables"),
        ("Srikashyap Amaravadi", "S24CSEU1423", "Architecture Design, Spark Session Tuning, Linear SVM/RF Implementation, Web Server"),
        ("Gitesh Goyal", "S24CSEU0774", "Deep/ML Model Implementation (GBT, LR, DT), Hyperparameter Optimization & Model Validation"),
        ("Annya Sharma", "S24CSEU1408", "Data Profiling, Missing Value Analysis, Preprocessing Pipeline, StringIndexer/OHE Design"),
        ("Ajitej Singh", "S24CSEU1413", "Heuristic Risk Engine, Operational 4-Tier Hybrid Triage Engine, Power BI Modeling & Report")
    ]
    t_team = doc.add_table(rows=len(team_data), cols=3)
    for r_idx, row in enumerate(team_data):
        for c_idx, val in enumerate(row):
            t_team.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_team, col_widths=[1.8, 1.3, 3.4])

    doc.add_page_break()

    # ==========================
    # DECLARATION & PLAGIARISM
    # ==========================
    add_heading_1("DECLARATION OF ORIGINALITY AND PLAGIARISM COMPLIANCE")
    add_body(
        "We hereby declare that this project report entitled 'Scalable Financial Fraud Detection and Risk Intelligence Using Apache Spark, "
        "Hadoop and Machine Learning' is an authentic record of our own research and engineering work undertaken under the supervision of "
        "Dr. Aditya Bhardwaj, School of Computer Science Engineering and Technology, Bennett University."
    )
    add_body(
        "All data pipelines, transformation algorithms, machine learning models, and hybrid operational triage engines presented herein were "
        "executed and evaluated directly on our execution environment. No generative-AI illustrations or synthetic performance metrics have "
        "been fabricated; all diagrams and heatmaps reflect verified empirical measurements. Plagiarism policies of the University and ethical standards "
        "have been rigorously maintained."
    )

    # ==========================
    # EXECUTIVE SUMMARY
    # ==========================
    add_heading_1("EXECUTIVE SUMMARY")
    add_body(
        "Digital payment infrastructures process astronomical transaction volumes under severe class imbalance (~4.90% fraud). Single-machine workflows "
        "suffer memory bottlenecks when processing multi-gigabyte datasets. This project delivers an end-to-end distributed Big Data and Machine Learning "
        "architecture built with Apache Spark 3.5.4, Apache Hadoop 3.3.5, and Python 3.11, empirically validated on the 5.01 GB CreditTransAct dataset (15,000,000 transactions)."
    )
    add_callout(
        "Empirical Highlight: Linear SVM and Random Forest achieved peak performance with an F1-Score of 0.9898 and Precision of 99.97% on unseen test data, "
        "while the hybrid triage engine achieved automated clearance for 95.23% of transactions and blocked 97.59% of fraudulent attempts instantly.",
        title="EMPIRICAL HIGHLIGHT"
    )

    # ==========================
    # CHAPTER 1: INTRODUCTION & PROPOSED METHODOLOGY
    # ==========================
    add_heading_1("CHAPTER 1: INTRODUCTION AND PROPOSED METHODOLOGY")
    add_body(
        "Modern payment networks require real-time fraud defense that combines high recall (catching subtle fraud attempts) with exceptional precision "
        "(preventing false declines on legitimate cardholders). Our proposed methodology addresses this using a distributed multi-stage architecture."
    )
    add_heading_2("1.1 Proposed Methodology Architecture Diagram")
    add_body("Figure 1.1 illustrates the end-to-end distributed Big Data and Machine Learning pipeline architecture:")
    add_image_safe(PLOTS_DIR / 'methodology_architecture.png', "Figure 1.1: Proposed Scalable Financial Fraud Analytics Methodology Architecture", width=Inches(6.2))

    # ==========================
    # CHAPTER 2: THEORETICAL FOUNDATION & BIG DATA FRAMEWORK
    # ==========================
    add_heading_1("CHAPTER 2: THEORETICAL FOUNDATION AND BIG DATA DISTRIBUTED FRAMEWORK")
    add_body(
        "Apache Spark provides a distributed memory-centric computing paradigm. Using Spark SQL DataFrames and the Catalyst query optimizer, "
        "transformations are converted into optimized execution graphs executed across 16 logical cores. Raw 5.01 GB CSV was transformed into Snappy-compressed "
        "columnar Apache Parquet partitions (results/raw), reducing storage footprint by 85% and eliminating repeated schema inference."
    )

    # ==========================
    # CHAPTER 3: DATASET PROFILING & PREPROCESSING METHODOLOGY
    # ==========================
    add_heading_1("CHAPTER 3: DATASET PROFILING AND PREPROCESSING METHODOLOGY")
    add_body(
        "The CreditTransAct benchmark dataset contains 15,000,000 records and 34 attributes. Target label is_fraud has zero missing values (14,264,776 legitimate, 735,224 fraud). "
        "Identifier attributes (customer_id, transaction_id) were strictly isolated to prevent target leakage."
    )
    add_heading_2("3.1 Preprocessing and Feature Engineering Methodology")
    add_body(
        "The data preparation methodology encompasses four deterministic steps: (1) Whitespace sanitation via F.trim(), (2) Full deduplication via dropDuplicates(), "
        "(3) Categorical indexing via StringIndexer with handleInvalid='keep' and OneHotEncoder sparse representation, and (4) VectorAssembler aggregation combining 9 numeric "
        "and 22 one-hot encoded vector columns."
    )
    add_image_safe(PLOTS_DIR / 'preprocessing_methodology.png', "Figure 3.1: Step-by-Step Data Preprocessing and Feature Engineering Workflow", width=Inches(6.2))

    # ==========================
    # CHAPTER 4: DISTRIBUTED MACHINE LEARNING & HYPERPARAMETER TUNING
    # ==========================
    add_heading_1("CHAPTER 4: DISTRIBUTED MACHINE LEARNING AND HYPERPARAMETER TUNING")
    add_body(
        "As directed in project guidelines (Comment 11), Srikashyap Amaravadi and Gitesh Goyal implemented and validated 5 distributed machine learning algorithms "
        "in Spark MLlib: Linear Support Vector Machine (Linear SVM), Random Forest Classifier, Gradient-Boosted Trees (GBT), Logistic Regression, and Decision Tree."
    )
    add_heading_2("4.1 Hyperparameter Tuning Framework")
    add_body(
        "Tuning sweeps balanced generalization against memory constraints: Linear SVM configured with L2 regParam=0.01; Random Forest with 50 trees, maxDepth=8, "
        "featureSubset=sqrt; GBT with 30 iterations, stepSize=0.1, maxDepth=5; Logistic Regression with L2 ElasticNet; and Decision Tree with maxDepth=8."
    )
    add_image_safe(PLOTS_DIR / 'hyperparameter_tuning_flow.png', "Figure 4.1: Distributed Model Training and Hyperparameter Tuning Framework", width=Inches(6.2))

    add_heading_2("4.2 Model Performance Visualizations")
    add_body("Below are the graphical visualization results of the implemented models evaluated on 300,296 unseen holdout records:")
    add_image_safe(PLOTS_DIR / 'overall_model_comparison.png', "Figure 4.2: Overall Model Performance Comparison (Precision, Recall, F1, and ROC-AUC)", width=Inches(5.8))
    add_image_safe(PLOTS_DIR / 'roc_auc_comparison.png', "Figure 4.3: Area Under ROC Curve (ROC-AUC) Comparison", width=Inches(5.2))
    add_image_safe(PLOTS_DIR / 'f1_comparison.png', "Figure 4.4: F1-Score Harmonic Mean Comparison", width=Inches(5.2))

    # ==========================
    # CHAPTER 5: EMPIRICAL RESULTS & CONFUSION MATRICES
    # ==========================
    add_heading_1("CHAPTER 5: EMPIRICAL RESULTS, CONFUSION MATRICES AND BENCHMARK ANALYSIS")
    add_body(
        "All models were evaluated on the 20% holdout test partition containing 14,513 actual fraud events and 285,783 legitimate transactions:"
    )

    perf_data = [
        ("Algorithm", "Precision", "Recall", "F1-Score", "ROC-AUC", "TP", "FP", "FN", "TN"),
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

    add_heading_2("5.1 Confusion Matrix Visualizations")
    add_body("Confusion matrix heatmaps for the evaluated classifiers on 300,296 transactions:")
    add_image_safe(PLOTS_DIR / 'confusion_LinearSVM.png', "Figure 5.1: Linear SVM Confusion Matrix (14,224 TP, 5 FP, 289 FN, 285,778 TN)", width=Inches(4.4))
    add_image_safe(PLOTS_DIR / 'confusion_RandomForest.png', "Figure 5.2: Random Forest Confusion Matrix (14,044 TP, 4 FP, 469 FN, 285,779 TN)", width=Inches(4.4))
    add_image_safe(PLOTS_DIR / 'confusion_LogisticRegression.png', "Figure 5.3: Logistic Regression Confusion Matrix", width=Inches(4.4))

    # ==========================
    # CHAPTER 6: EXPLAINABLE HEURISTIC SCORING & HYBRID TRIAGE
    # ==========================
    add_heading_1("CHAPTER 6: EXPLAINABLE HEURISTIC SCORING AND OPERATIONAL TRIAGE ENGINE")
    add_body(
        "Engineered by Annya Sharma and Ajitej Singh, Stage 03 calculates empirical 90th percentile amount thresholds and rare merchant category shares, "
        "assigning auditable reason codes. Stage 06 merges these heuristic bands with model probabilities into an actionable 4-tier banking decision protocol."
    )

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
    # CHAPTER 7: POWER BI ENTERPRISE INTEGRATION
    # ==========================
    add_heading_1("CHAPTER 7: BUSINESS INTELLIGENCE AND POWER BI ENTERPRISE INTEGRATION")
    add_body(
        "To satisfy the Business Intelligence curriculum of CSET371, 5 star-schema CSV tables were generated (powerbi/data/) with complete DAX formulas "
        "for Fraud Detection Rate (Recall), False Alarm Rate, and Financial Loss Prevented."
    )

    # ==========================
    # CHAPTER 8: CONCLUSION & REFERENCES
    # ==========================
    add_heading_1("CHAPTER 8: CONCLUSION AND FUTURE ROADMAP")
    add_body(
        "The project has successfully fulfilled all 12 directives provided by the faculty guide. The distributed architecture seamlessly processed "
        "15,000,000 transactions, achieved an F1-Score of 0.9898 with Linear SVM, and delivered an operational hybrid triage engine that automatically clears "
        "95.23% of normal traffic while intercepting 97.59% of fraudulent attempts."
    )

    add_heading_1("REFERENCES")
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
