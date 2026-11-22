import json
import os
import sys
from pathlib import Path
from pyspark.sql import SparkSession

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / 'config' / 'project_config.json'

# Ensure Java 17 and Hadoop winutils are configured on Windows
jdk17_path = Path(r'C:\Program Files\Microsoft\jdk-17.0.21.21-hotspot')
if jdk17_path.exists():
    os.environ['JAVA_HOME'] = str(jdk17_path)

hadoop_home = ROOT / 'hadoop'
if hadoop_home.exists():
    os.environ['HADOOP_HOME'] = str(hadoop_home)
    bin_path = str(hadoop_home / 'bin')
    if bin_path not in os.environ.get('PATH', ''):
        os.environ['PATH'] = bin_path + os.pathsep + os.environ.get('PATH', '')

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable


def config():
    return json.loads(CONFIG_PATH.read_text(encoding='utf-8'))


def spark(app_name):
    return (SparkSession.builder.appName(app_name)
            .config('spark.pyspark.python', sys.executable)
            .config('spark.pyspark.driver.python', sys.executable)
            .config('spark.driver.memory', '6g')
            .config('spark.executor.memory', '6g')
            .config('spark.sql.parquet.compression.codec', 'snappy')
            .getOrCreate())


def output_path(cfg, name):
    base = cfg.get('output_base', 'results').rstrip('/')
    return f"{base}/{name}"


def resolve_input_path(cfg):
    path = cfg['input_path']
    # Keep HDFS and other URI paths unchanged; resolve ordinary relative paths
    # against the project root so commands work from any current directory.
    if '://' not in path and not Path(path).is_absolute():
        candidate = ROOT / path
        if candidate.exists():
            return str(candidate)
    return path


def read_source(spark_session, cfg):
    path = resolve_input_path(cfg)
    source_format = cfg.get('input_format', Path(path).suffix.lstrip('.').lower())

    if source_format == 'csv':
        options = cfg.get('csv_options', {})
        reader = spark_session.read.format('csv')
        for key, value in options.items():
            reader = reader.option(key, value)
        return reader.load(path)
    if source_format in ('parquet', 'pq'):
        return spark_session.read.parquet(path)
    raise ValueError(
        f"Unsupported input_format={source_format!r}. Use 'csv' or 'parquet'."
    )
