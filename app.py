import os, json, time

from flask import Flask, request, Response,jsonify
from pymongo import MongoClient, errors
from flask_bcrypt import Bcrypt

from bson.json_util import dumps

app = Flask(__name__)
time.sleep(5) # to ensure mongodb runs immediately the app comes up

users = MongoClient('localhost', 27017).thinkific_challenge.users
flask_bcrypt = Bcrypt(app)

# Get the last id in the database

@app.route('/register', methods=['POST'])
def register():

    data = request.get_json()  
    #£nsure that email exist in the request
    if 'email' not in data:
        return jsonify({"status": "Email not present!", "data": "Email is not provided, pls supply the email!"}), 404

    #£nsure that password exist in the request
    if 'password' not in data:
        return jsonify({"status": "Password not present!", "data": "Password is not provided, pls supply the password!"}), 404

    email = data['email']
    password = flask_bcrypt.generate_password_hash(data['password'])

    if email and password:
        response = users.insert_one({
            'email': email,
            'password': password
        })

    if response:
        return jsonify({"status": "ok", "data": "User created successfully!"}),200
    else:
        return jsonify({"status": "failed", "data": "Error, there was an issue!"}), 400

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')