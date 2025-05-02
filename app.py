# File: app.py

import streamlit as st
import os
import tempfile
from parsers import tmx_parser, excel_handler

# Page config
st.set_page_config(page_title="Glossary Format Converter", layout="centered")

st.title("🧰 Glossary Format Converter")

# File upload
uploaded_file = st.file_uploader("Upload a file", type=["tmx", "tbx", "xlsx", "sdltb", "sdltm"])

# Format options (expand later)
conversion_option = st.selectbox("Select conversion type", [
    "TMX → Excel"
])

# Process on button click
if uploaded_file and st.button("Convert"):
    with tempfile.NamedTemporaryFile(delete=False) as temp_input:
        temp_input.write(uploaded_file.read())
        input_path = temp_input.name

    if conversion_option == "TMX → Excel":
        try:
            df = tmx_parser.parse_tmx_to_dataframe(input_path)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_output:
                excel_handler.save_dataframe_to_excel(df, temp_output.name)
                st.success("Conversion successful!")
                with open(temp_output.name, "rb") as f:
                    st.download_button("📥 Download Excel File", f, file_name="converted_glossary.xlsx")
        except Exception as e:
            st.error(f"Conversion failed: {e}")
