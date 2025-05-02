# File: parsers/excel_handler.py

import pandas as pd

def save_dataframe_to_excel(df, output_path):
    """
    Saves a pandas DataFrame to an Excel file.
    """
    df.to_excel(output_path, index=False)

def read_excel_to_dataframe(file_path):
    """
    Reads an Excel file and returns a pandas DataFrame.
    """
    return pd.read_excel(file_path)
