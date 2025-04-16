from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['cqrs_db']
items_collection = db['items']

# Authentication setup
auth = HTTPBasicAuth()

# Example user data
users = {
    "admin": generate_password_hash("password")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

# Command: Create an item
@app.route('/items', methods=['POST'])
@auth.login_required
def create_item():
    data = request.get_json()
    item = {
        'name': data['name'],
        'description': data['description']
    }
    result = items_collection.insert_one(item)
    item['_id'] = str(result.inserted_id)
    return jsonify({'message': 'Item created successfully', 'item': item}), 201

# Query: Get all items
@app.route('/items', methods=['GET'])
@auth.login_required
def get_items():
    items = list(items_collection.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return jsonify({'items': items}), 200

if __name__ == '__main__':
    app.run(debug=True)

# This code is a simple Flask application that demonstrates the CQRS pattern with MongoDB.
# It allows users to create and retrieve items using HTTP requests.
# The application uses basic authentication to secure the endpoints.
# The `create_item` function handles the command to create a new item,
# while the `get_items` function handles the query to retrieve all items.
# The items are stored in a MongoDB collection, and the application uses the PyMongo library to interact with the database.
# The `verify_password` function checks the username and password against the stored user data.
# The application runs on localhost with debugging enabled.
# To run the application, save this code in a file named `app.py` and run it using Python.          