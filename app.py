import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import tempfile
import pandas as pd

from parsers import tmx_parser, tbx_parser, sdltm_parser, excel_handler
from utils import converters, excel_to_tmx
from utils import sdltm_to_tmx, tmx_to_sdltm, sdltb_to_csv, sdltb_to_tbx

st.set_page_config(page_title="Glossary Format Converter", layout="wide")

with st.sidebar:
    st.header("Developer Information")
    st.subheader("Ahmed Mostafa Saad")
    st.write("""
    - **Position**: Localization Engineering & TMS Support Team Lead  
    - **Contact**: [ahmed.mostafaa@future-group.com](mailto:ahmed.mostafaa@future-group.com)  
    - **Company**: Future Group Translation Services
    """)
    st.divider()
    st.markdown("## 🛠 Tool Instructions")
    st.markdown("""
    1. Upload glossary file (TMX, TBX, Excel, SDLTM, SDLTB, CSV)
    2. Select the desired conversion type
    3. Download the converted file
    """)

st.markdown("<h1 style='text-align: center;'> Glossary Format Converter</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:16px;'>Translation Engineering Tool – 2025 • v1.0.0</p>", unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("Upload a glossary file", type=["tmx", "tbx", "xlsx", "csv", "sdltm", "sdltb"])

conversion_option = st.selectbox("Select conversion type", [
    "TMX → Excel",
    "TBX → Excel",
    "SDLTM → Excel",
    "SDLTM → TMX",
    "TMX → SDLTM",
    "SDLTB → CSV",
    "SDLTB → TBX",
    "Excel → TBX",
    "Excel → TMX"
])

if uploaded_file and st.button("Convert"):
    with tempfile.NamedTemporaryFile(delete=False) as temp_input:
        temp_input.write(uploaded_file.read())
        input_path = temp_input.name

    try:
        if conversion_option == "TMX → Excel":
            df = tmx_parser.parse_tmx_to_dataframe(input_path)
            st.dataframe(df)
            st.download_button("Download Excel", df.to_csv(index=False), file_name="output.csv")

        elif conversion_option == "SDLTM → TMX":
            output_path = sdltm_to_tmx.convert_sdltm_to_tmx(input_path)
            st.success("Converted to TMX")
            with open(output_path, "rb") as f:
                st.download_button("Download TMX", f, file_name="output.tmx")

        elif conversion_option == "TMX → SDLTM":
            output_path = tmx_to_sdltm.convert_tmx_to_sdltm(input_path)
            st.success("Converted to SDLTM")
            with open(output_path, "rb") as f:
                st.download_button("Download SDLTM", f, file_name="output.sdltm")

        elif conversion_option == "SDLTB → CSV":
            output_dir = os.path.dirname(input_path)
            table_names = sdltb_to_csv.convert_sdltb_to_csv(input_path, output_dir)
            for table in table_names:
                csv_path = os.path.join(output_dir, f"{table}.csv")
                with open(csv_path, "rb") as f:
                    st.download_button(f"Download {table}.csv", f, file_name=f"{table}.csv")

        elif conversion_option == "SDLTB → TBX":
            output_path = sdltb_to_tbx.convert_sdltb_to_tbx(input_path)
            st.success("Converted to TBX")
            with open(output_path, "rb") as f:
                st.download_button("Download TBX", f, file_name="output.tbx")

        else:
            st.warning("This conversion is not implemented yet.")
    except Exception as e:
        st.error(f"Error during conversion: {e}")
