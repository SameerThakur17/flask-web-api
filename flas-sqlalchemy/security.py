from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


def identity(_id):
    return UserModel.find_by_id(_id)
