import os
from flask import Flask, render_template, request, jsonify
from gemini_client import GeminiClient

# Dynamically resolve template path
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

client = GeminiClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    payload = request.get_json(silent=True) or {}
    user_message = payload.get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response_text = client.generate_response(user_message)
        return jsonify({'response': response_text})
    except Exception as e:
        return jsonify({'error': 'Error generating response'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render provides PORT
    app.run(host='0.0.0.0', port=port, debug=True)