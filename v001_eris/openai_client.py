import os
import json
import openai

class OpenAIClient:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        openai.api_key = config['api_key']

    def get_chat_response(self, system_prompt, user_message, model="gpt-3.5-turbo"):
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message['content']
