from flask import Flask

from flask_restful import Api, Resource

from flask_jwt_extended import (
    create_access_token,
    JWTManager,
)


from resources.user import UserRegister

from resources.item import ItemList, Item

from resources.auth import Authentication

app = Flask(__name__)
app.secret_key = "sam"
api = Api(app)
jwt = JWTManager(app)


api.add_resource(Authentication, "/auth")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
