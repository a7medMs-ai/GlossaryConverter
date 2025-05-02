# File: parsers/sdltm_parser.py

import sqlite3
import pandas as pd

def parse_sdltm_to_dataframe(file_path):
    """
    Extracts bilingual segments from SDLTM file using translation_unit_fragments table.
    Returns a DataFrame with source and target segments.
    """
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    # Load data from fragments table
    query = """
    SELECT
        f.translation_unit_id,
        f.fragment,
        f.culture
    FROM
        translation_unit_fragments f
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Pivot data so each row is one translation unit, with columns for each language
    pivot_df = df.pivot(index="translation_unit_id", columns="culture", values="fragment")
    pivot_df.reset_index(drop=True, inplace=True)

    return pivot_df
