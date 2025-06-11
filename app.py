import streamlit as st
from analysis.analyzer import analyze_singing_ai
import tempfile
import os
import base64

# Page config must be first
st.set_page_config(page_title="VirtuSinger", layout="centered")

# Enhanced custom styling
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        background-color: #f2f4f7;
        font-family: 'Segoe UI', sans-serif;
        color: #1a1a1a;
    }
    .stApp {
        padding: 2rem;
        background: linear-gradient(to bottom right, #ffffff, #f0f2f5);
    }
    h1, h2, h3, h4 {
        color: #2c3e50;
        font-weight: 600;
    }
    .stTextInput>div>input {
        border: 1px solid #cccccc;
        border-radius: 5px;
        padding: 0.5rem;
    }
    .stButton>button {
        background-color: #4b6cb7;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #3b5998;
    }
    .block-container {
        padding: 1rem 2rem;
    }
    .stMetricValue {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .stMetricLabel {
        font-size: 0.9rem;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

st.title("VirtuSinger")
st.subheader("AI-Powered Vocal Feedback for Classical and Opera Singers")

st.markdown("""
Upload your vocal recording and provide reference notes to receive personalized feedback 
on pitch accuracy, breath support, and diction clarity. Review performance visuals and tips to improve.
""")

uploaded_file = st.file_uploader("Upload your .wav file", type=["wav"])
notes_input = st.text_input("Reference Notes (comma-separated) eg. C4,C4,G4,E4", value="")
notes_list = [n.strip() for n in notes_input.split(",") if n.strip()]

if uploaded_file and notes_list:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_path = temp_audio.name

    st.audio(temp_path)
    st.info("Analyzing your performance...")

    with st.spinner("Running analysis..."):
        result = analyze_singing_ai(temp_path, notes_list)

    st.success("Analysis complete")
    os.remove(temp_path)

    st.header("Vocal Score Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pitch", f"{result['pitch_score']}/10")
    col2.metric("Breath", f"{result['breath_score']}/10")
    col3.metric("Diction", f"{result['diction_score']}/10")
    col4.metric("Total", f"{result['total_score']}/10")

    st.header("Visual Analysis")
    st.image(result["pitch_plot"], caption="Pitch Contour", use_column_width=True)
    st.image(result["breath_plot"], caption="Breath Support", use_column_width=True)

    st.header("Feedback")
    with st.container():
        st.subheader("Pitch Feedback")
        st.markdown(result["pitch_feedback"])

        st.subheader("Breath Feedback")
        st.markdown(result["breath_feedback"])

        st.subheader("Diction Feedback")
        st.markdown(result["diction_feedback"])

    st.divider()
    st.caption("VirtuOpera is in active development. Stay tuned for new features including session tracking and practice plans.")
