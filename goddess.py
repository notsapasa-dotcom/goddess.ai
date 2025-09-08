


# Simple goddess.ai Chatbot - Enhanced Version
from flask import Flask, request, jsonify, render_template
from personality_manager import GoddessPersonality
from openai_client import OpenAIClient
import os

app = Flask(__name__)
personality = GoddessPersonality(os.path.join(os.path.dirname(__file__), 'personality.json'))
openai_client = OpenAIClient(os.path.join(os.path.dirname(__file__), 'config.json'))
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        print(f"Received message: {user_message}")  # Debug log
        try:
            ai_response = personality.generate_full_response(user_message, openai_client)
            print(f"AI Response: {ai_response}")  # Debug log
            return jsonify({"response": ai_response})
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")  # Debug log
            return jsonify({"error": f"OpenAI API Error: {str(e)}"}), 500
    except Exception as e:
        print(f"Server Error: {str(e)}")  # Debug log
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    print("goddess.ai is starting...")
    app.run(debug=True, port=5000)

# Test with: curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d '{"message":"Hello"}'
