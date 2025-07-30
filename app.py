# app.py

import streamlit as st
import requests
import pandas as pd
from fpdf import FPDF
import datetime
import os

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="REHMAT SHIPPING", layout="centered")

# ========== DARK THEME (CUSTOM CSS) ==========
st.markdown("""
    <style>
        .stApp {
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
        }
        .stTextInput > div > div > input {
            background-color: #2a2a2a;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            border-radius: 5px;
            height: 2.5em;
        }
        .stDataFrame {
            background-color: #2a2a2a;
        }
    </style>
""", unsafe_allow_html=True)

# ========== TITLE ==========
st.title("🔍 Search Users ")
st.write("Search user by name or email")

# ========== INPUT ==========
search_term = st.text_input("Enter name or email to search:")

col1, col2 = st.columns(2)
search_clicked = col1.button("🔍 Search")
pdf_clicked = col2.button("🖨️ Generate PDF")

results = []
first_match = None
api_url = "https://jsonplaceholder.typicode.com/users"

# ========== SEARCH + PDF ==========
if search_clicked or pdf_clicked:
    if search_term.strip() == "":
        st.warning("Please enter a search term.")
    else:
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            for user in data:
                if search_term.lower() in user['name'].lower() or search_term.lower() in user['email'].lower():
                    if not first_match:
                        first_match = user
                    results.append({
                        "Name": user['name'],
                        "Email": user['email'],
                        "City": user['address']['city'],
                        "Phone": user['phone']
                    })

            if results:
                df = pd.DataFrame(results)
                st.success(f"✅ {len(results)} result(s) found.")
                st.dataframe(df)

                # ========== PDF SECTION ==========
                if pdf_clicked and first_match:
                    pdf = FPDF()
                    pdf.add_page()

                    # Title
                    pdf.set_font("Arial", "B", 16)
                    pdf.set_text_color(30, 30, 30)
                    pdf.cell(0, 10, "REHMAT SHIPPING REPORT", ln=True, align="C")

                    # Date
                    pdf.set_font("Arial", "", 10)
                    pdf.cell(0, 10, f"Date: {datetime.date.today()}", ln=True, align="C")
                    pdf.ln(10)

                    # Top Info
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 10, f"Name: {first_match['name']}", ln=True)
                    pdf.cell(0, 10, f"Phone: {first_match['phone']}", ln=True)
                    pdf.ln(5)

                    # Table Header
                    pdf.set_fill_color(200, 220, 255)
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(50, 10, "Name", border=1, fill=True)
                    pdf.cell(60, 10, "Email", border=1, fill=True)
                    pdf.cell(40, 10, "Phone", border=1, fill=True)
                    pdf.ln()

                    # Table Rows
                    pdf.set_font("Arial", "", 12)
                    for row in results:
                        pdf.cell(50, 10, row["Name"], border=1)
                        pdf.cell(60, 10, row["Email"], border=1)
                        pdf.cell(40, 10, row["Phone"], border=1)
                        pdf.ln()

                    pdf_file = "search_result.pdf"
                    pdf.output(pdf_file)

                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            label="📥 Download PDF",
                            data=f,
                            file_name="search_result.pdf",
                            mime="application/pdf"
                        )
            else:
                st.info("No results found.")

        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
