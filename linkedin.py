from flask_restful import Resource
from flask import request
from social.linkedin_oauth2 import get_access_token
from social.linkedin_oauth2.auth import main as auth
from social.linkedin import linkedin_instance as li

class li_launch_auth(Resource):
    def get(self):
        auth()
        
class li_auth(Resource):
    def get(self):
        if 'code' in request.args:
            code = request.args.get('code')
            #TODO compare the state to ensure security
            state = request.args.get('state')
            get_access_token.main(code)
            return "got code processing... redirect in less then 5 sec"
        else :
            return "Ok"
           

class li_search(Resource):
    def search_linkedin(self):
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
        return li.LinkedinInstance(email, password).get_users_by_search(search_string)


