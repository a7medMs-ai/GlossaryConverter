import xml.etree.ElementTree as ET

def write_tmx(tu_dict, output_path, srclang="en-US"):
    root = ET.Element("tmx", version="1.4")
    header = ET.SubElement(root, "header", {
        "creationtool": "GlossaryConverter",
        "creationtoolversion": "1.0",
        "segtype": "sentence",
        "o-tmf": "TMX",
        "adminlang": "en-us",
        "srclang": srclang,
        "datatype": "PlainText"
    })
    body = ET.SubElement(root, "body")

    for tu_id, langs in tu_dict.items():
        tu_elem = ET.SubElement(body, "tu")
        for lang, text in langs.items():
            tuv = ET.SubElement(tu_elem, "tuv", {"xml:lang": lang})
            seg = ET.SubElement(tuv, "seg")
            seg.text = text

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
