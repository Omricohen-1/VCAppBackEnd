from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin


application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'


api = Api(application)



@application.route("/status")
def status():
    return "ok"


if __name__ == "__main__":
    application.run(port=8080, debug=True)
