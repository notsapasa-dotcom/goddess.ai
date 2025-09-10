import os
import openai
import json


SYSTEM_PROMPT_DIR = os.path.dirname(__file__)
DEFAULT_SYSTEM_PROMPT = os.path.join(SYSTEM_PROMPT_DIR, "system_prompt.txt")

def get_system_prompt(archetype=None):
    if archetype:
        prompt_path = os.path.join(SYSTEM_PROMPT_DIR, f"system_prompt_{archetype}.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read().strip()
    # fallback to default
    with open(DEFAULT_SYSTEM_PROMPT, "r", encoding="utf-8") as f:
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
    current_archetype = None
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

        # Summon archetype logic
        if user_message.lower().startswith("summon "):
            archetype = user_message[7:].strip().lower()
            if archetype == "sa":
                # Always use default system prompt for 'sa'
                current_archetype = None
                system_prompt = get_system_prompt()
                print(f"[Archetype 'sa' uses default system prompt.]")
            else:
                prompt = get_system_prompt(archetype)
                if prompt:
                    current_archetype = archetype
                    system_prompt = prompt
                    print(f"[System prompt updated to archetype: {archetype}]")
                else:
                    print(f"[Archetype '{archetype}' not found. Using default system prompt.]")
                    current_archetype = None
                    system_prompt = get_system_prompt()
            # Reset conversation with new system prompt
            messages = [{"role": "system", "content": system_prompt}]
            continue

        messages.append({"role": "user", "content": user_message})
        response = get_response(api_key, messages)
        display_name = current_archetype if current_archetype else "sa"
        print(f"{display_name}: {response}\n")
        messages.append({"role": "developer", "content": response})

if __name__ == "__main__":
    main()
