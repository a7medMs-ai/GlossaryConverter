import subprocess
import pandas as pd
import os
import tempfile

def extract_tables_from_sdltb(sdltb_path):
    """
    Extracts tables from an SDLTB (Access .mdb) file using mdbtools.
    Returns a dictionary of {table_name: DataFrame}.
    """
    tables = {}

    # Get list of tables using mdb-tables
    cmd_tables = ["mdb-tables", "-1", sdltb_path]
    result = subprocess.run(cmd_tables, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"mdb-tables error: {result.stderr}")

    table_names = result.stdout.strip().split("\n")

    for table in table_names:
        if not table:
            continue
        cmd_export = ["mdb-export", sdltb_path, table]
        result = subprocess.run(cmd_export, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            df = pd.read_csv(pd.compat.StringIO(result.stdout))
            tables[table] = df
        else:
            print(f"[WARNING] Skipped table '{table}': {result.stderr}")

    return tables
