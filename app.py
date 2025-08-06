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
def stream_response():
    data = request.get_json()
    prompt = data.get('message', '').strip()
    model = data.get('model', 'gemma3:4b')  # default to gemma3:4b

    if not prompt:
        return jsonify({"error": "Missing 'message' in request"}), 400

    def generate():
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True
        }

        try:
            with requests.post(OLLAMA_API_URL, json=payload, stream=True) as response:
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        yield f"data: {chunk.get('response', '')}\n\n"
        except requests.exceptions.RequestException as e:
            yield f"data: [Error connecting to Ollama API: {e}]\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
