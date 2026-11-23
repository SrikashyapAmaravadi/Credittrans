import os
import shutil
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / 'docs'
PLOTS_DIR = ROOT / 'results' / 'plots'
LOGO_PATH = ROOT / 'results' / 'bennett_logo.png'

# Color Palette
NAVY = RGBColor(27, 54, 93)       # #1B365D Primary Dark
SLATE = RGBColor(74, 85, 104)     # #4A5568 Secondary Slate
CRIMSON = RGBColor(185, 28, 28)   # #B91C1C Accent Red
BLUE = RGBColor(14, 116, 144)     # #0E7490 Accent Blue
DARK = RGBColor(30, 41, 59)       # #1E293B Text Dark
LIGHT_BG = RGBColor(248, 250, 252)# #F8FAFC Card BG
WHITE = RGBColor(255, 255, 255)
GREEN = RGBColor(16, 149, 100)    # #109564 Success

def add_para_run(p, text, bold=False, size=10, color=DARK):
    r = p.add_run()
    r.text = text
    r.font.bold = bold
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.font.name = "Calibri"
    return r

def add_header(slide, title_text, category_text="CSET371 · BIG DATA ANALYTICS & BUSINESS INTELLIGENCE"):
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = BLUE
    p_c.font.name = "Calibri"
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.6))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY
    p_t.font.name = "Calibri"

