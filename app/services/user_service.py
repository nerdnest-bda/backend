from flask import current_app
from bson import Binary, ObjectId
from pymongo.errors import DuplicateKeyError
from uuid import uuid4

from app.schemas.user import UserInResponse

def get_user(user_id):
    db = current_app.db
    users_collection = db["users"]

    user = users_collection.find_one({"uid": user_id})
    user = UserInResponse(**user)

    if user is None:
        return None
    return user

def create_user(user_data):
    db = current_app.db
    users_collection = db["users"]
    user_data_dict = user_data.dict()
    user_data_dict["_id"] = Binary.from_uuid(uuid4())
    try:
        users_collection.insert_one(user_data_dict)
        return True
    except DuplicateKeyError:
        raise Exception("User already exists")
    except Exception as e:
        raise ValueError("error creating user", e)

