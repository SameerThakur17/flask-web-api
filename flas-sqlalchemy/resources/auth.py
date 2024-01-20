from flask_jwt_extended import create_access_token

from security import authenticate

from flask_restful import Resource
from flask import request, jsonify


class Authentication(Resource):
    def post(self):
        data = request.get_json()
        user = authenticate(data["username"], data["password"])
        if not user:
            return {"message": "invalid credentials"}
        access_token = create_access_token(identity=data["username"])
        return jsonify(access_token=access_token)
