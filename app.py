from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS, cross_origin
from add_contact_api import add_contact
from linkedin import li_auth, li_search, li_launch_auth

from dynaconf import settings


application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

api = Api(application)

api.add_resource(add_contact, "/add-contacts")

#linkedin paths
api.add_resource(li_auth, '/linkedin/auth')
api.add_resource(li_search, '/linkedin/search')
api.add_resource(li_launch_auth, '/linkedin/launch_auth')


@application.route("/status")
def status():
    return "ok"


if __name__ == "__main__":
    application.run(port=8080, debug=True)
