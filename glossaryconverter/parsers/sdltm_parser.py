import sqlite3

def extract_sdltm_data(sdl_file_path):
    """
    Extracts translation unit data from SDLTM SQLite file.
    """
    conn = sqlite3.connect(sdl_file_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT tu.ID, frag.LanguageCode, frag.PlainTextSegment FROM translation_units tu JOIN translation_unit_fragments frag ON tu.ID = frag.TranslationUnit_ID")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise RuntimeError(f"SQLite error: {e}\nMaybe you're using wrong table names or unsupported SDLTM format.")

    conn.close()

    # Organize data into list of dicts: [{en: ..., fr: ...}, ...]
    tu_dict = {}
    for tu_id, lang, segment in rows:
        if tu_id not in tu_dict:
            tu_dict[tu_id] = {}
        tu_dict[tu_id][lang] = segment

    return list(tu_dict.values())
