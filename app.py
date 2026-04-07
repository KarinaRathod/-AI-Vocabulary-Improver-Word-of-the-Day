import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import random

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="AI Vocabulary Coach", layout="wide")
st.title("📚 AI Vocabulary Improver")
st.caption("Improve your English with AI-powered suggestions")

# -----------------------------
# SESSION STATE
# -----------------------------
if "saved_words" not in st.session_state:
    st.session_state.saved_words = []

# -----------------------------
# WORD LIST (Fallback)
# -----------------------------
word_bank = [
    "Serendipity", "Eloquent", "Meticulous", "Resilient",
    "Ephemeral", "Ubiquitous", "Pragmatic", "Ambiguous"
]

# -----------------------------
# WORD OF THE DAY
# -----------------------------
st.subheader("📅 Word of the Day")

word = random.choice(word_bank)

if st.button("Generate Word Details"):
    prompt = f"""
    Provide details for the word: {word}

    Include:
    - Meaning
    - Example sentence
    - 2 synonyms
    - Simple explanation
    """

    response = model.generate_content(prompt)

    st.success(f"Word: {word}")
    st.write(response.text)

    if st.button("💾 Save Word"):
        st.session_state.saved_words.append(word)

# -----------------------------
# VOCAB IMPROVER
# -----------------------------
st.subheader("🧠 Improve Your Sentence")

user_text = st.text_area("Enter a sentence", height=150)

if st.button("✨ Improve Vocabulary"):
    if not user_text.strip():
        st.warning("⚠️ Enter a sentence")
    else:
        prompt = f"""
        Improve the vocabulary of this sentence:
        "{user_text}"

        Provide:
        - Improved sentence
        - Explanation
        """

        response = model.generate_content(prompt)

        st.subheader("💡 Improved Version")
        st.write(response.text)

# -----------------------------
# LEVEL-BASED WORDS
# -----------------------------
st.subheader("🎯 Learn by Level")

level = st.selectbox("Select Level", ["Beginner", "Intermediate", "Advanced"])

if st.button("📖 Generate Words"):
    prompt = f"""
    Give 5 {level} level vocabulary words with:
    - Meaning
    - Example
    """

    response = model.generate_content(prompt)
    st.write(response.text)

# -----------------------------
# SAVED WORDS
# -----------------------------
if st.session_state.saved_words:
    st.subheader("💾 Saved Words")
    for w in st.session_state.saved_words:
        st.info(w)