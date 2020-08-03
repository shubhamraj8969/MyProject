from flask import Flask, request, Response
from helpers.DBHelper import DBHelper

TOKEN_KEY = "HTTP_AUTHORIZATION"

def authenticate(func):
    def wrapper(*args, **kwargs):
        if TOKEN_KEY not in request.environ:
            return {"error":"Forbidden! No valid token/domain found!"},403
        else:
            auth = request.environ[TOKEN_KEY]
            db = DBHelper()
            try:
                sql = db.query("select username from user where token=%s", (auth.split(' ')[1],))
                res= sql.fetchone()
                if not res:
                    return {"error":"Forbidden! Try generating new token"},403

            except Exception as e:
                    print("Authenticate:", e.__str__())
                    return {"error": "Authentication Failed"},403
            ret = func(*args, **kwargs)
            return ret
    return wrapper
