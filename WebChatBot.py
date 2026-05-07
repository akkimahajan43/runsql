import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
# -----------------------------
# Configure Page
# -----------------------------
st.set_page_config(
    page_title="Groq Chatbot",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# Title
# -----------------------------
st.title("🤖 Groq AI Chatbot")
# -----------------------------
# GROQ API KEY
# -----------------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# -----------------------------
# Session State for Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display Previous Messages
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# User Input
# -----------------------------
prompt = st.chat_input("Type your message...")

if prompt:

    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response area
    with st.chat_message("assistant"):

        response_placeholder = st.empty()
        full_response = ""

        # Streaming response
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful chatbot"
                },
                *st.session_state.messages
            ],
            stream=True
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content

            if content:
                full_response += content
                response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )