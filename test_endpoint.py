import unittest
import os
import json
import requests
import sys

from app import app, initialize_env
from pymongo import MongoClient
from pymongo import errors

#load values from .env for unit testing
from dotenv import load_dotenv
load_dotenv()

port = eval(os.environ.get("mongo_db_port"))
db = MongoClient(os.environ.get("mongodb_server"), port).test.incremental_counter

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
 
    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        initialize_env(testing=True)
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.testing = True

        #This indicate the unit test database
        self.db = MongoClient('localhost', 27017).test.users
        
        #Test case for the unit testing 
        #Which involves registering 1 user for test
        self.new_users = {"email":"igeadetokunbo@gmail.com","password":"123455"}

    #Destory the content of the test database once done   
    def tearDown(self):
        self.db.delete_many({})

    #Test registering users to the database
    #Ensure it returns just 1 record that was used as a test case
    def test_add_user_get_token(self):
        self.app.post('/v1/register',data=json.dumps(self.new_users),content_type='application/json')
        self.assertEqual(self.db.count(), 1)
    
    #Test registering users to the database returns 201 when a user is created
    #Also, check the count of the database 
    def test_when_new_config_is_created_status_code_is_201(self):
        response = self.app.post('/v1/register',data=json.dumps(self.new_users),content_type='application/json')
        self.assertEqual(response.status_code, 201)
  
if __name__ == '__main__':
    unittest.main()