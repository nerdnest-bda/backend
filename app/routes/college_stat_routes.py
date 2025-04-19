from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin
from uuid import uuid4

from app.schemas.stats import StatsBatchRequest

from app.services.stats_service import insert_batch




stats_bp = Blueprint("collegestats", __name__)

@stats_bp.route("/insert_stats", methods=["POST"])
@cross_origin()
def inject_college_stats():
    try:
        print("REQUEST RECEIVED")
        body = StatsBatchRequest(**request.json)
        print("BODY:",body.stats[0].dict())
        data = []
        for stats in body.stats:
            stats_dict = stats.dict()
            if '_id' not in stats_dict:
                stats_dict["_id"] = str(uuid4())        # Needs to get similar university id
            data.append(stats_dict)
        flag, msg = insert_batch(data)
        if flag:
            return jsonify({"message": f"Successfully inserted: {msg}"}), 201
        else:
            return jsonify({"error": f"Failed to inject data {msg}"}), 500
    except Exception as e:
        return jsonify({"error": "An error occurred while injecting stats: {}".format(str(e))}), 500