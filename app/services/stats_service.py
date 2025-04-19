from flask import current_app, jsonify
from pymongo.errors import DuplicateKeyError
from pymongo import UpdateOne

def insert_batch(data):
    try:
        db = current_app.db
        college_stats_collection = db[current_app.config["COLLEGE_STATS_COLLECTION"]]

        bulk_operations = []

        for stats in data:
            # Copy uni and remove 'quadrant' if present
            stats_insert = stats.copy()

            operation = UpdateOne(
                {"name": stats["name"]},
                {
                    "$setOnInsert": stats_insert,
                },
                upsert=True
            )

            bulk_operations.append(operation)

        if bulk_operations:
            result = college_stats_collection.bulk_write(bulk_operations, ordered=False)
            return True, f"Inserted {result.upserted_count} new records, updated {result.modified_count} existing records."
        else:
            return True, "No data to process."

    except Exception as e:
        return False, str(e)