from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin
from uuid import uuid4

from app.schemas.universities import UniversityBatchRequest
from app.services.universities_service import insert_batch




universities_bp = Blueprint("universities", __name__)

@universities_bp.route("/insert_universities", methods=["POST"])
@cross_origin()
def inject_universities():
    try:
        body = UniversityBatchRequest(**request.json)
        data = []
        for university in body.universities:
            university_dict = university.dict()
            if '_id' not in university_dict:
                university_dict["_id"] = str(uuid4())
            data.append(university_dict)
        flag, msg = insert_batch(data)
        if flag:
            return jsonify({"message": f"Successfully inserted: {msg}"}), 201
        else:
            return jsonify({"error": f"Failed to inject data {msg}"}), 500
    except Exception as e:
        return jsonify({"error": "An error occurred while injecting user: {}".format(str(e))}), 500
