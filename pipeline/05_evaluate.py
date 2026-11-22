import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from common import ROOT

# Ensure matplotlib writable temp cache
os.environ['MPLCONFIGDIR'] = str(ROOT / 'results' / '.matplotlib')

res = ROOT / 'results'
metrics_file = res / 'model_metrics.csv'
if not metrics_file.exists():
    raise FileNotFoundError('Run 04_train_models.py first.')

df = pd.read_csv(metrics_file)
ok = df[df.status == 'OK'].copy()
if ok.empty:
    raise RuntimeError('No model completed successfully. Inspect model_metrics.csv.')

plots = res / 'plots'
plots.mkdir(parents=True, exist_ok=True)

# Comparison plots with nice styling
colors = {'precision': '#1B365D', 'recall': '#D97706', 'f1': '#059669', 'roc_auc': '#7C3AED'}

for metric in ['precision', 'recall', 'f1', 'roc_auc']:
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(ok['model'], ok[metric], color=colors.get(metric, '#2563EB'), width=0.55, edgecolor='black', linewidth=0.8)
    ax.set_ylabel(metric.replace('_', '-').upper(), fontsize=11, fontweight='bold')
    ax.set_title(f'Model Benchmark: {metric.replace("_", "-").upper()}', fontsize=13, fontweight='bold', pad=12)
    ax.set_ylim(0, 1.08)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation=20, ha='right', fontsize=10)
    
    # Add value labels on top of bars
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, h + 0.015, f'{h:.4f}', ha='center', va='bottom', fontsize=9.5, fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(plots / f'{metric}_comparison.png', dpi=200)
    plt.close(fig)

# Combined metrics bar chart
fig, ax = plt.subplots(figsize=(10, 6))
width = 0.18
x = range(len(ok))
for idx, (metric, col) in enumerate(colors.items()):
    ax.bar([i + idx * width for i in x], ok[metric], width=width, label=metric.replace('_', '-').upper(), color=col)

ax.set_xticks([i + 1.5 * width for i in x])
ax.set_xticklabels(ok['model'], fontsize=10, fontweight='bold')
ax.set_ylabel('Score', fontsize=11, fontweight='bold')
ax.set_title('Overall Model Performance Comparison (CreditTransAct)', fontsize=13, fontweight='bold', pad=12)
ax.set_ylim(0, 1.15)
ax.legend(loc='lower right', frameon=True)
ax.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(plots / 'overall_model_comparison.png', dpi=200)
plt.close(fig)

# Individual Confusion Matrices with heatmap colors
for _, r in ok.iterrows():
    matrix = [[int(r.tn), int(r.fp)], [int(r.fn), int(r.tp)]]
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(matrix, cmap='Blues', aspect='auto')
    
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Pred: Legitimate', 'Pred: Fraud'], fontsize=10, fontweight='bold')
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Actual: Legitimate', 'Actual: Fraud'], fontsize=10, fontweight='bold')
    ax.set_title(f"{r['model']} Confusion Matrix", fontsize=12, fontweight='bold', pad=12)
    
    thresh = (int(r.tn) + int(r.tp) + int(r.fp) + int(r.fn)) / 4.0
    for i in range(2):
        for j in range(2):
            val = matrix[i][j]
            txt_color = 'white' if val > thresh else 'black'
            ax.text(j, i, f"{val:,}", ha='center', va='center', fontsize=12, fontweight='bold', color=txt_color)
            
    fig.colorbar(im, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.savefig(plots / f"confusion_{r['model']}.png", dpi=200)
    plt.close(fig)

print('\n======================================================')
print('EVALUATION COMPLETED SUCCESSFULLY')
print('Artifacts and charts saved to:', plots)
print('======================================================')
print(ok[['model', 'precision', 'recall', 'f1', 'roc_auc', 'tp', 'fp', 'fn', 'tn']].to_string(index=False))
