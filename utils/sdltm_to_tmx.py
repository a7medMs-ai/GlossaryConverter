import os
from parsers.sdltm_parser import extract_sdltm_data
from parsers.tmx_writer import write_tmx

def convert_sdltm_to_tmx(input_file, output_file=None):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"SDLTM file not found: {input_file}")

    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + ".tmx"

    print(f"[INFO] Extracting SDLTM: {input_file}")
    tu_data = extract_sdltm_data(input_file)

    print(f"[INFO] Writing TMX to: {output_file}")
    write_tmx(tu_data, output_file)

    print("[SUCCESS] Conversion complete.")
    return output_file
