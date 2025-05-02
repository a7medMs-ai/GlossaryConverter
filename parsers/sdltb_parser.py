# File: parsers/sdltb_parser.py

import pandas as pd
import tempfile
import os
from pyglossary import Glossary

def parse_sdltb_to_dataframe(file_path):
    """
    Converts an SDLTB file to a pandas DataFrame using pyglossary.
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_csv:
        csv_path = tmp_csv.name

    glossary = Glossary()
    glossary.open(file_path, format="sdltb")
    glossary.export(csv_path, format="csv")

    # Read the resulting CSV into DataFrame
    df = pd.read_csv(csv_path)
    os.remove(csv_path)
    return df
