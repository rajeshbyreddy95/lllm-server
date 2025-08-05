from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import requests

app = Flask(__name__)
CORS(app)

def ask_ollama(question, model="gemma3:4b"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": question,
        "stream": False
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()["response"].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "successfully running"})

@app.route('/chat', methods=['POST'])
def chat_response():
    data = request.get_json()
    question = data.get('message')
    print(question)
    if not question:
        return jsonify({"response": "No question received"}), 400

    answer = ask_ollama(question)
    return jsonify({"response": answer})

# Run Flask in a separate thread (if embedding inside another script)


# If running standalone:
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)

