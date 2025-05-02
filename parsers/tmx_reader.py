import xml.etree.ElementTree as ET

def parse_tmx(tmx_path):
    """
    Parse a TMX file and return a list of translation units.
    Each TU is a dict of {lang: text}
    """
    tree = ET.parse(tmx_path)
    root = tree.getroot()

    body = root.find("body")
    tus = []

    for tu in body.findall("tu"):
        tu_entry = {}
        for tuv in tu.findall("tuv"):
            lang = tuv.attrib.get("{http://www.w3.org/XML/1998/namespace}lang")
            seg = tuv.find("seg")
            if lang and seg is not None and seg.text:
                tu_entry[lang] = seg.text
        if tu_entry:
            tus.append(tu_entry)

    return tus
