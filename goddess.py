# Simple goddess.ai Chatbot - Hello World Version
import openai
from flask import Flask, request, jsonify, render_template_string
from personality_manager import GoddessPersonality
import os
import json

app = Flask(__name__)
personality = GoddessPersonality(os.path.join(os.path.dirname(__file__), 'personality.json'))

# Load API key from config
with open(os.path.join(os.path.dirname(__file__), 'config.json')) as f:
    config = json.load(f)
openai.api_key = config['api_key']

@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>goddess.ai</title>
        <style>
            body { max-width: 800px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; }
            #chat { height: 400px; overflow-y: auto; border: 1px solid #ccc; margin-bottom: 10px; padding: 10px; }
            #message { width: 80%; padding: 8px; margin-right: 10px; }
            button { padding: 8px 15px; }
            .error { color: red; }
        </style>
    </head>
    <body>
        <h1>goddess.ai chatbot</h1>
        <div id="chat"></div>
        <div>
            <input type="text" id="message" placeholder="Type your message...">
            <button onclick="sendMessage()" id="sendButton">Send</button>
        </div>
        <script>
            const messageInput = document.getElementById('message');
            const sendButton = document.getElementById('sendButton');
            const chatDiv = document.getElementById('chat');

            // Allow sending message with Enter key
            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            async function sendMessage() {
                const message = messageInput.value.trim();
                if (!message) return;

                try {
                    // Disable input while processing
                    messageInput.disabled = true;
                    sendButton.disabled = true;

                    // Add user message
                    appendMessage('you', message);
                    messageInput.value = '';

                    // Send to server
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: message})
                    });

                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }

                    const data = await response.json();
                    appendMessage('goddess.ai', data.response);
                } catch (error) {
                    appendMessage('Error', 'Sorry, something went wrong. Please try again.');
                    console.error('Error:', error);
                } finally {
                    // Re-enable input
                    messageInput.disabled = false;
                    sendButton.disabled = false;
                    messageInput.focus();
                }
            }

            function appendMessage(sender, text) {
                const p = document.createElement('p');
                p.innerHTML = `<b>${sender}:</b> ${text}`;
                if (sender === 'Error') {
                    p.classList.add('error');
                }
                chatDiv.appendChild(p);
                chatDiv.scrollTop = chatDiv.scrollHeight;
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        print(f"Received message: {user_message}")  # Debug log
        
        try:
            # Analyze the message and get context
            message_analysis = personality.analyze_message(user_message)
            
            # Build the system message with current context
            system_prompt = personality.get_system_prompt()
            
            # Add contextual guidance based on message analysis
            style = message_analysis.get('style', 'neutral')
            if style == 'poetic':
                system_prompt += "\n\nUser speaks in poetic metaphors - mirror their ethereal energy"
            if message_analysis.get('is_tech_related'):
                system_prompt += "\n\nUser discusses technology - maintain reluctant interest"
                
            # Add suggested gesture if appropriate
            if message_analysis.get('needs_gesture') and message_analysis.get('suggested_gesture'):
                system_prompt += f"\n\nConsider using this gesture: {message_analysis['suggested_gesture']}"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            
            ai_response = response.choices[0].message['content']
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