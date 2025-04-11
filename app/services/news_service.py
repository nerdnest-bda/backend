from flask import current_app
from bson import Binary, ObjectId
from pymongo.errors import DuplicateKeyError
from pymongo import UpdateOne

def get_news(university_id):
    try:
        db = current_app.db
        news_collection = db[current_app.config["NEWS_COLLECTION"]]
        news = list(news_collection.find({"_id": university_id}, {"_id": 1, "news": 1}))
        
        return True, news
    except Exception as e:
        return False, str(e)  