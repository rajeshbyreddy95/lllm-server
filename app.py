from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}}, supports_credentials=True)

OLLAMA_API_URL = "http://43.204.231.116:11434/api/generate"

@app.route('/chat', methods=['GET'])
def stream_response():
    prompt = request.args.get('message', '')

    if not prompt:
        return jsonify({'error': 'Missing message'}), 400

    def generate():
        payload = {
            "model": "gemma3:4b",
            "prompt": prompt,
            "stream": True
        }

        try:
            with requests.post(OLLAMA_API_URL, json=payload, stream=True, timeout=60) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        if 'response' in chunk:
                            yield f"data: {chunk['response']}\n\n"
        except requests.exceptions.RequestException as e:
            yield f"data: ⚠️ Server error: {str(e)}\n\n"

    return Response(generate(), mimetype='text/event-stream', headers={
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)