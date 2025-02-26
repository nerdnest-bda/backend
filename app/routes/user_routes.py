from flask import Blueprint, jsonify, request
import uuid


from app.models.user import User
from app.services.user_service import get_user, create_user
from app.schemas.user import UserCreate
from uuid import uuid4

import logging

from flask_cors import CORS, cross_origin





user_bp = Blueprint("users", __name__)


@user_bp.route("/<user_id>", methods=["GET"])
@cross_origin()
def get_users_by_id(user_id):
    user = get_user(user_id)
    if not user:
        return jsonify({"User not found": "User not found"}), 404
    return jsonify(user.dict()), 200

@user_bp.route("", methods=["POST", "OPTIONS"])
@cross_origin()
def create_user_route():

    try:
        user_data = UserCreate(**request.json)
        if create_user(user_data):
            return jsonify({"full_name": user_data.full_name}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while creating the user: {}".format(str(e))}), 500






