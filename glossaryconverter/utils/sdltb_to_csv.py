import os
from glossaryconverter.parsers.sdltb_reader import extract_tables_from_sdltb

def convert_sdltb_to_csv(sdltb_path, output_dir):
    """
    Converts an SDLTB file into multiple CSVs (one per table).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tables = extract_tables_from_sdltb(sdltb_path)

    for table_name, df in tables.items():
        out_path = os.path.join(output_dir, f"{table_name}.csv")
        df.to_csv(out_path, index=False)
        print(f"[INFO] Saved table '{table_name}' to {out_path}")

    print("[SUCCESS] SDLTB converted to CSV.")
    return list(tables.keys())
