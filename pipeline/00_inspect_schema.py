import json
from pathlib import Path
from common import ROOT, config, spark, read_source

cfg = config(); sp = spark('CreditTransAct-Schema-Inspection')
df = read_source(sp, cfg)
report = {
  'input_path': cfg['input_path'], 'rows': df.count(), 'columns': len(df.columns),
  'schema': df.schema.jsonValue(), 'column_names': df.columns,
  'sample_rows': [r.asDict(recursive=True) for r in df.limit(5).collect()]
}
out = ROOT / 'results' / 'schema_report.json'; out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2, default=str), encoding='utf-8')
print(json.dumps({'rows': report['rows'], 'columns': report['columns'], 'column_names': df.columns}, indent=2))
print('Wrote', out)
sp.stop()
