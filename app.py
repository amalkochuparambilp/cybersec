import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="Akphaio - Cybersecurity AI Assistant", layout="centered")
st.title("🛡️ Akphaio - Cybersecurity & Ethical Hacking AI Assistant")
st.caption("Empowering ethical hackers with AI ⚡")

# --- LOGIN SYSTEM WITH NICKNAME ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔐 Login to Access Akphaio")
    user_name = st.text_input("Enter your nickname")
    user_api_key = st.text_input("Enter your Gemini API Key", type="password")

    if st.button("Login"):
        try:
            genai.configure(api_key=user_api_key)
            test_model = genai.GenerativeModel("gemini-pro")
            test_model.generate_content("Say hello")  # Validate key
            st.session_state.api_key = user_api_key
            st.session_state.authenticated = True
            st.session_state.user_name = user_name or "Hacker"
            st.success(f"Welcome, {st.session_state.user_name}! 🔐")
            st.rerun()
        except Exception:
            st.error("Invalid API key. Please try again.")
    st.stop()

# --- CONTINUE IF LOGGED IN ---
genai.configure(api_key=st.session_state.api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# --- SIDEBAR MENU WITH LOGOUT ---
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Chat", "About"],
        icons=["chat", "info-circle"],
        default_index=0
    )
    st.markdown("---")
    st.write(f"👋 Hello, **{st.session_state.get('user_name', 'Hacker')}**")
    if st.button("🔓 Logout"):
        st.session_state.authenticated = False
        st.session_state.api_key = ""
        st.session_state.messages = []
        st.session_state.user_name = ""
        st.experimental_rerun()

# --- SESSION STATE SETUP ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are Akphaio, a professional cybersecurity and ethical hacking AI assistant. "
                "Provide expert advice on topics like penetration testing, network security, security tools, "
                "bug bounty, and responsible disclosure. Avoid illegal or unethical guidance."
            )
        }
    ]

# --- CHAT PAGE ---
if selected == "Chat":
    user_input = st.chat_input("Ask Akphaio anything about cybersecurity or ethical hacking...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Akphaio is thinking..."):
            contents = [
                {
                    "type": "text",
                    "text": msg["content"],
                    "author": msg["role"]
                }
                for msg in st.session_state.messages
            ]
            response = model.generate_content(contents)
            assistant_reply = response.text
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- ABOUT PAGE ---
elif selected == "About":
    st.markdown("""
    ## 🔐 About Akphaio

    **Akphaio** is your intelligent AI assistant, built to help cybersecurity professionals, ethical hackers,
    and learners explore secure practices and advanced tools including:

    - 🛡️ Penetration Testing  
    - 🔍 Network Security & Reconnaissance  
    - 🧰 Tools like Nmap, Metasploit, Burp Suite, Wireshark  
    - 🐞 Bug Bounty & Responsible Disclosure  
    - ⚠️ Secure Coding & Cyber Threat Awareness  

    **Important:** Akphaio promotes only ethical and legal cybersecurity practices.

    ---
    👨‍💻 Built by [Your Name or Organization]
    """)