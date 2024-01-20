import sqlite3

from flask_restful import reqparse, Resource

from flask_jwt_extended import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field is required"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json(), 200
        else:
            return {"message": "item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return ({"message": f"An item with name {name} already exists"}, 400)

        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"])
        try:
            item.insert()
        except:
            return {"message": "An error occured while inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        sql_query = "DELETE FROM items WHERE name=?"
        cursor.execute(sql_query, (name,))
        connection.commit()
        connection.close()

        return {"message": "item deleted"}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data["price"])
        if item:
            try:
                updated_item.update()
            except:
                return {"message": "An error occured  while updating the item"}, 500
        else:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occured  while inserting the item"}, 500
        return updated_item.json(), 200


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        sql_query = "SELECT * FROM items"
        result = cursor.execute(sql_query)
        items = []
        for row in result:
            items.append({"name": row[0], "price": row[1]})

        connection.close()
        return {"items": items}, 200
