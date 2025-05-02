# File: utils/excel_to_tmx.py

import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom

def convert_excel_to_tmx(df, output_path):
    """
    Converts a pandas DataFrame with bilingual columns to a TMX file.
    Assumes first two columns are source and target language codes.
    """

    # Get language codes from column headers
    if len(df.columns) < 2:
        raise ValueError("The Excel file must have at least two columns for source and target languages.")

    source_lang = df.columns[0]
    target_lang = df.columns[1]

    # Create root element
    root = ET.Element("tmx", version="1.4")
    header = ET.SubElement(root, "header", attrib={
        "creationtool": "Glossary Converter",
        "creationtoolversion": "1.0",
        "datatype": "PlainText",
        "segtype": "sentence",
        "adminlang": "en-us",
        "srclang": source_lang,
        "o-tmf": "GlossaryConverterTMX"
    })
    body = ET.SubElement(root, "body")

    for _, row in df.iterrows():
        src_text = str(row[source_lang]) if pd.notna(row[source_lang]) else ""
        tgt_text = str(row[target_lang]) if pd.notna(row[target_lang]) else ""

        tu = ET.SubElement(body, "tu")
        tuv_src = ET.SubElement(tu, "tuv", attrib={"xml:lang": source_lang})
        seg_src = ET.SubElement(tuv_src, "seg")
        seg_src.text = src_text

        tuv_tgt = ET.SubElement(tu, "tuv", attrib={"xml:lang": target_lang})
        seg_tgt = ET.SubElement(tuv_tgt, "seg")
        seg_tgt.text = tgt_text

    # Beautify XML
    xml_str = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="  ")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
