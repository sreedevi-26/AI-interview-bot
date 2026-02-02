import streamlit as st
from langchain_ollama import OllamaLLM

# -------------------------------
# Load Model (only once)
# -------------------------------
@st.cache_resource
def load_model():
    return OllamaLLM(model="phi3")

llm = load_model()

# -------------------------------
# Page Title
# -------------------------------
st.title("AI Interview Bot 🤖")

# -------------------------------
# Session State Initialization
# -------------------------------
if "question" not in st.session_state:
    st.session_state.question = None

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "evaluation" not in st.session_state:
    st.session_state.evaluation = None

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# -------------------------------
# Role Selection
# -------------------------------
role = st.selectbox(
    "Select Interview Role",
    ["Java Developer", "AI/ML", "DSA", "HR"]
)

# -------------------------------
# Start Interview Button
# -------------------------------
if st.button("Start Interview"):
    with st.spinner("Generating question..."):
        prompt = f"Ask ONE interview question for a {role}. Do not give the answer."
        st.session_state.question = llm.invoke(prompt)

    st.session_state.answer = ""
    st.session_state.evaluation = None
    st.session_state.submitted = False

# -------------------------------
# Show Question
# -------------------------------
if st.session_state.question:
    st.subheader("Interviewer Question")
    st.write(st.session_state.question)

    # Answer Input
    st.session_state.answer = st.text_area(
        "Your Answer",
        value=st.session_state.answer
    )

    # -------------------------------
    # Submit Answer Button
    # -------------------------------
    if st.button("Submit Answer"):
        st.session_state.submitted = True

        eval_prompt = f"""
You are an interviewer.

Question:
{st.session_state.question}

Candidate Answer:
{st.session_state.answer}

Evaluate the answer and provide:
- Score out of 10
- Short feedback
- Missing or weak concepts
"""

        with st.spinner("Evaluating your answer..."):
            st.session_state.evaluation = llm.invoke(eval_prompt)

# -------------------------------
# Show Evaluation
# -------------------------------
if st.session_state.submitted and st.session_state.evaluation:
    st.subheader("Interview Feedback")
    st.write(st.session_state.evaluation)

    # -------------------------------
    # Next Question Button
    # -------------------------------
    if st.button("Next Question"):
        with st.spinner("Generating next question..."):
            prompt = f"Ask ONE different interview question for a {role}. Do not give the answer."
            st.session_state.question = llm.invoke(prompt)

        st.session_state.answer = ""
        st.session_state.evaluation = None
        st.session_state.submitted = False
