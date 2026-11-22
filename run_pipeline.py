import sys
import time
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run_step(script_name, description):
    print("\n" + "=" * 70)
    print(f"STEP: {description}")
    print(f"SCRIPT: {script_name}")
    print("=" * 70)
    t0 = time.time()
    
    python_exe = ROOT / ".venv" / "Scripts" / "python.exe"
    if not python_exe.exists():
        python_exe = sys.executable
        
    script_path = ROOT / script_name
    
    cmd = [str(python_exe), str(script_path)]
    result = subprocess.run(cmd, cwd=str(ROOT))
    
    elapsed = time.time() - t0
    if result.returncode != 0:
        print(f"[-] FAILED: {script_name} exited with code {result.returncode} in {elapsed:.2f}s")
        sys.exit(result.returncode)
    else:
        print(f"[+] COMPLETED: {script_name} finished successfully in {elapsed:.2f}s")

def main():
    print("*" * 70)
    print("CREDITTRANSACT FRAUD ANALYTICS: FULL END-TO-END PIPELINE RUNNER")
    print("*" * 70)
    
    start_total = time.time()
    
    # 1. Inspect schema (if report doesn't exist)
    schema_rep = ROOT / "results" / "schema_report.json"
    if not schema_rep.exists():
        run_step("pipeline/00_inspect_schema.py", "Stage 0: Schema Inspection & Discovery")
    else:
        print("\n[i] Stage 0: Schema report already exists. Skipping inspection.")

    # 2. Ingest raw CSV to Parquet (if raw layer doesn't exist)
    raw_dir = ROOT / "results" / "raw"
    if not raw_dir.exists() or not any(raw_dir.iterdir()):
        run_step("pipeline/01_ingest.py", "Stage 1: Distributed Ingestion to Parquet")
    else:
        print("\n[i] Stage 1: Raw Parquet layer already exists. Skipping ingestion.")

    # 3. Clean and transform to Parquet (if cleaned layer doesn't exist)
    cleaned_dir = ROOT / "results" / "cleaned"
    if not cleaned_dir.exists() or not any(cleaned_dir.iterdir()):
        run_step("pipeline/02_transform.py", "Stage 2: Data Cleaning & Hygiene")
    else:
        print("\n[i] Stage 2: Cleaned Parquet layer already exists. Skipping transform.")

    # 4. Risk analysis
    run_step("pipeline/03_risk_analysis.py", "Stage 3: Explainable Heuristic Risk Scoring")

    # 5. Model training
    run_step("pipeline/04_train_models.py", "Stage 4: Distributed Spark MLlib Model Training (5 Models)")

    # 6. Evaluation & visualizations
    run_step("pipeline/05_evaluate.py", "Stage 5: Model Evaluation, Metrics & Visualizations")

    # 7. Hybrid triage decision engine
    run_step("pipeline/06_hybrid_inference.py", "Stage 6: Hybrid Operational Fraud Triage Engine")

    # 8. Export pre-modeled datasets for Power BI
    run_step("export_for_powerbi.py", "Stage 7: Power BI Data Assets & Star Schema Export")

    # 9. Final Word Document Report generation
    run_step("create_final_report_docx.py", "Stage 8: Comprehensive Word Report Generation (.docx)")

    total_time = time.time() - start_total
    print("\n" + "*" * 70)
    print(f"ALL STAGES COMPLETED SUCCESSFULLY IN {total_time:.2f}s!")
    print("*" * 70)

if __name__ == "__main__":
    main()
