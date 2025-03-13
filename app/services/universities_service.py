from flask import current_app
from bson import Binary, ObjectId
from pymongo.errors import DuplicateKeyError
from pymongo import UpdateOne
from uuid import uuid4


def insert_batch(data):
    try:
        db = current_app.db
        universities_collection = db[current_app.config["COORDINATES_COLLECTION"]]

        bulk_operations = [
            UpdateOne(
                {"name": uni["name"], "coordinates": uni["coordinates"]},
                {"$setOnInsert": uni},
                upsert=True
            )
            for uni in data
        ]

        if bulk_operations:
            result = universities_collection.bulk_write(bulk_operations, ordered=False)
            return True, f"Inserted {result.upserted_count} new records, updated {result.modified_count} existing records."
        else:
            return True, "No data to process."

    except Exception as e:
        return False, str(e)