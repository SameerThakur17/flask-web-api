from flask import Flask, request, jsonify

from flask_restful import Api, Resource, reqparse

from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    get_jwt_identity,
    jwt_required,
)

from security import authenticate

app = Flask(__name__)
app.secret_key = "sam"
api = Api(app)
jwt = JWTManager(app)


items = []


class Authentication(Resource):
    def post(self):
        data = request.get_json()
        user = authenticate(data["username"], data["password"])
        if not user:
            return {"message": "invalid credentials"}
        access_token = create_access_token(identity=data["username"])
        return jsonify(access_token=access_token)


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field is required"
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)

        return ({"item": item}, 200 if item else 404)

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return ({"message": f"An item with name {name} already exists"}, 400)

        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {"name": name, "price": data["price"]}
            items.append(item)

        return item


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Authentication, "/auth")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
app.run(port=5000, debug=True)
