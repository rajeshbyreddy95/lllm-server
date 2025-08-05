from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)
client = OpenAI()
# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(question, model="gpt-3.5-turbo"):
    try:
        
        response = client.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": question}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "successfully running"})

@app.route('/chat', methods=['POST'])
def chat_response():
    data = request.get_json()
    question = data.get('message')
    print(f"Received: {question}")
    if not question:
        return jsonify({"response": "No question received"}), 400

    answer = ask_openai(question)
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
