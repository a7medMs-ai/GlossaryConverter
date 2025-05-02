import os
import sqlite3
from glossaryconverter.parsers.tmx_reader import parse_tmx

def create_sdltm_schema(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS translation_units (
            ID INTEGER PRIMARY KEY
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS translation_unit_fragments (
            ID INTEGER PRIMARY KEY,
            TranslationUnit_ID INTEGER,
            LanguageCode TEXT,
            PlainTextSegment TEXT,
            FOREIGN KEY (TranslationUnit_ID) REFERENCES translation_units(ID)
        );
    """)

def insert_translation_units(cursor, tus):
    for tu_id, tu in enumerate(tus, start=1):
        cursor.execute("INSERT INTO translation_units (ID) VALUES (?)", (tu_id,))
        for lang, text in tu.items():
            cursor.execute("""
                INSERT INTO translation_unit_fragments 
                (TranslationUnit_ID, LanguageCode, PlainTextSegment)
                VALUES (?, ?, ?)
            """, (tu_id, lang, text))

def convert_tmx_to_sdltm(tmx_path, output_file=None):
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
