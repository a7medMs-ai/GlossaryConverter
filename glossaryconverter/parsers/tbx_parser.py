# File: parsers/tbx_parser.py

import xml.etree.ElementTree as ET
import pandas as pd

def parse_tbx_to_dataframe(file_path):
    """
    Parses a TBX file and returns a DataFrame with terms for each language.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    entries = []
    for term_entry in root.findall(".//termEntry"):
        entry = {}
        for lang_set in term_entry.findall("langSet"):
            lang = lang_set.attrib.get("{http://www.w3.org/XML/1998/namespace}lang")
            if not lang:
                continue
            term_elem = lang_set.find(".//term")
            if term_elem is not None:
                entry[lang] = term_elem.text
        if len(entry) >= 1:
            entries.append(entry)

    df = pd.DataFrame(entries)
    return df
