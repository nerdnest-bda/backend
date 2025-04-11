from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin

from app.services.news_service import get_news

news_bp = Blueprint("news", __name__)

@news_bp.route("/<university_id>", methods=["GET"])
@cross_origin()
def get_news_for_university(university_id):
    try:
        print("University Id", university_id)
        flag, news_data = get_news(university_id)  
        if flag:
            return jsonify(news_data), 200
        else:
            print(f"Error in fetching news {news_data}")
            return jsonify({"message": f"Error in fetching news "}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching news: {}".format(str(e))}), 500