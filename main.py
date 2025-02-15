import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables (optional)
load_dotenv()

# Set your Google Gemini API Key
API_KEY = os.getenv("GEMINI_API_KEY")

# API Endpoint for Gemini 1.5 Flash
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# Streamlit UI setup
st.set_page_config(page_title="Conversational Q&A Chatbot")
st.header("Hey, Let's Chat!")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to get response from Gemini API
def get_gemini_response(user_input):
    """Sends user input to Gemini API and returns the chatbot's response."""
    # Append user message to chat history
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": user_input}]})

    # Prepare request payload (excluding system role)
    payload = {
        "contents": st.session_state.chat_history[-5:]  # Keep only the last 5 messages for context
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_data = response.json()
        if "candidates" in response_data and response_data["candidates"]:
            chatbot_reply = response_data["candidates"][0]["content"]["parts"][0]["text"]
            st.session_state.chat_history.append({"role": "model", "parts": [{"text": chatbot_reply}]})
            return chatbot_reply
        else:
            return "Sorry, I couldn't get a response. Please try again."
    else:
        return f"Error: {response.status_code}, {response.text}"

# User input text box
user_input = st.text_input("Input:", key="input")

# Submit button
if st.button("Ask the question"):
    if user_input:
        response = get_gemini_response(user_input)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("Please enter a question.")
