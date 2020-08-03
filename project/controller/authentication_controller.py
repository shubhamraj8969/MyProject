# Import flask Modules
from flask_restful import Resource
from flask import request
import uuid

# Module for hashing password
import bcrypt as bcrypt

# Current date and time
from datetime import datetime

# Import Database Modules
from helpers.DBHelper import DBHelper
from helpers.authenticate import *

TOKEN_KEY = "HTTP_AUTHORIZATION"

class AuthenticationController(Resource):
    def __init__(self):
        self.db = DBHelper()

    def post(self):
        if request.endpoint == "login_ep":
            data = request.authorization
            return self.log_in(data)

        if request.endpoint == "logout_ep":
            return self.log_out()

        if request.endpoint == "signup_ep":
            req_data = request.get_json(force = True)
            return self.sign_up(req_data)

    def sign_up(self, data = None):
        try:
            if "username" and "password" not in data.keys():
                return { "error": "User name and password cannot be empty" },200
            else : 
                password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
                username = data["username"]
                sql = "insert into user (username, password) VALUES(%s, %s)"
                self.db.transact(sql,(data['username'], password))
                self.db.commit()
                return "Signup Successfull",200
        except Exception as e:
            print("INternal Error Occured, Please retry" + e.__str__())
            return { "error": "Internal Error Occured, Please retry" },500

    def log_in(self, data = None):
        try:
            if "username" and "password" not in data.keys():
                return { "error": "User name and password cannot be empty" },200
            else :
                sql = "select password from user where username = '{}'".format(data["username"])
                res = self.db.query(sql).fetchone()
                if not res:
                    return { "error": "Invalid username, user not found!" },200
                elif bcrypt.checkpw(data["password"].encode("utf8"), res["password"].encode("utf8")):
                    token = uuid.uuid4()
                    sql = "update user set token = '{}' where username = '{}'".format(str(token), data["username"])
                    id = self.db.transact(sql)
                    self.db.commit()
                    sql = "select token from user where username = '{}'".format(data['username'])
                    token = self.db.query(sql).fetchone()
                    return token,200
                else:
                    return { "error": "Password Not matched" },200
        except Exception as e:
            print("AuthenticationController: log_in: " + e.__str__())
            return { "error": "Failed to complete authentication" },403

    @authenticate
    def log_out(self):
        try:
            if TOKEN_KEY not in request.environ:
                return { "error": "Invalid user" },200
            else:
                sql = "update user set token = '' where token = '{}'".format(request.environ[TOKEN_KEY].split(' ')[1])
                self.db.transact(sql)
                self.db.commit()
                return {"status": "Logged out successfully"}, 200
        except Exception as e:
            print("AuthenticationController: log_out :" + e.__str__())
            return {"error": "User not logged out"}, 200
