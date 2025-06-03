import streamlit as st
import subprocess

# Must be first Streamlit command
st.set_page_config(layout="wide")

# Load custom styles
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<div class="chat-title">🤖 EduAssist Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

# Wrapper for vertical centering
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

def ask_ollama_cli(messages, max_context=5):
    context_msgs = messages[-max_context:]
    prompt = ""
    for msg in context_msgs:
        prefix = "You: " if msg['role'] == 'user' else "Bot: "
        prompt += prefix + msg['content'] + "\n"
    prompt += "Bot: "

    try:
        result = subprocess.run(
            ['ollama', 'run', 'mistral', prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
        )
        stdout = result.stdout.decode('utf-8', errors='ignore').strip()
        stderr = result.stderr.decode('utf-8', errors='ignore').strip()

        if result.returncode == 0 and stdout:
            return stdout
        else:
            return f"Error: {stderr or 'Unknown error'}"
    except subprocess.TimeoutExpired:
        return "Sorry, the model took too long to respond. Please try again."
    except Exception as e:
        return f"Exception: {str(e)}"

# Layout: 2 columns
col1, col2 = st.columns(2)

# Left side: user input and history
with col1:
    st.markdown("### 💬 Your Question")
    user_input = st.text_area("Type here:", value="", height=150, label_visibility="collapsed", key="input_text")

    if st.button("Send"):
        user_input = user_input.strip()
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Bot is typing..."):
                bot_reply = ask_ollama_cli(st.session_state.messages)
            st.session_state.messages.append({"role": "bot", "content": bot_reply})
            st.rerun()

    st.markdown("### 🕘 Chat History")
    with st.container():
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"**🧑 You:** {msg['content']}", unsafe_allow_html=True)

# Right side: bot responses only
with col2:
    st.markdown("### 🤖 Bot Replies")
    with st.container():
        for msg in st.session_state.messages:
            if msg["role"] == "bot":
                st.markdown(f"<div class='bot-response'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
