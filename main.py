# Logging
import logging

# CORS
from flask_cors import CORS

# Configuration
from config import config

# Request
from src.http import HTTP

# API Versions
from src.versions.v1.api import API1

# Models
from src.models.database import Database

# Swagger implementation
from flask_swagger_ui import get_swaggerui_blueprint

api = {}

# HTTP Request
http = HTTP()

##
# Allow Cross Origin
#
CORS(http.flask)

# Database
database = Database(config)

##
# API Versions, new version of
# the API will be added below
#
api['v1'] = API1(database)

##
# Routes for every request
#
http.api(api)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)

http.flask.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

# Handle not found error
@http.flask.errorhandler(404)
# Not Found
def notfound(e):
  return http.response([], 404)



# Handle method not allowed error
@http.flask.errorhandler(405)
# Not Allowed
def notallowed(e):
  return http.response([], 405)



# Run the App
if __name__ == '__main__':
  http.flask.run(debug=True, port=80, host='0.0.0.0')


# Logging
logging.basicConfig(filename='error.log', filemode='w', level=logging.DEBUG)
