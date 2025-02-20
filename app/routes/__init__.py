from flask import Blueprint

from app.routes.user_routes import user_bp

api_bp = Blueprint("api", __name__)

api_bp.register_blueprint(user_bp, url_prefix="/users")

print("ROUTES")

