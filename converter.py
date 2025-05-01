import markdown
from fpdf import FPDF
import pandas as pd

def convert_to_format(df, export_format, output_path):
    content = ""
    if export_format == "Markdown":
        content = "\n".join([f"### {term}\n{definition}" for term, definition in zip(df['المصطلح'], df['التعريف'])])
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

    elif export_format == "HTML":
        content = df.to_html(index=False)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

    elif export_format == "PDF":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for i, row in df.iterrows():
            pdf.multi_cell(0, 10, f"{row['المصطلح']}:\n{row['التعريف']}\n", border=0)
        pdf.output(output_path)
