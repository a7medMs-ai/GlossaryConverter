# File: utils/converters.py

import xml.etree.ElementTree as ET
from xml.dom import minidom

def convert_excel_to_tbx(df, output_path):
    """
    Converts a pandas DataFrame to a TBX file and saves it to the given path.
    Assumes each column is a language code and each row is a term pair/group.
    """

    root = ET.Element("tbx", attrib={"style": "dca", "type": "TBX-Basic"})
    body = ET.SubElement(root, "body")

    for _, row in df.iterrows():
        term_entry = ET.SubElement(body, "termEntry")
        for lang_code, value in row.items():
            if pd.isna(value):
                continue
            lang_set = ET.SubElement(term_entry, "langSet", attrib={
                "{http://www.w3.org/XML/1998/namespace}lang": lang_code
            })
            tig = ET.SubElement(lang_set, "tig")
            term = ET.SubElement(tig, "term")
            term.text = str(value)

    # Pretty XML output
    xml_str = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="  ")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
