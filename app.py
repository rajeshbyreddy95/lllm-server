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
@app.route('/chat', methods=['GET'])
def stream_response():
    prompt = request.args.get('message', '')
    def generate():
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "gemma3:4b",
            "prompt": prompt,
            "stream": True
        }

        with requests.post(url, json=payload, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    yield f"data: {chunk.get('response', '')}\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
