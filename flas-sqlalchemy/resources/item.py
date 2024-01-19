import sqlite3

from flask_restful import reqparse, Resource

from flask_jwt_extended import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field is required"
    )

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)

        if item:
            return item
        else:
            return {"message": "item not found"}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        sql_query = "SELECT * FROM items WHERE name=?"

        result = cursor.execute(sql_query, (name,))
        row = result.fetchone()

        connection.close()
        if row:
            return {"item": {"name": row[0], "price": row[1]}}, 200

    def post(self, name):
        if Item.find_by_name(name):
            return ({"message": f"An item with name {name} already exists"}, 400)

        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}
        try:
            Item.insert(item)
        except:
            return {"message": "An error occured while inserting the item."}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        sql_query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(sql_query, (item["name"], item["price"]))

        connection.commit()
        connection.close()

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
        item = Item.find_by_name(name)
        updated_item = {"name": name, "price": data["price"]}
        if item:
            try:
                Item.update(updated_item)
            except:
                return {"message": "An error occured  while updating the item"}, 500
        else:
            try:
                Item.insert(updated_item)
            except:
                return {"message": "An error occured  while inserting the item"}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        sql_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(sql_query, (item["price"], item["name"]))
        connection.commit()
        connection.close()


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
        return {"items": items}
