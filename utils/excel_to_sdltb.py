# File: utils/excel_to_sdltb.py

import pandas as pd
import tempfile
import os
from pyglossary import Glossary

def convert_excel_to_sdltb(df, output_path):
    """
    Converts a pandas DataFrame to SDLTB format using PyGlossary.
    Assumes the first two columns are source and target terms.
    """

    # Save DataFrame to a temporary CSV file (PyGlossary supports CSV)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_csv:
        csv_path = tmp_csv.name
        df.to_csv(csv_path, index=False)

    glossary = Glossary()
    glossary.open(csv_path, format="csv")
    glossary.export(output_path, format="sdltb")

    os.remove(csv_path)
