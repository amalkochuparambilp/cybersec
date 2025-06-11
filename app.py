import streamlit as st
import google.generativeai as genai

# Load Gemini API key from Streamlit secrets
api_key = st.secrets["gemini"]["api_key"]
genai.configure(api_key=api_key)

# Initialize chat model
model = genai.GenerativeModel("gemini-pro")

# Session state for chat history
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.set_page_config(page_title="Gemini Chat", page_icon="🤖")
st.title("💬 Gemini GPT Chat App")

# Display chat history
for msg in st.session_state.chat.history:
    with st.chat_message("user" if msg.role == "user" else "ai"):
        st.markdown(msg.parts[0].text)

# Input box
prompt = st.chat_input("Type your message...")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send to Gemini API
    response = st.session_state.chat.send_message(prompt)

    with st.chat_message("ai"):
        st.markdown(response.text)