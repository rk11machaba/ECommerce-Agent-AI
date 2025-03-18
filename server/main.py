from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# flask app setup
app = Flask(__name__)
CORS(app) # allow frontend request

# supabase setup

#signup route
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are nrequired"}), 400
    
    return jsonify({"message": "Signup successful"})

# login route
@app.route("signin", method=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")


if __name__ == "__main__":
    app.run(debug=True)
    
