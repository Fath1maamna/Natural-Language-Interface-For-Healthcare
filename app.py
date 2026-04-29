import streamlit as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.append(str(SRC_PATH))

from dataset_loader import load_dataset
from response_handler import get_response
from logger import save_chat

st.set_page_config(page_title="Government Medical College", layout="wide")

if "data" not in st.session_state:
    st.session_state.data = load_dataset()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome to Government Medical College Chatbot. Ask about fever, doctor, bed, ambulance, appointment, or hospital status."
        }
    ]

# Header Banner
st.markdown("""
<div style='background: linear-gradient(90deg,#d9f3ff,#e8fff1); padding:20px; border-radius:20px;'>
    <h1 style='text-align:center;'>🏥 Government Medical College</h1>
    <h3 style='text-align:center;'>👨‍⚕️ Smart Healthcare Chatbot Portal 👩‍⚕️</h3>
    <p style='text-align:center; font-size:18px;'>Use the right-side buttons to open <b>Chatbot</b> or <b>Dashboard History</b></p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([4, 1.2])

with col2:
    st.markdown("## Navigation")
    page = st.radio(
        "Choose Section",
        ["💬 Chatbot", "📊 Dashboard History"]
    )

if page == "💬 Chatbot":
    st.subheader("💬 Healthcare Chatbot")

    st.image(
        "https://images.unsplash.com/photo-1631815588090-d4bfec5b1ccb",
        width='stretch'
    )

    st.markdown("""
    <div style='max-width:340px; background:white; border:2px solid #dbeafe; border-radius:18px; padding:15px;'>
        <h3>💬 Chatbot Box</h3>
    </div>
    """, unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.write(user_input)

        response = get_response(user_input, st.session_state.data)

        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.write(response)

        save_chat(user_input, response)

elif page == "📊 Dashboard History":
    st.subheader("📊 Dashboard History")
    st.write("Full chatbot conversation history")

    log_file = PROJECT_ROOT / "logs" / "chat_history.txt"

    if log_file.exists():
        with open(log_file, "r", encoding="utf-8") as file:
            history = file.read()

        st.text_area(
            "Chat History",
            value=history,
            height=500
        )
    else:
        st.info("No chat history available yet.")
