# File: app.py

import streamlit as st
import os
import tempfile
import pandas as pd
from parsers import tmx_parser, tbx_parser, excel_handler
from utils import converters

# Page config
st.set_page_config(page_title="Glossary Format Converter", layout="centered")

st.title("🧰 Glossary Format Converter")

# File upload
uploaded_file = st.file_uploader("Upload a file", type=["tmx", "tbx", "xlsx", "sdltb", "sdltm"])

# Format options
conversion_option = st.selectbox("Select conversion type", [
    "TMX → Excel",
    "TBX → Excel",
    "Excel → TBX"
])

# Process on button click
if uploaded_file and st.button("Convert"):
    with tempfile.NamedTemporaryFile(delete=False) as temp_input:
        temp_input.write(uploaded_file.read())
        input_path = temp_input.name

    try:
        if conversion_option == "TMX → Excel":
            df = tmx_parser.parse_tmx_to_dataframe(input_path)
            ext = ".xlsx"
            export_func = excel_handler.save_dataframe_to_excel

        elif conversion_option == "TBX → Excel":
            df = tbx_parser.parse_tbx_to_dataframe(input_path)
            ext = ".xlsx"
            export_func = excel_handler.save_dataframe_to_excel

        elif conversion_option == "Excel → TBX":
            df = excel_handler.read_excel_to_dataframe(input_path)
            ext = ".tbx"
            export_func = lambda df_, path_: converters.convert_excel_to_tbx(df_, path_)

        else:
            st.error("Unsupported conversion type.")
            st.stop()

        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_output:
            export_func(df, temp_output.name)
            st.success("Conversion successful!")
            with open(temp_output.name, "rb") as f:
                st.download_button(f"📥 Download Converted File", f, file_name=f"converted_glossary{ext}")

    except Exception as e:
        st.error(f"Conversion failed: {e}")
