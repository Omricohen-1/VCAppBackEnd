from flask_restful import Resource
from flask import request


class add_contact(Resource):
    def get(self):
        response = 'You can add contacts :)'
        return response

    def post(self):
        data = request.json()

        #TODO upload the data to the server
        #TODO should we do validaition here?
        #TODO manage responses from writing to DB
        
        return data
