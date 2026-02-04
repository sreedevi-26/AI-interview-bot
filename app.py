import streamlit as st
from groq import Groq
import os

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Interview Bot", page_icon="🤖")

st.title("AI Interview Bot 🤖")

# ------------------ API KEY SETUP ------------------
api_key = st.secrets.get("GROQ_API_KEY")

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

# ------------------ FUNCTION TO GENERATE QUESTION ------------------
def generate_question(role):
    try:
        prompt = f"Ask ONE professional interview question for a {role}. Do not give the answer."

        response = client.chat.completions.create(
        model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a professional technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200,
            timeout=20
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error("BACKEND ERROR:")
        st.code(str(e))
        return None

# ------------------ FUNCTION TO EVALUATE ANSWER ------------------
def evaluate_answer(question, answer):
    try:
        eval_prompt = f"""
You are an interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate and provide:
- Score out of 10
- Short feedback
- Missing concepts
"""

        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are a professional interviewer evaluating a candidate."},
                {"role": "user", "content": eval_prompt}
            ],
            temperature=0.5,
            max_tokens=400,
            timeout=20
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error("BACKEND ERROR:")
        st.code(str(e))
        return None

# ------------------ START INTERVIEW ------------------
if st.button("Start Interview"):
    st.session_state.question = generate_question(role)
    st.session_state.answer = ""
    st.session_state.evaluation = ""

# ------------------ SHOW QUESTION ------------------
if st.session_state.question:
    st.subheader("Interviewer Question")
    st.write(st.session_state.question)

    st.session_state.answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):
        st.session_state.evaluation = evaluate_answer(
            st.session_state.question,
            st.session_state.answer
        )

# ------------------ SHOW EVALUATION ------------------
if st.session_state.evaluation:
    st.subheader("Interview Feedback")
    st.write(st.session_state.evaluation)

# ------------------ TEST API BUTTON ------------------
with st.expander("Debug Tools"):
    if st.button("Test API Connection"):
        test = generate_question("DSA")
        if test:
            st.success("✅ API Working!")
            st.write(test)



