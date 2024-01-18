from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [{"name": "My Store", "items": [{"name": "My Item", "price": 10.67}]}]
"""
GET /store
GET /store/<string:name>
GET /store/<string:name>/item

POST /store {name:}
POST /store/<string:name>/item{name:,price:}
"""


# POST /stores {name:}
@app.route("/stores", methods=["POST"])
def create_store():
    # get_json coverts json to a dictionary
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return jsonify(new_store)


# GET /stores
@app.route("/stores")
def get_stores():
    return jsonify({"stores": stores})


# GET /stores/<string:name>
@app.route("/stores/<string:name>")
def get_store(name):
    # iterate over stores
    # if store name matches
    # return the store else error

    for store in stores:
        if store["name"] == name:
            return jsonify(store)

    return jsonify({"Error": "Store Not Found"})


# POST /stores/<string:name>/items
@app.route("/stores/<string:name>/items", methods=["POST"])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return jsonify(new_item)
    return jsonify({"Error": "Store Not Found"})


# GET /stores/<string:name>/items
@app.route("/stores/<string:name>/items")
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items": store["items"]})
    return jsonify({"Error": "Store Not Found"})


app.run(port=5000)
