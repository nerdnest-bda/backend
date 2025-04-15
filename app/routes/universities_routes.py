from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin
from uuid import uuid4

from app.schemas.universities import UniversityBatchRequest, Coordinates
from app.services.universities_service import insert_batch, get_universities, get_universities_via_id, get_about, get_logo, get_university_id_with_name




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
    
@universities_bp.route("/get_university_id", methods = ["GET"])
def get_university_id():
    university_name = request.args.get("university_name", "")
    if not university_name:
        return jsonify({"error": "College name is required"}), 400
    try:
        flag, results = get_university_id_with_name(university_name)
        if flag:
            if results == {}:
                jsonify({}), 404
            else:
                return jsonify(results), 200
        else:
            jsonify({"message": "An error occured while fetching universities: {}".format(str(e))}), 500
            
    except Exception as e:
        return jsonify({"message": "An error occured while fetching universities: {}".format(str(e))}), 500

    



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
    
@universities_bp.route("/about", methods=["GET"])
@cross_origin()
def get_about_details():
    try:
        university_name = request.args.get("university_name")
        if university_name == "":
            return {
                "message": "university name cannot be an empty string"
            }, 400
        flag, about_university = get_about(university_name)

        if not flag:
            if not about_university:
                return {
                    "message": "could not find data on the web"
                }, 404
            return {
                "message": "could not retrieve university details"
            }, 500
        return {
            "college": university_name,
            "about_college": about_university
        }, 200
    except Exception as e:
        return {
            "message": "something went wrong on the server",
            "error": str(e)
        }, 500
    

@universities_bp.route("/logo", methods=["GET"])
@cross_origin()
def get_logo_url():
    try:
        university_name = request.args.get("university_name")
        if university_name == "":
            return {
                "message": "university name cannot be an empty string"
            }, 400
        flag, logo_url = get_logo(university_name)

        if not flag:
            if not logo_url:
                return {
                    "message": "could not find data on the web"
                }, 404
            return {
                "message": "could not retrieve university details"
            }, 500
        return {
            "college": university_name,
            "logo_url": logo_url
        }, 200
    except Exception as e:
        return {
            "message": "something went wrong on the server",
            "error": str(e)
        }, 500

