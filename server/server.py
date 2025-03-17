from flask import Flask, jsonify
from flask_cors import CORS

# app instance
app = Flask(__name__)
CORS(app)

# app route
@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        "message": "Welcome to Our Store",
        "items": ['Laptop', 'Smart Phone', 'Router']
    })

# run app
if __name__ == "__main__":
    app.run(debug=True, port=5000)