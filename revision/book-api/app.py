from flask import Flask, jsonify, request

app = Flask(__name__)

books = [{"name": "The Alchemist", "price": "100"}]


@app.route("/books")
def get_all_books():
    return jsonify(books), 200


@app.route("/book/<name>")
def get_book_by_name(name):
    book = next(filter(lambda x: x["name"] == name, books), None)
    print(book)
    if book:
        return jsonify(book), 200
    else:
        return jsonify({"message": "Not Found"}), 400


@app.route("/book/<name>", methods=["POST"])
def create_book_by_name(name):
    if next(filter(lambda x: x["name"] == name, books), None):
        return {"message": f"A book with the name {name} already exists"}, 400
    else:
        data = request.get_json()
        book = {"name": name, "price": data["price"]}
        books.append(book)
        return book, 201


@app.route("/book/<name>", methods=["DELETE"])
def delete_book_by_name(name):
    global books
    if not next(filter(lambda x: x["name"] == name, books), None):
        return {"message": f"A book with the name {name} doesn't exists"}, 400
    else:
        books = next(filter(lambda x: x["name"] != name, books), None)
        return jsonify({"message": "book deleted succesfully"}), 200


@app.route("/book/<name>", methods=["PUT"])
def update_book_by_name(name):
    data = request.get_json()
    book = next(filter(lambda x: x["name"] == name, books), None)
    if book:
        book.update({"name": name, "price": data["price"]})
        return jsonify(book)

    else:
        new_book = {"name": name, "price": data["price"]}
        books.append(new_book)
        return jsonify(new_book)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
