import os
import sqlite3
from GlossaryConverter.parsers.tmx_reader import parse_tmx

def create_sdltm_schema(cursor):
    """
    Create a minimal SDLTM-compatible schema in the SQLite database.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TranslationUnits (
            ID INTEGER PRIMARY KEY
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TranslationUnitVariants (
            ID INTEGER PRIMARY KEY,
            TranslationUnit_ID INTEGER,
            LanguageCode TEXT,
            PlainTextSegment TEXT,
            FOREIGN KEY (TranslationUnit_ID) REFERENCES TranslationUnits(ID)
        );
    """)

def insert_translation_units(cursor, tus):
    """
    Insert parsed TMX data into the SQLite schema.
    """
    for tu_id, tu in enumerate(tus, start=1):
        cursor.execute("INSERT INTO TranslationUnits (ID) VALUES (?)", (tu_id,))
        for lang, text in tu.items():
            cursor.execute("""
                INSERT INTO TranslationUnitVariants 
                (TranslationUnit_ID, LanguageCode, PlainTextSegment)
                VALUES (?, ?, ?)
            """, (tu_id, lang, text))

def convert_tmx_to_sdltm(tmx_path, output_file=None):
    """
    Convert a TMX file into a minimal SDLTM SQLite database.
    """
    if not os.path.exists(tmx_path):
        raise FileNotFoundError(f"TMX file not found: {tmx_path}")

    if output_file is None:
        output_file = os.path.splitext(tmx_path)[0] + ".sdltm"

    print(f"[INFO] Parsing TMX: {tmx_path}")
    tus = parse_tmx(tmx_path)

    print(f"[INFO] Creating SDLTM: {output_file}")
    conn = sqlite3.connect(output_file)
    cursor = conn.cursor()
    create_sdltm_schema(cursor)
    insert_translation_units(cursor, tus)
    conn.commit()
    conn.close()

    print("[SUCCESS] SDLTM created successfully.")
    return output_file
