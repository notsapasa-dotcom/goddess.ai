from app.openai_client import OpenAIClient

if __name__ == "__main__":
    # Minimal CLI for testing
    config_path = "config.json"
    openai_client = OpenAIClient(config_path)
    print("goddess.ai (eris) - minimal CLI test\n")
    while True:
        user_message = input("you: ")
        if user_message.lower() in ("exit", "quit"): break
        # Read system prompt from file
        with open("app/system_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read().strip()
        response = openai_client.get_chat_response(system_prompt, user_message)
        print(f"goddess.ai: {response}\n")
