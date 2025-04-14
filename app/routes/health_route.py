from flask import Blueprint, jsonify, request

health_bp = Blueprint("health", __name__)

@health_bp.route("/", methods=["GET"])
def get_health():
    return {
        "message": "API is healthy"
    }, 200