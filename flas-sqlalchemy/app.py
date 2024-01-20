from flask import Flask

from flask_restful import Api
from flask_jwt_extended import JWTManager


from resources.user import UserRegister

from resources.item import ItemList, Item

from resources.auth import Authentication

app = Flask(__name__)
app.secret_key = "sam"

# turns of the Flask-SQLAlchemy tracker
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)
jwt = JWTManager(app)


api.add_resource(Authentication, "/auth")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    # to avoid circular imports
    from db import db

    db.init_app(app)

    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
