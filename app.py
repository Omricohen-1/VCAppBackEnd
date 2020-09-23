from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS, cross_origin
from add_contact_api import add_contact
from social.linkedin import linkedin_instance as li
from social.facebook import facebook
# from elasticsearch import Elasticsearch
from linkedin import li_auth, li_search, li_launch_auth
from dynaconf import settings

application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

api = Api(application)

api.add_resource(add_contact, "/add-contacts")
# elastic = Elasticsearch(['https://search-omri-elflj5ij34pitprcoersng2dfm.eu-central-1.es.amazonaws.com:443'],
#                         http_auth=('vcapp_test', 'CliqueHub1!'))

# linkedin paths
api.add_resource(li_auth, '/linkedin/auth')
api.add_resource(li_search, '/linkedin/search')
api.add_resource(li_launch_auth, '/linkedin/launch_auth')


@application.route("/facebook/search", methods=['GET'])
def search_facebook():
    """
    Function excpects GET request with:
    q='{str}' arg
    email='{str}'
    password='{str}'
    """
    # TODO change to oauth2
    search_string = request.args.get('q')
    email = request.args.get('email')
    password = request.args.get('password')
    return facebook.get_users_by_search(email, password, search_string)


@application.route("/add_contact", methods=['POST'])
def add_contact_to_db():
    # TODO fix connection with the new elastic
    pass
    # contact = request.get_json()
    # elastic.index(index='eitan-cl', body=contact)


@application.route("/status")
def status():
    return "ok"


if __name__ == "__main__":
    application.run(port=8080, debug=True)
