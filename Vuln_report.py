import streamlit as st
import pandas as pd
from PIL import Image
import os
from io import BytesIO
from datetime import datetime

EXCEL_FILE = "vuln_data.xlsx"

def load_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        columns = [
            "Vulnerability Name", "Severity", "CVSS Score", 
            "Service", "Version", "Description", 
            "Evidence Text", "Evidence Image", "Pentesting Done", 
            "Date Recorded", "Affected IPs (Grouped)"
        ]
        return pd.DataFrame(columns=columns)

def save_data(df):
    df.to_excel(EXCEL_FILE, index=False)

st.set_page_config(page_title="Vulnerability Report Form", layout="wide")
st.title("🔐 Vulnerability Input Form")

st.markdown("Fill in the form below. You can add multiple IPs grouped by the same vulnerability.")

with st.form("vuln_form", clear_on_submit=True):
    vuln_name = st.text_input("🔸 Vulnerability Name")
    severity = st.selectbox("⚠️ Severity", ["Low", "Medium", "High", "Critical"])
    cvss_score = st.number_input("💥 CVSS Score", min_value=0.0, max_value=10.0, step=0.1)
    
    service_name = st.text_input("💻 Affected Service (e.g., Apache, SSH, MySQL)")
    service_version = st.text_input("🧩 Service Version")
    
    vuln_description = st.text_area("📝 Description about the Vulnerability")
    pentest_done = st.selectbox("📅 Was Pentesting Done for this Vulnerability?", ["Yes", "No"])
    
    st.markdown("### 💻 Affected IPs (Grouped Format)")
    st.markdown("Add IPs like this (each on new line):\n`IP_address<TAB>Port(s)<TAB>Version`\nExample:\n`172.16.0.5\t80,443\t2.4.53`")
    grouped_ips_input = st.text_area("Affected IPs (Grouped)", height=150)
    
    st.markdown("### 📁 Evidence")
    evidence_text = st.text_area("🗒 Textual Evidence (optional)")
    evidence_img = st.file_uploader("📸 Upload Evidence Image (optional)", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("✅ Save Entry")
    
    if submitted:
        df = load_data()

        img_data = ""
        if evidence_img:
            image = Image.open(evidence_img)
            img_bytes = BytesIO()
            image.save(img_bytes, format='PNG')
            img_data = img_bytes.getvalue()

        new_entry = {
            "Vulnerability Name": vuln_name,
            "Severity": severity,
            "CVSS Score": cvss_score,
            "Service": service_name,
            "Version": service_version,
            "Description": vuln_description,
            "Evidence Text": evidence_text,
            "Evidence Image": img_data,
            "Pentesting Done": pentest_done,
            "Date Recorded": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Affected IPs (Grouped)": grouped_ips_input.strip()
        }

        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        save_data(df)
        st.success("✅ Entry saved successfully!")
