# File: parsers/sdltm_parser.py

import sqlite3
import pandas as pd

def parse_sdltm_to_dataframe(file_path):
    """
    Parses an SDLTM file (SQLite) and extracts source/target segments into a DataFrame.
    """

    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    # SDLTM files have a table 'TranslationUnits' with serialized data (binary BLOBs)
    # Actual data is in 'TranslationUnitVariants', linked by 'TranslationUnitId'
    query = """
    SELECT tuv.TranslationUnitId, tuv.Culture, tuv.PlainText
    FROM TranslationUnitVariants tuv
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Pivot table: one row per translation unit, columns by language
    pivot = df.pivot(index="TranslationUnitId", columns="Culture", values="PlainText")
    pivot.reset_index(drop=True, inplace=True)

    return pivot
