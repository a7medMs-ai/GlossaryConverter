# File: parsers/sdltm_parser.py

import sqlite3
import pandas as pd

def parse_sdltm_to_dataframe(file_path):
    """
    Parses an SDLTM file and extracts source/target segments from available tables.
    """
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    # List available tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    if "TranslationUnitVariants" not in tables:
        raise RuntimeError("Expected table 'TranslationUnitVariants' not found in this SDLTM file.")

    query = """
    SELECT tuv.TranslationUnitId, tuv.Culture, tuv.PlainText
    FROM TranslationUnitVariants tuv
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Pivot data to create bilingual rows
    pivot = df.pivot(index="TranslationUnitId", columns="Culture", values="PlainText")
    pivot.reset_index(drop=True, inplace=True)

    return pivot
