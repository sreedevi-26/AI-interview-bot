import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="AI Interview Bot", page_icon="🤖")

# Load API key from Streamlit Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("AI Interview Bot 🤖")

# Session state
if "question" not in st.session_state:
    st.session_state.question = ""

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "evaluation" not in st.session_state:
    st.session_state.evaluation = ""

# Role selection
role = st.selectbox(
    "Select Interview Role",
    ["Java Developer", "AI/ML", "DSA", "HR"]
)

# Start interview
if st.button("Start Interview"):
    prompt = f"Ask ONE professional interview question for a {role}. Do not give the answer."

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    st.session_state.question = response.choices[0].message.content
    st.session_state.evaluation = ""
    st.session_state.answer = ""

# Show question
if st.session_state.question:
    st.subheader("Interviewer Question")
    st.write(st.session_state.question)

    st.session_state.answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):
        eval_prompt = f"""
You are an interviewer.

Question:
{st.session_state.question}

Candidate Answer:
{st.session_state.answer}

Evaluate and provide:
- Score out of 10
- Short feedback
- Missing concepts
"""

        eval_response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": eval_prompt}]
        )

        st.session_state.evaluation = eval_response.choices[0].message.content

# Show evaluation
if st.session_state.evaluation:
    st.subheader("Interview Feedback")
    st.write(st.session_state.evaluation)
