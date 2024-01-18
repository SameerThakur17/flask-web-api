from user import User

# users = [{"id": 1, "usename": "rahul", "password": "champindeed"}]

# username_mapping = {{"rahul": {"id": 1, "usename": "rahul", "password": "champindeed"}}}
# userid_mapping = {{1: {"id": 1, "usename": "rahul", "password": "champindeed"}}}

users = [User(1, "rahul", "champindeed")]
username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user
