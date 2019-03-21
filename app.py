import os, json, time, pprint

from flask import Flask, request, Response,jsonify, make_response
from pymongo import MongoClient, errors
from flask_bcrypt import Bcrypt

from bson.json_util import dumps

app = Flask(__name__)
time.sleep(5) # to ensure mongodb runs immediately the app comes up

users = MongoClient('localhost', 27017).thinkific_challenge.users
flask_bcrypt = Bcrypt(app)

# Get the last id in the database

def get_last_user_id():
    #check the user_id of the last registered user in the database
    user = users.find().sort("user_id", -1)

    user_id = ''
    for x in user:
        user_id+=str(x)
    print(user_id)
    print("s")
    return user_id

def check_email(email):
    #if email already exist, don't insert into the database
    user = users.find_one({'email' : email})
    if user:
        return user

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

    #confirm if email exist in the database 
    #if it exist, there is no need add the credentials in the database
    check_email_exist = check_email(email)
    if check_email_exist:
        return jsonify({"status": "The email already exist!", "data": "The email exist, hence it can not be added!"}), 400

    #Get the last_user_id in the users collection
    #last_user_id = get_last_user_id()

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