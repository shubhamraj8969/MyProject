# Import System modules
import sys, getopt

# Import flask Packages
from flask import Flask, render_template
from flask_restful import Api

#Import Utility Functions and Configurations
from util.config import API_PATH, API_CONF


# Import Controller modules
from controller.health import Health
from controller.authentication_controller import AuthenticationController
from controller.api_controller import APIController
# Flask application
app = Flask(__name__, template_folder="View")

# REST API definition
api = Api(app)

api.add_resource(
	Health,
	API_PATH + "/health/",
	endpoint = "health")

api.add_resource(
    AuthenticationController,
    API_PATH + "/login/",
	endpoint = "login_ep")

api.add_resource(
	AuthenticationController,
	API_PATH + "/logout/",
	endpoint = "logout_ep")

api.add_resource(
	AuthenticationController,
	API_PATH + "/signup/",
	endpoint = "signup_ep")

api.add_resource(
    APIController,
    API_PATH + "/call_api/",
    endpoint = "call_api"
    )

api.add_resource(
    APIController,
    API_PATH + "/see_remaining_limits/",
    endpoint = "see_remaining_limits"
    )

hostEnv   = API_CONF["host"]
portEnv   = API_CONF["port"]
debugFlag = False

# Driver Program
if __name__ == "__main__":
	# Start Application
	app.run(debug = debugFlag, host = hostEnv, port = portEnv, threaded = True)
