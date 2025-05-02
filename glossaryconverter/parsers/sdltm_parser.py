import sqlite3

def extract_sdltm_data(sdl_file_path):
    """
    Extracts source and target segments from SDLTM SQLite file.
    Returns a list of dictionaries like: [{"en-US": ..., "ar-EG": ...}, ...]
    """
    conn = sqlite3.connect(sdl_file_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT source_segment, target_segment FROM translation_units")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise RuntimeError(f"SQLite error: {e}\nThis SDLTM may use a different schema.")

    conn.close()

    # Convert to list of dictionaries
    tu_list = []
    for source, target in rows:
        tu_list.append({
            "source": source,
            "target": target
        })

    return tu_list
