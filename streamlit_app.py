import streamlit as st
import speech_recognition as sr
import json
import time
from collections import defaultdict
import random

# Initialize session state variables
if 'user_history' not in st.session_state:
    st.session_state.user_history = defaultdict(int)
if 'qa_data' not in st.session_state:
    # Simple educational QA database
    st.session_state.qa_data = {
        "science": {
            "what is photosynthesis": "Photosynthesis is the process by which plants convert sunlight, water, and carbon dioxide into energy and oxygen.",
            "what are the states of matter": "The main states of matter are solid, liquid, and gas. Some scientists also consider plasma as the fourth state.",
            "what is gravity": "Gravity is a force of attraction between all masses in the universe. It's what keeps planets orbiting around the sun and makes objects fall to Earth."
        },
        "math": {
            "what is pythagorean theorem": "The Pythagorean theorem states that in a right triangle, the square of the hypotenuse equals the sum of squares of the other two sides (a² + b² = c²).",
            "what is pi": "Pi (π) is the ratio of a circle's circumference to its diameter. It's approximately equal to 3.14159.",
            "what are prime numbers": "Prime numbers are numbers greater than 1 that have no positive divisors other than 1 and themselves."
        },
        "history": {
            "who was albert einstein": "Albert Einstein was a renowned physicist who developed the theory of relativity. He's considered one of the most influential scientists of the 20th century.",
            "what is the renaissance": "The Renaissance was a period of European history between the 14th and 17th centuries marking the transition from medieval to modern times.",
            "what caused world war 1": "World War I was triggered by the assassination of Archduke Franz Ferdinand but had deeper causes including nationalism, imperialism, and complex alliances."
        }
    }

def get_audio_input():
    """Function to capture audio input and convert to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Speak your question.")
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            return text.lower()
        except sr.WaitTimeoutError:
            return "No speech detected"
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Could not request results"

def find_answer(question):
    """Function to find answer in the QA database"""
    question = question.lower()
    
    # Update user history
    for category in st.session_state.qa_data:
        if any(q in question for q in st.session_state.qa_data[category]):
            st.session_state.user_history[category] += 1
    
    # Search for exact matches
    for category in st.session_state.qa_data:
        for q, a in st.session_state.qa_data[category].items():
            if q in question:
                return a, category
    
    # If no exact match, return a suggestion
    return "I'm not sure about that. Try asking about topics like photosynthesis, gravity, or prime numbers.", None

def suggest_question():
    """Function to suggest questions based on user history"""
    if not st.session_state.user_history:
        # If no history, suggest random category
        category = random.choice(list(st.session_state.qa_data.keys()))
    else:
        # Suggest from most viewed category
        category = max(st.session_state.user_history, key=st.session_state.user_history.get)
    
    # Get random question from category
    question = random.choice(list(st.session_state.qa_data[category].keys()))
    return f"Try asking: {question}?"

# Streamlit UI
st.title("Voice-Controlled Educational Aid")
st.write("Ask questions about Science, Math, or History!")

# Add sidebar with user statistics
st.sidebar.title("Learning Statistics")
for category, count in st.session_state.user_history.items():
    st.sidebar.metric(f"{category.title()} Questions", count)

# Main interface
col1, col2 = st.columns(2)

with col1:
    if st.button("Start Voice Input"):
        question = get_audio_input()
        if question not in ["No speech detected", "Could not understand audio", "Could not request results"]:
            st.write("You asked:", question)
            answer, category = find_answer(question)
            st.write("Answer:", answer)
            if category:
                st.success(f"Category: {category.title()}")
        else:
            st.error(question)

with col2:
    # Text input alternative
    text_question = st.text_input("Or type your question here:")
    if text_question:
        answer, category = find_answer(text_question)
        st.write("Answer:", answer)
        if category:
            st.success(f"Category: {category.title()}")

# Show suggested questions
st.markdown("---")
st.write("Need ideas?")
if st.button("Suggest a question"):
    suggestion = suggest_question()
    st.info(suggestion)

# Add a section for learning progress
st.markdown("---")
st.subheader("Your Learning Journey")
if st.session_state.user_history:
    # Create a simple bar chart of categories explored
    chart_data = {
        "Category": list(st.session_state.user_history.keys()),
        "Questions Asked": list(st.session_state.user_history.values())
    }
    st.bar_chart(chart_data)
else:
    st.write("Start asking questions to see your learning progress!")