def add_card(slide, left, top, width, height, bg_color=LIGHT_BG, border_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    return shape

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title & System Overview
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    
    if LOGO_PATH.exists():
        s1.shapes.add_picture(str(LOGO_PATH), Inches(0.8), Inches(0.6), width=Inches(1.2))
    
    tb = s1.shapes.add_textbox(Inches(2.2), Inches(0.55), Inches(10), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "CSET371 · BIG DATA ANALYTICS & BUSINESS INTELLIGENCE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE
    
    p2 = tb.text_frame.add_paragraph()
    p2.text = "CreditTransAct: Big Data Distributed Fraud Analytics"
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = NAVY
    
    p3 = tb.text_frame.add_paragraph()
    p3.text = "Multi-Tier Triage Decision Engine over 15 Million Transactions | Bennett University"
    p3.font.size = Pt(12)
    p3.font.color.rgb = SLATE

    kpis = [
        ("15,000,000", "Transactions Ingested", "5.01 GB Raw CSV to Parquet"),
        ("99.96%", "Linear SVM Precision", "Champion Model (5 FPs only)"),
        ("4.2 min", "Total Pipeline Runtime", "80% Speedup via RDD Caching"),
        ("95.23%", "Automated Clearance", "Zero Friction Checkout Flow")
    ]
    card_w = Inches(2.7)
    card_h = Inches(1.5)
    top_pos = Inches(1.8)
    for idx, (val, title, sub) in enumerate(kpis):
        left_pos = Inches(0.8 + idx * 2.95)
        add_card(s1, left_pos, top_pos, card_w, card_h, LIGHT_BG, BLUE)
        tb_kpi = s1.shapes.add_textbox(left_pos + Inches(0.15), top_pos + Inches(0.15), card_w - Inches(0.3), card_h - Inches(0.3))
        tf = tb_kpi.text_frame
        p_val = tf.paragraphs[0]
        p_val.text = val
        p_val.font.size = Pt(24)
        p_val.font.bold = True
        p_val.font.color.rgb = CRIMSON if idx == 1 else NAVY
        
        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = DARK
        
        p_s = tf.add_paragraph()
        p_s.text = sub
        p_s.font.size = Pt(9.5)
        p_s.font.color.rgb = SLATE

    add_card(s1, Inches(0.8), Inches(3.6), Inches(11.7), Inches(3.2), LIGHT_BG)
    tb_team = s1.shapes.add_textbox(Inches(1.1), Inches(3.75), Inches(11), Inches(2.8))
    tf_team = tb_team.text_frame
    p_th = tf_team.paragraphs[0]
    p_th.text = "CORE ENGINEERING TEAM & TECHNICAL ROLES (FACULTY GUIDE: DR. ADITYA BHARDWAJ)"
    p_th.font.size = Pt(12)
    p_th.font.bold = True
    p_th.font.color.rgb = NAVY

    team_members = [
        ("Srikashyap Amaravadi (S24CSEU1423)", "Lead Big Data Engineer & Classifier Architect", "Distributed PySpark MLlib Pipeline, Linear SVM & Random Forest, REST API Simulator"),
        ("Gitesh Goyal (S24CSEU0774)", "ML Optimization Engineer & Schema Discovery Lead", "Schema Discovery across 34 attributes, GBT, Logistic Regression, Decision Tree Grid Search"),
        ("Annya Sharma (S24CSEU1408)", "Data Hygiene & Feature Pipeline Engineering Lead", "Distributed Parquet Ingestion (5.01 GB), PCI-DSS Sanitization, VectorAssembler Feature Pipeline"),
        ("Ajitej Singh (S24CSEU1413)", "Risk Intelligence, Evaluation Analytics & Visualization Lead", "Domain Heuristic Risk Engine, 4-Tier Hybrid Triage Matrix, Evaluation Curves & Dashboard")
    ]
    for name, role, work in team_members:
        p_m = tf_team.add_paragraph()
        p_m.space_before = Pt(6)
        add_para_run(p_m, f"• {name}: ", bold=True, size=11, color=DARK)
        add_para_run(p_m, f"{role} — ", bold=True, size=10.5, color=BLUE)
        add_para_run(p_m, work, bold=False, size=10, color=SLATE)

    # =========================================================================
    # SLIDE 2: Problem Domain & Big Data Scale Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Domain Identification & Big Data Scale Challenges")

    add_card(s2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), LIGHT_BG)
    tb_p = s2.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.8))
    tf_p = tb_p.text_frame
    p_ph = tf_p.paragraphs[0]
    p_ph.text = "THE FINANCIAL FRAUD PARADOX"
    p_ph.font.size = Pt(14)
    p_ph.font.bold = True
    p_ph.font.color.rgb = CRIMSON

    p_p1 = tf_p.add_paragraph()
    p_p1.space_before = Pt(8)
    p_p1.text = "• Massive Velocity: Over $5.8 Trillion in digital transactions globally. Systems must authorize or decline transactions within 100 milliseconds."
    p_p1.font.size = Pt(11)
    p_p1.font.color.rgb = DARK

    p_p2 = tf_p.add_paragraph()
    p_p2.space_before = Pt(8)
    p_p2.text = "• Extreme Class Imbalance: Legitimate transactions represent 95.10% (14.26M rows), while fraud is only 4.90% (735k rows). Naive accuracy models completely fail."
    p_p2.font.size = Pt(11)
    p_p2.font.color.rgb = DARK

    p_p3 = tf_p.add_paragraph()
    p_p3.space_before = Pt(8)
    p_p3.text = "• The Cost of False Positives: Declining genuine cardholders destroys customer lifetime value and causes immediate checkout abandonment."
    p_p3.font.size = Pt(11)
    p_p3.font.color.rgb = DARK

    add_card(s2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3), LIGHT_BG)
    tb_s = s2.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf_s = tb_s.text_frame
    p_sh = tf_s.paragraphs[0]
    p_sh.text = "WHY DISTRIBUTED BIG DATA (SPARK)?"
    p_sh.font.size = Pt(14)
    p_sh.font.bold = True
    p_sh.font.color.rgb = NAVY

    p_s1 = tf_s.add_paragraph()
    p_s1.space_before = Pt(8)
    p_s1.text = "• Single-Machine Memory Ceiling: Standard Python (Scikit-Learn/Pandas) crashes with Out-Of-Memory (OOM) errors on 5.01 GB / 15M records."
    p_s1.font.size = Pt(11)
    p_s1.font.color.rgb = DARK

    p_s2 = tf_s.add_paragraph()
    p_s2.space_before = Pt(8)
    p_s2.text = "• Snappy Columnar Parquet: Ingestion into partitioned Parquet reduces disk footprint and increases query scan speed by 6.8x."
    p_s2.font.size = Pt(11)
    p_s2.font.color.rgb = DARK

    p_s3 = tf_s.add_paragraph()
    p_s3.space_before = Pt(8)
    p_s3.text = "• 4-Tier Operational Triage: Replaces rigid binary approve/decline with Automated Block, Step-Up MFA, Analyst Review, and Frictionless Clearance."
    p_s3.font.size = Pt(11)
    p_s3.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 3: System & Methodology Architecture Diagram
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "CreditTransAct Proposed System & Methodology Architecture")
    
    arch_img = PLOTS_DIR / "methodology_architecture.png"
    if arch_img.exists():
        s3.shapes.add_picture(str(arch_img), Inches(0.8), Inches(1.4), width=Inches(11.7))

    # =========================================================================
    # SLIDE 4: Srikashyap Amaravadi — Individual Technical Contribution
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Srikashyap Amaravadi (S24CSEU1423) — MLlib & REST API Architecture")

    add_card(s4, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4), LIGHT_BG)
    tb_sri = s4.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.6), Inches(5.1))
    tf_sri = tb_sri.text_frame
    p_sh = tf_sri.paragraphs[0]
    p_sh.text = "CORE TECHNICAL OWNERSHIP"
    p_sh.font.size = Pt(13)
    p_sh.font.bold = True
    p_sh.font.color.rgb = NAVY

    items_sri = [
        ("Owned Modules", "pipeline/04_train_models.py, server.py, batch launchers"),
        ("Champion Linear SVM", "Trained LinearSVC with Hinge Loss + L2 Regularization (regParam=0.05, maxIter=100) yielding 99.96% Precision & 0.9898 F1-Score."),
        ("Random Forest Ensemble", "Trained 50-tree bagging model with random feature subsampling (m=sqrt(p)), yielding lowest false alarms (only 4 FPs)."),
        ("Live Multi-Threaded REST API", "Built Python HTTP server (socketserver.ThreadingMixIn) serving /api/predict, /api/metrics, and /api/triage in <12ms."),
        ("Real-Time Haversine Distance", "Implemented spherical geodesic math calculating customer-to-merchant distance anomalies on incoming live transactions.")
    ]
    for title, desc in items_sri:
        p_item = tf_sri.add_paragraph()
        p_item.space_before = Pt(6)
        add_para_run(p_item, f"• {title}: ", bold=True, size=11, color=DARK)
        add_para_run(p_item, desc, bold=False, size=10, color=SLATE)

    add_card(s4, Inches(7.1), Inches(1.4), Inches(5.4), Inches(5.4), LIGHT_BG)
    tb_brk = s4.shapes.add_textbox(Inches(7.3), Inches(1.55), Inches(5.0), Inches(5.1))
    tf_brk = tb_brk.text_frame
    p_bh = tf_brk.paragraphs[0]
    p_bh.text = "PIPELINE CACHING BREAKTHROUGH"
    p_bh.font.size = Pt(13)
    p_bh.font.bold = True
    p_bh.font.color.rgb = CRIMSON

    p_b1 = tf_brk.add_paragraph()
    p_b1.space_before = Pt(8)
    p_b1.text = "The Bottleneck:\nSpark was lazily re-fitting 22 StringIndexer stages on 12,000,000 rows for every model, taking ~2 Hours and causing JVM memory spills."
    p_b1.font.size = Pt(10.5)
    p_b1.font.color.rgb = DARK

    add_card(s4, Inches(7.4), Inches(3.0), Inches(4.8), Inches(1.5), NAVY)
    tb_code = s4.shapes.add_textbox(Inches(7.5), Inches(3.1), Inches(4.6), Inches(1.3))
    tf_code = tb_code.text_frame
    p_c1 = tf_code.paragraphs[0]
    p_c1.text = "RUNTIME OPTIMIZATION"
    p_c1.font.size = Pt(10)
    p_c1.font.bold = True
    p_c1.font.color.rgb = WHITE
    p_c2 = tf_code.add_paragraph()
    p_c2.text = "2 Hours  →  4.2 Minutes (80% Speedup)"
    p_c2.font.size = Pt(13)
    p_c2.font.bold = True
    p_c2.font.color.rgb = RGBColor(56, 189, 248)
    p_c3 = tf_code.add_paragraph()
    p_c3.text = "train_vec = feat_pipe.fit(train).transform(train).cache()\ntrain_vec.count()  # Materialized to RAM"
    p_c3.font.size = Pt(8.5)
    p_c3.font.color.rgb = WHITE

    p_b2 = tf_brk.add_paragraph()
    p_b2.space_before = Pt(115)
    p_b2.text = "Tuned Py4J Gateway & Socket Binding:\nResolved Windows socket permission error (WinError 10013) and set shuffle.partitions=64 to maximize multi-threaded CPU throughput."
    p_b2.font.size = Pt(10.5)
    p_b2.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 5: Gitesh Goyal — Individual Technical Contribution
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Gitesh Goyal (S24CSEU0774) — Schema Discovery & Model Optimization")

    add_card(s5, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4), LIGHT_BG)
    tb_git = s5.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.6), Inches(5.1))
    tf_git = tb_git.text_frame
    p_gh = tf_git.paragraphs[0]
    p_gh.text = "TECHNICAL DELIVERABLES & MODULES"
    p_gh.font.size = Pt(13)
    p_gh.font.bold = True
    p_gh.font.color.rgb = NAVY

    items_git = [
        ("Owned Modules", "pipeline/00_inspect_schema.py, pipeline/04_train_models.py"),
        ("Schema Discovery", "Engineered distributed schema profiling across 34 raw attributes, generating results/schema_report.json without memory spills."),
        ("Gradient-Boosted Trees (GBT)", "Trained iterative boosting model minimizing binomial deviance via pseudo-residual regression (0.9831 F1-Score)."),
        ("Logistic Regression", "Trained elastic-net / L2 regularized log-odds model with quasi-Newton L-BFGS optimizer (0.9890 F1-Score, 0.9990 ROC-AUC)."),
        ("Decision Tree Classifier", "Implemented baseline single-tree greedy partitioning optimizing Gini Impurity (0.9783 F1-Score).")
    ]
    for title, desc in items_git:
        p_item = tf_git.add_paragraph()
        p_item.space_before = Pt(6)
        add_para_run(p_item, f"• {title}: ", bold=True, size=11, color=DARK)
        add_para_run(p_item, desc, bold=False, size=10, color=SLATE)

    add_card(s5, Inches(7.1), Inches(1.4), Inches(5.4), Inches(5.4), LIGHT_BG)
    tb_hparam = s5.shapes.add_textbox(Inches(7.3), Inches(1.55), Inches(5.0), Inches(5.1))
    tf_hparam = tb_hparam.text_frame
    p_hh = tf_hparam.paragraphs[0]
    p_hh.text = "HYPERPARAMETER GRID SEARCH METHODOLOGY"
    p_hh.font.size = Pt(13)
    p_hh.font.bold = True
    p_hh.font.color.rgb = BLUE

    grid_params = [
        ("Max Tree Depth", "5, 8, 10", "Controls tree complexity & prevents leaf overfitting"),
        ("Bin Discretization", "32, 64", "Balances split precision vs memory during histogram binning"),
        ("GBT Step Size (Eta)", "0.05, 0.1, 0.2", "Shrinkage rate per boosting round for stable convergence"),
        ("L2 Regularization", "0.01, 0.05, 0.1", "Penalizes large weights to maintain generalizability")
    ]
    for p_name, vals, impact in grid_params:
        p_p = tf_hparam.add_paragraph()
        p_p.space_before = Pt(8)
        add_para_run(p_p, f"{p_name} ({vals}):\n", bold=True, size=10.5, color=DARK)
        add_para_run(p_p, impact, bold=False, size=9.5, color=SLATE)

    # =========================================================================
    # SLIDE 6: Annya Sharma — Individual Technical Contribution
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Annya Sharma (S24CSEU1408) — Data Ingestion & Feature Engineering")

    add_card(s6, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4), LIGHT_BG)
    tb_ann = s6.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.6), Inches(5.1))
    tf_ann = tb_ann.text_frame
    p_ah = tf_ann.paragraphs[0]
    p_ah.text = "DATA HYGIENE & PREPROCESSING PIPELINE"
    p_ah.font.size = Pt(13)
    p_ah.font.bold = True
    p_ah.font.color.rgb = NAVY

    items_ann = [
        ("Owned Modules", "pipeline/01_ingest.py, pipeline/02_transform.py"),
        ("Distributed Ingestion", "Streamed raw 5.01 GB CSV into partitioned snappy Parquet in results/raw/, boosting I/O throughput by 6.8x."),
        ("PCI-DSS Security Isolation", "Stripped sensitive cardholder identifiers (cc_num, trans_num, first, last) into secure lookup tables to eliminate target leakage."),
        ("Data Cleaning & Standardization", "Handled null-imputation, categorical whitespace trimming, and demographic format standardization across 15M records."),
        ("Vector Pipeline Construction", "Constructed chained StringIndexer, OneHotEncoderEstimator, and VectorAssembler pipelines assembling the final feature vectors.")
    ]
    for title, desc in items_ann:
        p_item = tf_ann.add_paragraph()
        p_item.space_before = Pt(6)
        add_para_run(p_item, f"• {title}: ", bold=True, size=11, color=DARK)
        add_para_run(p_item, desc, bold=False, size=10, color=SLATE)

    add_card(s6, Inches(7.1), Inches(1.4), Inches(5.4), Inches(5.4), LIGHT_BG)
    tb_dist = s6.shapes.add_textbox(Inches(7.3), Inches(1.55), Inches(5.0), Inches(5.1))
    tf_dist = tb_dist.text_frame
    p_dh = tf_dist.paragraphs[0]
    p_dh.text = "PARTITION & CLASS DISTRIBUTION INTEGRITY"
    p_dh.font.size = Pt(13)
    p_dh.font.bold = True
    p_dh.font.color.rgb = BLUE

    p_d1 = tf_dist.add_paragraph()
    p_d1.space_before = Pt(8)
    p_d1.text = "15,000,000 Transaction Population Breakdown:"
    p_d1.font.size = Pt(11)
    p_d1.font.bold = True
    p_d1.font.color.rgb = DARK

    add_card(s6, Inches(7.3), Inches(2.6), Inches(5.0), Inches(1.0), NAVY)
    tb_leg = s6.shapes.add_textbox(Inches(7.4), Inches(2.7), Inches(4.8), Inches(0.8))
    tf_leg = tb_leg.text_frame
    p_l1 = tf_leg.paragraphs[0]
    p_l1.text = "Legitimate: 14,264,776 records (95.10%)"
    p_l1.font.size = Pt(12)
    p_l1.font.bold = True
    p_l1.font.color.rgb = WHITE
    p_l2 = tf_leg.add_paragraph()
    p_l2.text = "Smooth consumer purchases cleared without false alarms"
    p_l2.font.size = Pt(9.5)
    p_l2.font.color.rgb = RGBColor(203, 213, 225)

    add_card(s6, Inches(7.3), Inches(3.8), Inches(5.0), Inches(1.0), CRIMSON)
    tb_frd = s6.shapes.add_textbox(Inches(7.4), Inches(3.9), Inches(4.8), Inches(0.8))
    tf_frd = tb_frd.text_frame
    p_f1 = tf_frd.paragraphs[0]
    p_f1.text = "Fraudulent: 735,224 records (4.90%)"
    p_f1.font.size = Pt(12)
    p_f1.font.bold = True
    p_f1.font.color.rgb = WHITE
    p_f2 = tf_frd.add_paragraph()
    p_f2.text = "Active fraud attacks intercepted by classification tiers"
    p_f2.font.size = Pt(9.5)
    p_f2.font.color.rgb = RGBColor(254, 202, 202)

    # =========================================================================
    # SLIDE 7: Ajitej Singh — Individual Technical Contribution
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Ajitej Singh (S24CSEU1413) — Risk Intelligence & 4-Tier Triage")

    add_card(s7, Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.4), LIGHT_BG)
    tb_aji = s7.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.4), Inches(5.1))
    tf_aji = tb_aji.text_frame
    p_ajh = tf_aji.paragraphs[0]
    p_ajh.text = "HEURISTIC RISK ENGINE & VISUAL ANALYTICS"
    p_ajh.font.size = Pt(13)
    p_ajh.font.bold = True
    p_ajh.font.color.rgb = NAVY

    items_aji = [
        ("Owned Modules", "pipeline/03_risk_analysis.py, pipeline/05_evaluate.py, pipeline/06_hybrid_inference.py, results/dashboard.html"),
        ("Heuristic Scoring Formula", "RiskScore = Base(10) + AmtScore(30) + MerchScore(20) + Foreign(15) + Velocity(25)."),
        ("Empirical Visualization", "Generated 10+ analytical plots (ROC curves, PR curves, Confusion Matrices, Threshold sweeps) in results/plots/."),
        ("Interactive Dashboard Layout", "Designed responsive UI components, metric counters, and operational triage queue visualizers.")
    ]
    for title, desc in items_aji:
        p_item = tf_aji.add_paragraph()
        p_item.space_before = Pt(6)
        add_para_run(p_item, f"• {title}: ", bold=True, size=11, color=DARK)
        add_para_run(p_item, desc, bold=False, size=10, color=SLATE)

    add_card(s7, Inches(6.9), Inches(1.4), Inches(5.6), Inches(5.4), LIGHT_BG)
    tb_tri = s7.shapes.add_textbox(Inches(7.1), Inches(1.55), Inches(5.2), Inches(5.1))
    tf_tri = tb_tri.text_frame
    p_trh = tf_tri.paragraphs[0]
    p_trh.text = "4-TIER OPERATIONAL TRIAGE DECISION MATRIX"
    p_trh.font.size = Pt(13)
    p_trh.font.bold = True
    p_trh.font.color.rgb = CRIMSON

    tiers = [
        ("Tier 1: Critical Block (p >= 0.85)", "14,168 txns (14,163 actual fraud = 99.96% accuracy). Immediate card lock."),
        ("Tier 2: Step-Up MFA (0.50 <= p < 0.85)", "78 borderline txns challenged with automated biometric/SMS OTP."),
        ("Tier 3: Analyst Review (0.20 <= p < 0.50)", "87 moderate-risk txns routed to fraud investigation worklists."),
        ("Tier 4: Automated Clearance (p < 0.20)", "285,963 txns (95.23% of volume). 100% frictionless instant checkout.")
    ]
    for t_name, t_desc in tiers:
        p_t = tf_tri.add_paragraph()
        p_t.space_before = Pt(8)
        add_para_run(p_t, f"{t_name}:\n", bold=True, size=10.5, color=DARK)
        add_para_run(p_t, t_desc, bold=False, size=9.5, color=SLATE)

    # =========================================================================
    # SLIDE 8: 5-Model Comparative Benchmark Table
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Empirical Evaluation Benchmark (300,296 Unseen Test Records)")

    rows = 6
    cols = 9
    table_shape = s8.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.7), Inches(3.2))
    table = table_shape.table

    table_data = [
        ["Model Name", "Precision", "Recall", "F1-Score", "ROC-AUC", "TP", "FP", "FN", "TN"],
        ["Linear SVM (Champion)", "0.9996", "0.9801", "0.9898", "0.9980", "14,224", "5", "289", "285,778"],
        ["Random Forest", "0.9997", "0.9677", "0.9834", "0.9968", "14,044", "4", "469", "285,779"],
        ["Logistic Regression", "0.9988", "0.9794", "0.9890", "0.9990", "14,214", "17", "299", "285,766"],
        ["Gradient-Boosted Trees", "0.9991", "0.9675", "0.9831", "0.9906", "14,042", "13", "471", "285,770"],
        ["Decision Tree", "0.9977", "0.9597", "0.9783", "0.8567", "13,928", "32", "585", "285,751"]
    ]

    col_w = [Inches(2.5), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.2), Inches(1.0), Inches(1.0), Inches(1.6)]
    for idx, width in enumerate(col_w):
        table.columns[idx].width = width

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY
                p.font.bold = True
                p.font.size = Pt(11)
                p.font.color.rgb = WHITE
            elif r_idx == 1:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(238, 242, 255)
                p.font.bold = True
                p.font.size = Pt(10)
                p.font.color.rgb = CRIMSON if c_idx == 0 or c_idx == 1 else DARK
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = LIGHT_BG if r_idx % 2 == 1 else WHITE
                p.font.size = Pt(9.5)
                p.font.color.rgb = DARK

    add_card(s8, Inches(0.8), Inches(5.0), Inches(11.7), Inches(1.8), LIGHT_BG)
    tb_tak = s8.shapes.add_textbox(Inches(1.0), Inches(5.1), Inches(11.3), Inches(1.6))
    tf_tak = tb_tak.text_frame
    p_th = tf_tak.paragraphs[0]
    p_th.text = "KEY EMPIRICAL TAKEAWAYS:"
    p_th.font.size = Pt(12)
    p_th.font.bold = True
    p_th.font.color.rgb = NAVY

    p_t1 = tf_tak.add_paragraph()
    p_t1.space_before = Pt(4)
    p_t1.text = "1. Champion Model (Linear SVM): Reached 0.9898 F1 and 0.9996 Precision with only 5 false alarms out of 285,783 legitimate transactions."
    p_t1.font.size = Pt(10.5)
    p_t1.font.color.rgb = DARK

    p_t2 = tf_tak.add_paragraph()
    p_t2.space_before = Pt(4)
    p_t2.text = "2. Random Forest: Achieved the lowest absolute false positives (4 FPs), while Logistic Regression provided high sub-millisecond efficiency."
    p_t2.font.size = Pt(10.5)
    p_t2.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 9: Visual Results & Confusion Matrices
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Graphical Visualizations & Champion Confusion Matrix")

    comp_img = PLOTS_DIR / "overall_model_comparison.png"
    cm_img = PLOTS_DIR / "confusion_LinearSVM.png"
    
    if comp_img.exists():
        s9.shapes.add_picture(str(comp_img), Inches(0.8), Inches(1.4), width=Inches(6.8))
    if cm_img.exists():
        s9.shapes.add_picture(str(cm_img), Inches(7.9), Inches(1.4), width=Inches(4.6))

    # =========================================================================
    # SLIDE 10: Interactive Verification Interface & Live Simulator
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Fullstack Verification Dashboard & Real-Time REST API Simulator")

    add_card(s10, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.4), LIGHT_BG)
    tb_ui = s10.shapes.add_textbox(Inches(1.1), Inches(1.6), Inches(11.1), Inches(5.0))
    tf_ui = tb_ui.text_frame
    p_uh = tf_ui.paragraphs[0]
    p_uh.text = "INTERACTIVE PLATFORM HIGHLIGHTS (LOCALHOST:8000)"
    p_uh.font.size = Pt(14)
    p_uh.font.bold = True
    p_uh.font.color.rgb = NAVY

    ui_points = [
        ("Bennett University Branding", "Incorporated official Bennett University crest, formal color styling, and academic course identifiers directly in the UI header."),
        ("Dynamic KPI Counters", "Real-time cards displaying total dataset records (15.0M), active models trained (5), champion F1 (0.9898), and clearance percentage (95.23%)."),
        ("Live Fraud Simulator (/api/predict)", "Examiners can manipulate amount, merchant category, and coordinates. The multi-threaded backend computes Haversine distance and returns risk score + tier in <12ms."),
        ("Multi-Tier Triage Data Explorer", "Interactive table sorting high-risk transactions with flags for Critical Block, Step-Up MFA, and Analyst Review."),
        ("One-Click Launchers", "Engineered start_server.bat and launch_verification_interface.bat for automated environment check and instant browser launch.")
    ]
    for title, desc in ui_points:
        p_u = tf_ui.add_paragraph()
        p_u.space_before = Pt(8)
        add_para_run(p_u, f"• {title}: ", bold=True, size=11, color=DARK)
        add_para_run(p_u, desc, bold=False, size=10, color=SLATE)

    # =========================================================================
    # SLIDE 11: Summary Accountability Matrix
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Engineering Accountability & Technical Contribution Matrix")

    t_shape11 = s11.shapes.add_table(5, 4, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.8))
    tbl11 = t_shape11.table

    matrix_data = [
        ["Student Name", "Roll Number", "Core Technical Area", "Key Deliverables & Implemented Modules"],
        ["Srikashyap Amaravadi", "S24CSEU1423", "Distributed Spark & MLlib", "Linear SVM & RF Models, Vector Caching (2h->4.2m), Multi-Threaded REST API (/api/predict)"],
        ["Gitesh Goyal", "S24CSEU0774", "Optimization & Schema Disc.", "GBT, LR, DT Models, 34-Attribute Schema Discovery, Coarse-to-Fine Grid Search"],
        ["Annya Sharma", "S24CSEU1408", "Ingestion & Feature Hygiene", "Distributed Parquet Ingestion (5.01 GB), PCI-DSS Sanitization, VectorAssembler Pipeline"],
        ["Ajitej Singh", "S24CSEU1413", "Risk Intelligence & Visuals", "Domain Heuristic Scoring, 4-Tier Hybrid Triage Engine, Evaluation Plots & Dashboard UI"]
    ]
    w11 = [Inches(2.4), Inches(1.4), Inches(2.6), Inches(5.3)]
    for idx, width in enumerate(w11):
        tbl11.columns[idx].width = width

    for r_idx, row in enumerate(matrix_data):
        for c_idx, val in enumerate(row):
            cell = tbl11.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY
                p.font.bold = True
                p.font.size = Pt(11)
                p.font.color.rgb = WHITE
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = LIGHT_BG if r_idx % 2 == 1 else WHITE
                p.font.size = Pt(9.5)
                p.font.color.rgb = DARK
                if c_idx == 0:
                    p.font.bold = True

    # =========================================================================
    # SLIDE 12: Conclusion & Q&A
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Conclusion, Industrial Impact & Discussion")

    add_card(s12, Inches(0.8), Inches(1.4), Inches(11.7), Inches(4.5), NAVY)
    tb_c = s12.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(3.8))
    tf_c = tb_c.text_frame
    p_ch = tf_c.paragraphs[0]
    p_ch.text = "CREDITTRANSACT: KEY TAKEAWAYS"
    p_ch.font.size = Pt(18)
    p_ch.font.bold = True
    p_ch.font.color.rgb = RGBColor(56, 189, 248)

    c_points = [
        "Scalability Proved: Successfully processed 15,000,000 transactions (5.01 GB) using Apache Spark MLlib with 80% runtime optimization.",
        "Precision Superiority: Linear SVM achieved 99.96% precision with only 5 false alarms, preventing customer checkout friction.",
        "Operational Practicality: 4-Tier hybrid triage routes 95.23% to instant clearance while intercepting 99.96% of critical fraud threats.",
        "Enterprise Readiness: Fullstack verification dashboard, REST API simulation, and formal 5-chapter report synchronized on GitHub."
    ]
    for pt in c_points:
        p_pt = tf_c.add_paragraph()
        p_pt.space_before = Pt(10)
        p_pt.text = f"✔ {pt}"
        p_pt.font.size = Pt(12)
        p_pt.font.color.rgb = WHITE

    tb_qa = s12.shapes.add_textbox(Inches(0.8), Inches(6.1), Inches(11.7), Inches(0.8))
    p_qa = tb_qa.text_frame.paragraphs[0]
    p_qa.alignment = PP_ALIGN.CENTER
    p_qa.text = "THANK YOU! WE ARE NOW READY FOR QUESTIONS & DISCUSSION."
    p_qa.font.size = Pt(14)
    p_qa.font.bold = True
    p_qa.font.color.rgb = CRIMSON

    out_file = DOCS_DIR / "CreditTransAct_Final_Presentation.pptx"
    prs.save(str(out_file))
    print(f"Presentation saved to: {out_file}")

    desktop_file = Path("C:/Users/kashy/OneDrive/Desktop/CreditTransAct_Final_Presentation.pptx")
    try:
        shutil.copy2(out_file, desktop_file)
        print(f"Copied presentation to Desktop: {desktop_file}")
    except Exception as e:
        print(f"Desktop copy notice: {e}")

if __name__ == "__main__":
    create_presentation()
