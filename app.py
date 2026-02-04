import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="AI Interview Bot", page_icon="🤖")

st.title("AI Interview Bot 🤖")

# ------------------ API KEY HANDLING ------------------
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ GROQ_API_KEY not found. Please add it in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# ------------------ SESSION STATE ------------------
if "question" not in st.session_state:
    st.session_state.question = ""

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "evaluation" not in st.session_state:
    st.session_state.evaluation = ""

# ------------------ ROLE SELECTION ------------------
role = st.selectbox(
    "Select Interview Role",
    ["Java Developer", "AI/ML", "DSA", "HR"]
)

# ------------------ START INTERVIEW ------------------
if st.button("Start Interview"):
    try:
        prompt = f"Ask ONE professional interview question for a {role}. Do not give the answer."

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        st.session_state.question = response.choices_
