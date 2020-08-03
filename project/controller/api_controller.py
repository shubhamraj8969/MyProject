# Import flask Modules
from flask_restful import Resource
from flask import request
from flask import jsonify
import requests

# Current date and time
from datetime import datetime

# Import Database Modules
from helpers.DBHelper import DBHelper
from helpers.authenticate import *

TOKEN_KEY = "HTTP_AUTHORIZATION"

class APIController(Resource):
    def __init__(self):
        self.db = DBHelper()
    
    def get(self):
        if request.endpoint == 'call_api':
            return self.call_api()
        if request.endpoint == 'see_remaining_limits':
            return self.see_remaining_limits()

    @authenticate
    def see_remaining_limits(self):
        try:
            token = request.environ[TOKEN_KEY].split(' ')[1]
            sql = 'select username from user where token = "{}"'.format(str(token))
            username = self.db.query(sql).fetchone()
            sql = 'select count(*) from login_data where username = "{}" and created >= NOW() - INTERVAL 1 MINUTE;'.format(username["username"])
            count = self.db.query(sql).fetchone()
            print(count)
            return {"remaining": 5 - count["count(*)"]}, 200
        
        except Exception as err:
            print(err)
            return {"error": "Internal Server error"}, 500

    @authenticate
    def call_api(self):
        try:
            token = request.environ[TOKEN_KEY].split(' ')[1]
            sql = 'select username from user where token = "{}"'.format(str(token))
            username = self.db.query(sql).fetchone()
            sql = 'select count(*) from login_data where username = "{}" and created >= NOW() - INTERVAL 1 MINUTE;'.format(username["username"])
            count = self.db.query(sql).fetchone()
            if count['count(*)'] > 4:
                return 'Your request quota exhausted, Please try after sometime', 403
            sql = 'insert into login_data (username , created) values ("{}", NOW())'.format(username['username'])
            id = self.db.transact(sql)
            sql = 'delete from login_data where created < NOW() - INTERVAL 2 MINUTE;'
            self.db.transact(sql)
            response = requests.get('http://localhost:8000/get_number')
            result = response.json()
            return result, 200
            # return id, 200
        except Exception as err:
            print(err)
            return {"error": "Internal Server error"}, 500
