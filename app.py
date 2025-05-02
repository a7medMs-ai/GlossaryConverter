# File: app.py

import sys
import os

# Fix path for module resolution
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import tempfile
import pandas as pd

from parsers import tmx_parser, tbx_parser, sdltm_parser, excel_handler
from utils import converters, excel_to_tmx

# ------------- PAGE CONFIGURATION ------------------
st.set_page_config(page_title="Glossary Format Converter", layout="wide")

# ------------- SIDEBAR (DEVELOPER INFO + INSTRUCTIONS) ------------------
with st.sidebar:
    st.markdown("## 🧑‍💻 Developer Information")
    st.markdown("**Ahmed Mostafa Saad**")
    st.markdown("*Position:* Localization Engineering & TMS Support Team Lead")
    st.markdown("*Contact:* [ahmed.mostafaa@future-group.com](mailto:ahmed.mostafaa@future-group.com)")
    st.markdown("*Company:* Future Group Translation Services")

    st.markdown("---")
    st.markdown("## 🛠 Tool Instructions")
    st.markdown("""
    1. Upload glossary file (TMX, TBX, Excel, SDLTM, CSV)
    2. Select the desired conversion type
    3. Download the converted file
    """)

# ------------- MAIN PAGE ------------------
st.markdown("<h1 style='text-align: center;'>🧰 Glossary Format Converter</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:16px;'>Translation Engineering Tool – 2025 • v1.0.0</p>", unsafe_allow_html=True)
st.markdown("---")

# File upload
uploaded_file = st.file_uploader("Upload a glossary file", type=["tmx", "tbx", "xlsx", "csv", "sdltm"])

# Conversion selection
conversion_option = st.selectbox("Select conversion type", [
    "TMX → Excel",
    "TBX → Excel",
    "SDLTM → Excel",
    "Excel → TBX",
    "Excel → TMX"
])

# Conversion process
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

        elif conversion_option == "SDLTM → Excel":
            df = sdltm_parser.parse_sdltm_to_dataframe(input_path)
            ext = ".xlsx"
            export_func = excel_handler.save_dataframe_to_excel

        elif conversion_option == "Excel → TBX":
            df = excel_handler.read_excel_to_dataframe(input_path)
            ext = ".tbx"
            export_func = converters.convert_excel_to_tbx

        elif conversion_option == "Excel → TMX":
            df = excel_handler.read_excel_to_dataframe(input_path)
            ext = ".tmx"
            export_func = excel_to_tmx.convert_excel_to_tmx

        else:
            st.error("Unsupported conversion type.")
            st.stop()

        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_output:
            export_func(df, temp_output.name)
            st.success("✅ Conversion successful!")
            with open(temp_output.name, "rb") as f:
                st.download_button("📥 Download Converted File", f, file_name=f"converted_glossary" + ext)

    except Exception as e:
        st.error(f"❌ Conversion failed: {e}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Future Group – Localization Engineering • © 2025 • v1.0.0</p>", unsafe_allow_html=True)
