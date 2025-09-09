from v001_eris.openai_client import OpenAIClient
from v001_eris.safety_layer import route_archetype_response

if __name__ == "__main__":
    # Minimal CLI for testing
    config_path = "config.json"
    openai_client = OpenAIClient(config_path)
    print("goddess.ai (eris) - minimal CLI test\n")
    while True:
        user_message = input("you: ")
        if user_message.lower() in ("exit", "quit"): break
        # Archetype routing: handle special cases before normal persona
        archetype_response = route_archetype_response(user_message)
        if archetype_response:
            print(f"goddess.ai: {archetype_response}\n")
            continue
        # Normal witty/chaotic persona response
        with open("v001_eris/system_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read().strip()
        response = openai_client.get_chat_response(system_prompt, user_message)
        print(f"goddess.ai: {response}\n")
