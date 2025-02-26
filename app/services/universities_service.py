from flask import current_app
from bson import Binary, ObjectId
from pymongo.errors import DuplicateKeyError
from uuid import uuid4


def insert_batch(data):
    try:
        db = current_app.db
        universities_collection = db["universities"]
        inserted_ids = []
        for university in data:
            existing_university = universities_collection.find_one({
                "name": university["name"], 
                "coordinates": university["coordinates"]
            })

            if existing_university:
                continue 
            else:
                result = universities_collection.insert_one(university)
                inserted_ids.append(str(result.inserted_id))
        return True, f" {inserted_ids}"
    
    except Exception as e:
        return False, str(e)