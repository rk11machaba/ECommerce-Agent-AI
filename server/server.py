from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
gemini_key = os.getenv("gemini_key")

# configure api key
os.environ["GOOGLE_API_KEY"] = gemini_key

#use gemini for prompting
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


gemini = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


# app instance
app = Flask(__name__)
CORS(app)

# app route
@app.route("/api/home", methods=['GET'])
def return_home():

    # try single prompt
    prompt = "Please write a one line welcome message for our store"

    # call llm
    response = gemini.invoke(prompt)
    return jsonify({
        "message": response.content,
        "items": ['Laptop', 'Smart Phone', 'Router']
    })

# run app
if __name__ == "__main__":
    app.run(debug=True, port=5000)