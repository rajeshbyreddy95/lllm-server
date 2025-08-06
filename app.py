from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# 👇 Use public EC2 URL where Docker Ollama is running
OLLAMA_API_URL = "http://43.204.231.116:11434/api/generate"

@app.route('/start', methods=['POST'])
def start_chat():
    data = request.get_json()
    message = data.get('message', '').strip()

    if not message:
        return jsonify({"error": "Missing 'message' field"}), 400

    return jsonify({"status": "started", "message": message})
@app.route('/chat', methods=['POST'])
def chat_response():
    data = request.get_json()
    prompt = data.get('message', '').strip()
    model = data.get('model', 'gemma3:4b')
    print(prompt)
    if not prompt:
        return jsonify({"error": "Missing 'message' in request"}), 400

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False  # ⛔ DISABLE STREAMING
    }

    try:
        res = requests.post(OLLAMA_API_URL, json=payload)
        response_json = res.json()
        return jsonify({"response": response_json.get("response", "").strip()})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Connection to Ollama failed: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
