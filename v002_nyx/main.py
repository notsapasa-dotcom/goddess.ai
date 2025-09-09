import os
import openai
import json

SYSTEM_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "system_prompt.txt")

def get_system_prompt():
    with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()

def get_response(api_key, messages):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"[OpenAI API error: {e}]"


def main():
    print("nyx v002 CLI\nType 'exit' to quit.\n")
    system_prompt = get_system_prompt()
    # Load your API key from an environment variable or config file
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        try:
            with open("config.json") as f:
                api_key = json.load(f)["api_key"]
        except Exception:
            print("[Error: OpenAI API key not found. Set OPENAI_API_KEY or provide config.json.]")
            return
    # Conversation history
    messages = [{"role": "system", "content": system_prompt}]
    while True:
        user_message = input("you: ")
        if user_message.lower() in ("exit", "quit"): break
        messages.append({"role": "user", "content": user_message})
        response = get_response(api_key, messages)
        print(f"nyx: {response}\n")
        messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
