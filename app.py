import streamlit as st
import pandas as pd
from converter import convert_to_format
from github_utils import upload_to_github, create_repo_if_not_exists
import tempfile

st.title("📘 Glossary Converter")

uploaded_file = st.file_uploader("ارفع ملف Excel يحتوي على أعمدة 'المصطلح' و'التعريف'", type=["xlsx"])
export_format = st.selectbox("اختر صيغة التصدير", ["HTML", "PDF", "Markdown"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📋 معاينة المحتوى")
    st.dataframe(df.head())

    if st.button("🔄 تحويل ورفع"):
        with st.spinner("جاري المعالجة..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{export_format.lower()}") as tmp:
                convert_to_format(df, export_format, tmp.name)

                repo_name = "glossary-files"
                file_name = f"glossary.{export_format.lower()}"
                create_repo_if_not_exists(repo_name)
                file_url = upload_to_github(tmp.name, file_name, repo_name)

                st.success("تم التحويل والرفع بنجاح!")
                st.markdown(f"[📂 رابط الملف على GitHub]({file_url})")
