import os
import shutil
from glossaryconverter.parsers.sdltb_reader import extract_tables_from_sdltb

def is_java_available():
    return shutil.which("java") is not None

def convert_sdltb_to_csv(sdltb_path, output_dir):
    """
    Converts an SDLTB file into multiple CSVs (one per table).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not is_java_available():
        raise EnvironmentError("Java runtime is not available. Cannot convert SDLTB to CSV without Java.")

    tables = extract_tables_from_sdltb(sdltb_path)

    for table_name, df in tables.items():
        out_path = os.path.join(output_dir, f"{table_name}.csv")
        df.to_csv(out_path, index=False)
        print(f"[INFO] Saved table '{table_name}' to {out_path}")

    print("[SUCCESS] SDLTB converted to CSV.")
    return list(tables.keys())
