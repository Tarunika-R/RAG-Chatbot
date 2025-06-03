import streamlit as st
import subprocess

st.set_page_config(page_title="College Helpdesk Chatbot")

st.title("College Helpdesk Chatbot (Ollama CLI)")

if "history" not in st.session_state:
    st.session_state.history = []

def ask_ollama_cli(question):
    try:
        result = subprocess.run(
            ['ollama', 'run', 'mistral', question],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120
        )
        # Decode output with utf-8 ignoring errors instead of using text=True
        stdout = result.stdout.decode('utf-8', errors='ignore').strip()
        stderr = result.stderr.decode('utf-8', errors='ignore').strip()
        
        if result.returncode == 0:
            return stdout
        else:
            return f"Error: {stderr}"
    except subprocess.TimeoutExpired:
        return "Sorry, the model took too long to respond. Please try again."
    except Exception as e:
        return f"Exception: {str(e)}"

def on_submit():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.history.append({"role": "user", "content": user_input})
        answer = ask_ollama_cli(user_input)
        st.session_state.history.append({"role": "bot", "content": answer})
        st.session_state.user_input = ""  # Clear input after submit

def main():
    st.text_input("Ask your question:", key="user_input", on_change=on_submit)

    for chat in st.session_state.history:
        if chat["role"] == "user":
            st.markdown(f"**You:** {chat['content']}")
        else:
            st.markdown(f"**Bot:** {chat['content']}")

if __name__ == "__main__":
    main()
