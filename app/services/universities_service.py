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

def assign_us_quadrant(lat, lon):
    us_center_lat = 39.8
    us_center_lon = -98.6
    if lat > us_center_lat and lon < us_center_lon:
        return "q1"  # Northwest (Top Left)
    elif lat > us_center_lat and lon > us_center_lon:
        return "q2"  # Northeast (Top Right)
    elif lat < us_center_lat and lon < us_center_lon:
        return "q3"  # Southwest (Bottom Left)
    else:
        return "q4"  # Southeast (Bottom Right)

def get_universities(data):
    try:
        db = current_app.db
        quadrant = assign_us_quadrant(data.latitude, data.longitude)
        print(quadrant)
        universities_collection = db[current_app.config["COORDINATES_COLLECTION"]]
        universities = list(universities_collection.find({"quadrant": quadrant}, {"_id": 1, "name": 1, "coordinates": 1}))
        return True, universities
    except Exception as e:
        return False, str(e)