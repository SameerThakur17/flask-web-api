from flask import Flask, request, jsonify

from flask_restful import Api, Resource

from flask_jwt_extended import (
    create_access_token,
    JWTManager,
)

from security import authenticate

from user import UserRegister

from item import ItemList, Item

app = Flask(__name__)
app.secret_key = "sam"
api = Api(app)
jwt = JWTManager(app)


class Authentication(Resource):
    def post(self):
        data = request.get_json()
        user = authenticate(data["username"], data["password"])
        if not user:
            return {"message": "invalid credentials"}
        access_token = create_access_token(identity=data["username"])
        return jsonify(access_token=access_token)


api.add_resource(Authentication, "/auth")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
