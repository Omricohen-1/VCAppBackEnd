from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS, cross_origin
from add_contact_api import add_contact
from social.linkedin import linkedin_instance as li
 
application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

api = Api(application)

api.add_resource(add_contact, "/add-contacts")


@application.route("/search_linkedin", methods=['GET'])
def search_linkedin():
    """
    Function excpects GET request with q='{str}' arg
    """
    search_string = request.args.get('q')
    #TODO change to get email and pass
    return li.test_instance().get_users_by_search(search_string)


@application.route("/status")
def status():
    return "ok"


if __name__ == "__main__":
    application.run(port=8080, debug=True)
