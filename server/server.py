from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import dj_database_url

load_dotenv()
gemini_key = os.getenv("gemini_key")
postgres_url = os.getenv("postgres_url")

# configure api key
os.environ["GOOGLE_API_KEY"] = gemini_key

# configure postgres
if postgres_url:
    os.environ["DATABASE_URL"] = postgres_url
    database_config = dj_database_url.parse(postgres_url)
else:
    # Placeholder for handling cases where postgres_url is not set
    print("Postgres URL is not set. Please configure the environment variable.")
    # use gemini for prompting
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_google_genai import ChatGoogleGenerativeAI

# database connection
import psycopg2

try:
    conn = psycopg2.connect(
        dbname=database_config['NAME'],
        user=database_config['USER'],
        password=database_config['PASSWORD'],
        host=database_config['HOST'],
        port=database_config['PORT']
    )
    print("Database connection established successfully.")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    conn = None
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
        "items": ['Coke', 'Sprite', 'Pepsi']
    })

# run app
if __name__ == "__main__":
    app.run(debug=True, port=5000)