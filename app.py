import os, json, time, jwt
import datetime

from flask import Flask, request, Response, jsonify
from pymongo import MongoClient, errors
from flask_bcrypt import Bcrypt

from bson.json_util import dumps
from functools import wraps

app = Flask(__name__)
time.sleep(5) # to ensure mongodb runs immediately the app comes up

#load values from .env for unit testing
from dotenv import load_dotenv
load_dotenv()

#This manages the client between unit testing and rest api
def initialize_env(testing = False):
    global db
    if testing:
        #Pick all this values from env variables
        port = eval(os.environ.get("mongo_db_port"))
        db = MongoClient(os.environ.get("mongodb_server"), port).test
        app.config['SECRET_KEY'] = os.environ.get("secret_key")
        intial_incremental_value_env = os.environ.get("intial_incremental_value")
    else:
        #Pick all this values from yaml file
        port = eval(os.getenv("mongo_db_port"))
        db = MongoClient(os.getenv("mongodb_server"), port).thinkific_challenge
        app.config['SECRET_KEY'] = os.getenv("secret_key")
        intial_incremental_value_env = os.getenv("intial_incremental_value")

flask_bcrypt = Bcrypt(app)

#Implemented the jwt function which generates the token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({"status": "Token not present!", "data": "Token is not provided, pls supply the token!"}), 404 

        try:
            jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message':'Token is invalid or it has expired'}), 403
    
        return f(*args, **kwargs)

    return decorated

def get_incremented_id():
    #check the incremental_id of the last registered incremental_counter in the database
    incremental_counter_details = db.incremental_counter.find({})

    if db.incremental_counter.count() == 0:
        #check if incremental_counter collection exist and 
        #create intial value in the collection

        #Get the intial_incremental_value from the yaml file, this assumes that there should be a initial value
        intial_incremental_value = intial_incremental_value_env
        db.incremental_counter.insert_one({'incremental_id': intial_incremental_value, 'name': 'counter'})
        incremental_counter = intial_incremental_value
    else:
        incremental_counter = ''
        for detail in incremental_counter_details:
            incremental_counter+= (str(detail["incremental_id"]))
    return incremental_counter
       
#Ensure token exist and it is valid before accepting the request       
@app.route('/v1/next', methods=["GET"])
@token_required
def next_integer():
    #Get the last integer
    former_integer = int (get_incremented_id())
    incrementer_integer =  former_integer + 1 
     
    #build up the update values 
    set = {}    
    name = 'counter'
    set['incremental_id'] = incrementer_integer

    response = db.incremental_counter.update_one({'name' : name}, {'$set': set}) 
    if response:
        return jsonify({"Former Integer": former_integer, "Next Integer":incrementer_integer})

#Ensure token exist and it is valid before accepting the request
@app.route('/v1/current', methods=["GET"])
@token_required
def current_integer():
    current_integer = int (get_incremented_id())
    return jsonify({"Current Integer": current_integer})

#Ensure token exist and it is valid before accepting the request
@app.route('/v1/current', methods=["PUT"])
@token_required
def reset_integer():
    data =  request.get_json()

    current = data['current']
    current = int(current)
    if current < 0:
        return jsonify({"status": "Integer will have to be a postive number!", "data": "Pls do provide a postive value, the value you provided is a negative value!"}), 404 

    #£nsure that email exist in the request
    if 'current' not in data: 
        return jsonify({"status": "Current integer not present!", "data": "The current integer is not provided, pls supply the current integer!"}), 404

    #build up the update values 
    set = {}
    set['incremental_id'] =  current

    response = db.incremental_counter.update_one({'name' : 'counter'}, {'$set': set})
    if not response:
        return jsonify({"Status":"An issue has occurred!"})
    return jsonify({"Current Integer is now": current, "data":"The current integer has been successfully updated!"})

def check_email(email):
    #if email already exist, don't insert into the database
    user = db.users.find_one({'email' : email})
    if user:
        return user

@app.route('/v1/register', methods=['POST'])
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

    #Get the incremented_id in the users collection
    #This is to keep track of who inserted the value 
    incremented_id = get_incremented_id()

    token = jwt.encode({'email':email,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=600)}, app.config['SECRET_KEY'])
    if email and password and token:
        response = db.users.insert_one({
            'incremented_id': incremented_id,
            'email': email,
            'password': password,
            'token':token
        })

    if response:
        return jsonify({"status": "ok", "data": "The user has been created successfully and token generated, please use that token for login!", "token expiry": "600 minutes", "token": token.decode('UTF-8')}),201
    else:
        return jsonify({"status": "Could not verify!", "data": "'www-Authenticate': 'Basic realm='Login Required''"}), 400

#health endpoint which checks that mongodb is up and the service is up 
@app.route("/health")
def healthcheck():
    check_mongodb = "True"
    if not db:
        check_mongodb = "False"
    return jsonify({"status": "ok", "check Mongodb": check_mongodb })

if __name__ == '__main__':
    initialize_env()
    port = os.getenv("SERVER_PORT")
    app.config['DEBUG'] = True
    app.run(debug=False, host='0.0.0.0')