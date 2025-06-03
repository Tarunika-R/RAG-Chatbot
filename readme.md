# EduAssist: RAG Chatbot — Retrieval-Augmented Generation Chatbot

## Overview

This project is a **Retrieval-Augmented Generation (RAG) Chatbot** built with **Streamlit** that integrates a local LLM (via the Ollama CLI) to answer user queries based on a limited context window of past chat history.

The chatbot UI is designed for ease of use with:

- A **two-column layout** splitting user prompts (left) and bot answers (right).
- Scrollable chat history and bot response areas for better UX.
- A centered chatbot title on top.
- Real-time interaction powered by subprocess calls to a local language model (e.g., Mistral via Ollama).

---

## Technical Details

- **Frontend:** Streamlit for interactive UI with custom CSS for styling.
- **Backend/Inference:** Calls `ollama run mistral` command using Python's `subprocess` module to generate responses.
- **Session management:** Uses `st.session_state` to persist conversation history and input text.
- **Layout:** Utilizes Streamlit’s `columns()` for side-by-side input and output.
- **Scroll behavior:** Custom CSS scrollbars keep conversation history and bot replies scrollable independently.
- **Error handling:** Manages subprocess timeouts and exceptions gracefully with user-friendly messages.

---

## How It Works

1. **User inputs a question** in the left textarea.
2. The chat history (last 5 messages) is formatted as a prompt for the LLM.
3. The prompt is sent via subprocess to the Ollama CLI for inference.
4. The LLM's response is displayed on the right side in the bot reply container.
5. Both user and bot messages are appended to the session state and shown in their respective scrollable areas.
6. The UI is refreshed without losing chat context.

---

## Installation & Setup

### Prerequisites

- Python 3.8+
- Streamlit
- Ollama CLI installed and configured with the desired LLM (e.g., Mistral)
- `styles.css` file present alongside `app.py`

---

### Step-by-Step Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/rag-chatbot.git
   cd rag-chatbot

   ```

2. **Create & Activate a virtual environment (recommended)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate     # Linux/macOS
   .venv\Scripts\activate      # Windows

   ```

3. **Install dependencies**

   ```bash
   pip in streamlit

   ```

4. **Ensure Ollama CLI is installed**

   - Follow Ollama Installation guide
   - Install your chosen model, eg. `mistral`

5. **Verify `styles.css` file exists with the required CSS content**

6. **Run the app**

   ```bash
   streamlit run app.py

   ```

7. **Access the chatbot**
   Open your browser and navigate to `http://localhost:8501`

---

## File Structure

```bash
    rag-chatbot/
    ├── app.py # Main Streamlit app code
    ├── styles.css # Custom CSS for UI styling
    ├── README.md # Project documentation
    └── .venv/ # (Optional) Python virtual environment folder
```

---

## Customization

- Update `ask_ollama_cli()` to change LLM or prompt logic.
- Modify `style.css` for UI appearance tweaks.
- Adjust session state window size (`max_context`) for longer/shorter chat history.
- Add additional UI features such as button, icons or user authentication.

## Troubleshooting

- `StreamlitSetPageConfigMustBeFirstCommandError`: Make sure `st.set_page_config()` is the very first Streamlit command.

- No `experimental_rerun` attribute: Use `st.experimental_rerun()` only if your Streamlit version supports it, else refactor logic to avoid it.

- **Ollama errors**: Verify Ollama is installed correctly and your model is available.

## UI Screenshots

### Chatbot Interface

![Chatbot Interface](screenshots/ui1.png)

### Chatbot Response Area with Scrollbar

![Bot Response Scroll](screenshots/ui2.png)
