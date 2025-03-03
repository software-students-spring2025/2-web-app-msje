from bson.objectid import ObjectId
import flask_login

class User(flask_login.UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

# cannot import db -> circular import problem
def load_user(db, user_id):
    user_info = db["users"].find_one({"_id": ObjectId(user_id)})
    if user_info:
        return User(user_info['_id'], user_info['username'], user_info['password'])
    return None

def check_user(db, username, password):
    user_info = db["users"].find_one({"username": username})

    if user_info['password'] == password and user_info:
        return User(user_info['_id'], user_info['username'], user_info['password'])
    return None
