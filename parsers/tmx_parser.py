# File: parsers/tmx_parser.py

import xml.etree.ElementTree as ET
import pandas as pd

def parse_tmx_to_dataframe(file_path):
    """
    Parses a TMX file and returns a DataFrame with source and target segments.
    Assumes bilingual file with two languages only.
    """

    tree = ET.parse(file_path)
    root = tree.getroot()

    # Default TMX namespace
    namespace = {'tmx': 'http://www.lisa.org/tmx14'}

    # Try both namespaced and non-namespaced files
    tus = root.findall(".//tu")
    data = []

    for tu in tus:
        segments = tu.findall("tuv")
        if len(segments) < 2:
            continue  # skip incomplete units

        entry = {}
        for tuv in segments:
            lang = tuv.attrib.get("{http://www.w3.org/XML/1998/namespace}lang")
            seg = tuv.find("seg")
            if lang and seg is not None:
                entry[lang] = seg.text
        if len(entry) >= 2:
            data.append(entry)

    df = pd.DataFrame(data)
    return df
