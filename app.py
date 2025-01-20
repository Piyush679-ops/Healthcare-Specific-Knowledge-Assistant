import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import streamlit as st
from transformers import pipeline
import pandas as pd
from rapidfuzz import process

# Initialize the QA pipeline
qa_pipeline = pipeline("question-answering", model="stanford-crfm/BioMedLM")

# Load dataset and handle errors
try:
    data = pd.read_csv("healthcare_faq.csv")  # Replace with your CSV file path
    if data.empty:
        st.error("The dataset is empty. Please ensure the CSV file has valid data.")
        st.stop()
except FileNotFoundError:
    st.error("The dataset file 'healthcare_faq.csv' was not found.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the dataset: {str(e)}")
    st.stop()

# Function to retrieve the answer
def get_answer(user_question):
    try:
        if not user_question.strip():
            return "Please enter a valid question."

        # Fuzzy matching to find the best question
        questions = data["Question"].tolist()
        best_match, score, index = process.extractOne(user_question, questions)
        
        if score > 80:  # Higher threshold for better accuracy
            return data.iloc[index]["Answer"]
        else:
            # Use the QA pipeline for context-based answers
            # Limit context to rows with top similar questions
            similar_questions = process.extract(user_question, questions, limit=5)
            related_context = " ".join([data.iloc[q[2]]["Answer"] for q in similar_questions])
            result = qa_pipeline(question=user_question, context=related_context)
            return result["answer"]
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit App
st.title("Healthcare-Specific Knowledge Assistant")
st.write("Ask me anything about healthcare!")

# Input for user question
user_question = st.text_input("Your Question")
if user_question:
    answer = get_answer(user_question)
    st.write("Answer:", answer)

    # Feedback handling
    feedback = st.text_input("Was this answer helpful? (Yes/No/Comments)")
    if feedback:
        try:
            with open("feedback_log.txt", "a") as f:
                f.write(f"Question: {user_question}\nFeedback: {feedback}\n\n")
            st.write("Thank you for your feedback!")
        except Exception as e:
            st.error(f"An error occurred while saving feedback: {str(e)}")

# Example questions
st.write("Example questions: 'What are the symptoms of flu?', 'How to prevent COVID-19?'")

# Fuzzy Matching Suggestions
if user_question:
    try:
        matches = process.extract(user_question, data["Question"].tolist(), limit=3)
        if matches:
            st.write("Did you mean:")
            for match in matches:
                st.write(match[0])
    except Exception as e:
        st.error(f"An error occurred while processing suggestions: {str(e)}")

# Caching function (optimized for Streamlit)
@st.cache_data
def get_answer_cached(user_question):
    return get_answer(user_question)
