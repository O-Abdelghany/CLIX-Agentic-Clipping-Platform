import os
import tempfile
import streamlit as st
from app.graph.graph import graph

st.set_page_config(page_title="CLIX", page_icon="🎬", layout="centered")

st.markdown("""
<style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
    }

    /* Hide default streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }

    /* Center column */
    .block-container {
        max-width: 760px !important;
        padding-top: 2rem !important;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
        padding: 0.75rem 1rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* User bubble */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: rgba(108, 99, 255, 0.15) !important;
        border-color: rgba(108, 99, 255, 0.3) !important;
    }

    /* Chat input bar */
    [data-testid="stChatInput"] {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 14px !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #f0f0f0 !important;
        background: transparent !important;
    }

    /* Upload area */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.04);
        border: 2px dashed rgba(108, 99, 255, 0.4);
        border-radius: 12px;
        padding: 0.5rem 1rem;
    }
    [data-testid="stFileUploader"] label { color: #a0a0c0 !important; }

    /* Transcribe button */
    .stButton > button {
        background: linear-gradient(90deg, #6c63ff, #a78bfa);
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85 !important; }

    /* Divider */
    hr { border-color: rgba(255,255,255,0.08) !important; }

    /* All text */
    p, label, span, div { color: #e0e0e0; }
    h1, h2, h3 { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align:center; letter-spacing:4px;'>🎬 CLIX</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#a0a0c0; margin-bottom:1.5rem;'>AI-powered video & audio transcription</p>", unsafe_allow_html=True)

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Upload expander above input ---
with st.expander("📎 Upload a video or audio file for transcription"):
    uploaded_file = st.file_uploader(
        "Supported: MP4, MKV, MP3, WAV, M4A, OGG, FLAC, WEBM",
        type=["mp4", "mkv", "mp3", "wav", "m4a", "ogg", "flac", "webm"],
        label_visibility="visible"
    )

    if uploaded_file:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption(f"📁 {uploaded_file.name}")
        with col2:
            transcribe_clicked = st.button("Transcribe", type="primary")

        if transcribe_clicked:
            with st.spinner("Transcribing... this may take a moment."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                try:
                    st.session_state.messages.append({
                        "role": "user",
                        "content": f"📎 Uploaded `{uploaded_file.name}` for transcription."
                    })

                    result = graph.invoke({
                        "messages": [{"role": "user", "content": tmp_path}]
                    })

                    last_message = result["messages"][-1]
                    transcription = last_message.content if hasattr(last_message, "content") else str(last_message)

                    st.session_state.messages.append({"role": "assistant", "content": transcription})
                    st.rerun()

                except Exception as e:
                    st.error(f"Something went wrong: {e}")
                finally:
                    os.unlink(tmp_path)

# --- Chat input ---
if prompt := st.chat_input("Message CLIX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(""):
            result = graph.invoke({"messages": st.session_state.messages})
            last_message = result["messages"][-1]
            response = last_message.content if hasattr(last_message, "content") else str(last_message)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
