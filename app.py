import streamlit as st
from google import genai
from google.genai import types
import requests
from pathlib import Path

from prompts import SUMMARY_REQUEST_PROMPT, SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE

MODEL_NAME = "gemini-3.5-flash"

st.set_page_config(
    page_title="DocAction",
    page_icon="📄"
)

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)

gemini_client = get_gemini_client()

def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])

def add_message(role, kind, content):
    st.session_state.messages.append(
        {"role": role, "kind": kind, "content": content}
    )
    render_message(st.session_state.messages[-1])

def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as error:
        return f"Sorry, something went wrong: {error}"

def clean_telegram_text(text):
    if not text:
        return "No document summary available."
    text = " ".join(text.split())
    return text[:4000] + "..." if len(text) > 4000 else text

def send_telegram(chat_id, user_name, summary):
    try:
        message = (
            f"📄 DocAction Summary\n\n"
            f"Hello {user_name}!\n\n"
            f"{clean_telegram_text(summary)}"
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return True, "Telegram message sent successfully!"
        return False, response.text
    except Exception as error:
        return False, str(error)

# Step 1: onboarding
if "onboarded" not in st.session_state:
    st.title("📄 DocAction")
    st.caption("Snap it. Understand it. Take action.")
    st.subheader("📲 Connect Telegram")
    st.info(
        "Follow these steps to receive your document summaries directly on Telegram."
    )
    st.markdown(
        """
        **Step 1:** Open our Telegram bot: [@DocActionAIBot](https://t.me/DocActionAIBot)

        **Step 2:** Press **Start** in the bot.

        **Step 3:** Open [@userinfobot](https://t.me/userinfobot) 
        and press **Start**.

        **Step 4:** Copy the **ID** shown by @userinfobot and enter it below.
        """
    )
    st.divider()
    with st.form("onboarding_form"):
        name = st.text_input(
            "Your name",
            placeholder="Enter your name"
        )
        telegram_chat_id = st.text_input(
            "Telegram Chat ID",
            placeholder="Example: 123456789",
            help="Enter the ID provided by @userinfobot."
        )
        submitted = st.form_submit_button("Let's go 🚀")
    if submitted:
        if not name.strip() or not telegram_chat_id.strip():
            st.warning(
                "Please enter both your name and Telegram Chat ID."
            )
        else:
            st.session_state.name = name.strip()
            st.session_state.telegram_chat_id = telegram_chat_id.strip()
            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                ),
            )
            st.session_state.messages = []
            st.session_state.onboarded = True
            st.rerun()
    st.stop()

# Step 2: chat interface
header_col, button_col = st.columns(
    [5, 2],
    vertical_alignment="center"
)

with header_col:
    st.title("📄 DocAction")

with button_col:
    send_disabled = len(st.session_state.messages) <= 2
    if st.button(
        "📤 Send to Telegram",
        disabled=send_disabled,
        use_container_width=True
    ):
        with st.spinner("Preparing your document summary..."):
            summary = ask_gemini(
                [SUMMARY_REQUEST_PROMPT]
            )
        success, info = send_telegram(
            st.session_state.telegram_chat_id,
            st.session_state.name,
            summary
        )
        if success:
            st.success(
                "Sent! Check your Telegram 📲"
            )
        else:
            st.error(
                f"Couldn't send that: {info}"
            )

st.caption(
    f"Logged in as {st.session_state.name} - "
    f"updates go to Telegram Chat ID: "
    f"{st.session_state.telegram_chat_id}"
)

if not st.session_state.messages:
    add_message(
        "assistant",
        "text",
        WELCOME_MESSAGE_TEMPLATE.format(
            name=st.session_state.name
        )
    )
else:
    for message in st.session_state.messages:
        render_message(message)

user_input = st.chat_input(
    "Ask a question, or attach a document",
    accept_file=True,
    file_type=["jpg", "jpeg", "png", "pdf"],
)

if user_input:
    document = (
        user_input.files[0]
        if user_input.files
        else None
    )
    text = user_input.text
    parts = []
    if document is not None:
        document_bytes = document.getvalue()
        add_message(
            "user",
            "image",
            document_bytes
        )
        parts.append(
            types.Part.from_bytes(
                data=document_bytes,
                mime_type=document.type
            )
        )
    if text:
        add_message(
            "user",
            "text",
            text
        )
        parts.append(text)
    elif document is not None:
        parts.append(
            "Analyze this document. "
            "Identify what type of document it is, "
            "extract the important information, "
            "find any deadlines, due dates, amounts, "
            "or required actions, "
            "and explain clearly what the user needs to do."
        )
    with st.spinner("Analyzing your document..."):
        answer = ask_gemini(parts)
    add_message(
        "assistant",
        "text",
        answer
    )