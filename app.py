import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import google.generativeai as genai
import json
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Akphaio - Cybersecurity AI Assistant", layout="centered")
st.title("🛡️ AKP CYBERSEC - Cybersecurity & Ethical Hacking AI Assistant")
st.caption("Empowering ethical hackers with AI ⚡")

# --- LOAD LOTTIE ANIMATION ---
def load_lottie(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception:
        return None

# --- SIDEBAR MENU ---
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Chat", "About"],
        icons=["chat", "info-circle"],
        default_index=0
    )
    lottie = load_lottie("assets/hacker.json")
    if lottie:
        st_lottie(lottie, height=180)

# --- CONFIGURE GOOGLE GENERATIVE AI ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY") or "YOUR_API_KEY_HERE")
model = genai.GenerativeModel("gemini-pro")

# --- SESSION STATE SETUP ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are Amal, a professional cybersecurity and ethical hacking AI assistant. "
                "Provide expert advice on topics like penetration testing, network security, security tools, "
                "bug bounty, and responsible disclosure. Avoid illegal or unethical guidance."
            )
        }
    ]

# --- CHAT PAGE ---
if selected == "Chat":
    user_input = st.chat_input("Ask Amal anything about cybersecurity or ethical hacking...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Akphaio is thinking..."):
            response = model.generate_content(st.session_state.messages)
            assistant_reply = response.text
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- ABOUT PAGE ---
elif selected == "About":
    st.markdown("""
    ## 🔐 About AKP CYBERSEC

    **Akphaio** is your intelligent AI assistant, built to help cybersecurity professionals, ethical hackers,
    and learners explore secure practices and advanced tools including:

    - 🛡️ Penetration Testing
    - 🔍 Network Security & Reconnaissance
    - 🧰 Tools like Nmap, Metasploit, Burp Suite, Wireshark
    - 🐞 Bug Bounty & Responsible Disclosure
    - ⚠️ Secure Coding & Cyber Threat Awareness

    **Important:** Amal K P promotes only ethical and legal cybersecurity practices.

    ---
    👨‍💻 Built by Amal K P ( bca student @ JNIAS )
    """)
