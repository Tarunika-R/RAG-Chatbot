import requests

OLLAMA_API_URL = "http://localhost:11434/api/chat/completions"

def chat_with_mistral(messages):
    """
    messages: list of dicts like
    [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello!"}, ...]
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "mistral",
        "messages": messages
    }

    response = requests.post(OLLAMA_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    assistant_message = data["choices"][0]["message"]["content"]
    return assistant_message
