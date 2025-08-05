from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Initializes OpenAI client from OPENAI_API_KEY env variable
client = OpenAI()

def ask_openai(question, model="gpt-3.5-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": question}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Server is running"})

@app.route('/chat', methods=['POST'])
def chat_response():
    data = request.get_json()
    question = data.get('message')
    if not question:
        return jsonify({"response": "No question received"}), 400

    answer = ask_openai(question)
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
