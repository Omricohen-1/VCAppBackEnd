from flask_restful import Resource
from flask import request


class add_contact(Resource):
    def get(self):
        response = 'You can add contacts :)'
        return response

    def post(self):
        