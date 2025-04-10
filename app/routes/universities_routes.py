from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin
from uuid import uuid4

from app.schemas.universities import UniversityBatchRequest, Coordinates
from app.services.universities_service import insert_batch, get_universities, get_universities_via_id




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

@universities_bp.route("/coordinates", methods=["GET"])
@cross_origin()
def get_universities_by_coordinates():
    try:
        data = Coordinates(**request.args.to_dict())
        flag, universities = get_universities(data)
        if flag:
            return jsonify([university for university in universities]), 200
        return jsonify({"message": "Error in fetching"}), 404
        
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching universities: {}".format(str(e))}), 500

@universities_bp.route("/<id>", methods=["GET"])
@cross_origin()
def get_universities_by_id(id):
    try:
        flag, university = get_universities_via_id(id)
        if flag:
            return jsonify(university), 200
        return jsonify({"message": "Error in fetching"}), 404
        
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching universities: {}".format(str(e))}), 500
