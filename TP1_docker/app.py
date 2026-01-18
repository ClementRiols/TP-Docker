from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://mongo:27017/")
db = client.test_db

@app.route("/")
def hello_world():
    return "Hello World! Connexion à Mongo DB"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
