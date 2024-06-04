import os
import openai
import requests
import dotenv

dotenv.load_dotenv()
from flask import render_template
from flask import Flask, request, jsonify
from flask_cors import CORS
OPENAI_API_KEY = "Your_api_key_here"


# i decided to use chromadb as my vector database more details can be found in emir_scraping.ipynb
import chromadb
client = chromadb.Client(settings=chromadb.Settings(is_persistent=True,
                                    persist_directory="./vectordb",))
collection = client.get_collection("UAEgov")


app = Flask(__name__)
CORS(app)

@app.route('/')
def ask():
    return render_template('./index.html')

client = openai.OpenAI(
    # This is the default and can be omitted
    api_key=OPENAI_API_KEY,
)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message') 
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400


    response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": user_message + "Knowing the following knowledge: " + collection.query(
    query_texts = [user_message],
    include = ["documents"],
    n_results = 1
)['documents'][0][0],
        }
    ],
    model="gpt-3.5-turbo",
)
    api_response = response.model_dump_json()
    chat_response = api_response['choices'][0]['message']['content']
    return jsonify({"response": chat_response})

if __name__ == '__main__':
    app.run(port=8000)




