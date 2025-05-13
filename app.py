from dotenv import load_dotenv
load_dotenv()

import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Configure API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Convert PDF to image
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=r"C:\Program Files\poppler-24.08.0\Library\bin")
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Page config
st.set_page_config(page_title="✨ Fancy ATS Resume Expert", page_icon="💼", layout="wide")

# 🌟 Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(145deg, #fdfbfb 0%, #ebedee 100%);
        color: #333333;
        font-size:18px;
    }

    .main {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        font-size:20px;
    }

    h1, h2 {
        text-align: center;
        font-family: 'Poppins', sans-serif;
        background: -webkit-linear-gradient(45deg, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-style: italic;
    }

    .stTextArea textarea {
        border: 1px solid #d4d8e8;
        border-radius: 10px;
        color: white;
        font-size: 18px;
    }

    .stFileUploader {
        color: white !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 24px;
        transition: 0.3s;
    }

    .stButton > button:hover {
        box-shadow: 0 0 10px #667eea;
        transform: scale(1.02);
    }

    .full-width-box {
        background-color: #ffffffcc;
        padding: 20px;
        border-radius: 12px;
        margin-top: 30px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 🌟 Main App UI
st.markdown("<h1>🎯 HireMeter</h1>", unsafe_allow_html=True)
st.markdown("### 📄 Upload your resume and 🚀 check how well it matches your dream job!", unsafe_allow_html=True)

# Input layout
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        input_text = st.text_area("📝 Job Description", placeholder="Paste the job description here...", height=250)

    with col2:
        uploaded_file = st.file_uploader("📎 Upload Resume (PDF)", type=["pdf"])
        if uploaded_file is not None:
            st.success("✅ Resume uploaded successfully!")

# Prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

# Buttons
st.markdown("---")
col3, col4, col5 = st.columns([1, 0.2, 1])

# Outputs full-width centered
with st.container():
    if st.button("🔍 Analyze Resume"):
        if uploaded_file:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.markdown('<div class="full-width-box">', unsafe_allow_html=True)
            st.subheader("🧾 Resume Evaluation")
            st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠ Please upload your resume.")

    if st.button("📊 Get Match %"):
        if uploaded_file:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.markdown('<div class="full-width-box">', unsafe_allow_html=True)
            st.subheader("📈 ATS Match Result")
            st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠ Please upload your resume.")


