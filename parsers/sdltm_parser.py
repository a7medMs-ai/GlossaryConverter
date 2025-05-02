import sqlite3

def extract_sdltm_data(sdltm_path):
    conn = sqlite3.connect(sdltm_path)
    cursor = conn.cursor()

    # جلب وحدات الترجمة
    cursor.execute("""
        SELECT tu.ID, tuv.LanguageCode, tuv.PlainTextSegment
        FROM TranslationUnits tu
        JOIN translation_unit_fragments tuv ON tu.ID = tuv.TranslationUnit_ID
    """)
    
    results = cursor.fetchall()

    # تنظيم البيانات في شكل (tu_id: {lang: text})
    tu_dict = {}
    for tu_id, lang, text in results:
        if tu_id not in tu_dict:
            tu_dict[tu_id] = {}
        tu_dict[tu_id][lang] = text

    conn.close()
    return tu_dict
