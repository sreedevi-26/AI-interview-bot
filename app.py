import streamlit as st
from groq import Groq
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Interview Bot", page_icon="🤖")

# Load API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found. Please add it in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.1-8b-instant"

# ---------------- FUNCTIONS ----------------

def generate_question(role):
    try:
        prompt = f"Ask one professional technical interview question for a {role}."

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error generating question: {str(e)}"


def evaluate_answer(question, answer):
    try:
        prompt = f"""
You are an interview evaluator.

Question:
{question}

Candidate Answer:
{answer}

Give a short professional evaluation and a score out of 10.
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=150
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error evaluating answer: {str(e)}"


def test_api():
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": "Say 'API working'"}
            ],
            max_tokens=10
        )
        return "✅ API Working!"
    except Exception as e:
        return f"❌ API Error: {str(e)}"


# ---------------- UI ----------------

st.title("AI Interview Bot 🤖")

role = st.selectbox(
    "Select Interview Role",
    ["Java Developer", "Python Developer", "Data Analyst", "Web Developer"]
)

if "question" not in st.session_state:
    st.session_state.question = ""

if st.button("Start Interview"):
    st.session_state.question = generate_question(role)

if st.session_state.question:
    st.subheader("Interview Question")
    st.write(st.session_state.question)

    answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):
        if answer.strip():
            result = evaluate_answer(st.session_state.question, answer)
            st.subheader("Evaluation Result")
            st.write(result)
        else:
            st.warning("⚠️ Please write an answer before submitting")

# ---------------- DEBUG ----------------

with st.expander("Debug Tools"):
    if st.button("Test API Connection"):
        st.write(test_api())
