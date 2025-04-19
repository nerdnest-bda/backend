from flask import Blueprint

from app.routes.user_routes import user_bp
from app.routes.universities_routes import universities_bp
from app.routes.news_routes import news_bp
from app.routes.health_route import health_bp
from app.routes.college_stat_routes import stats_bp

api_bp = Blueprint("api", __name__)

api_bp.register_blueprint(health_bp, url_prefix="/health")
api_bp.register_blueprint(user_bp, url_prefix="/users")
api_bp.register_blueprint(universities_bp, url_prefix="/universities")
api_bp.register_blueprint(news_bp, url_prefix="/news")
api_bp.register_blueprint(stats_bp, url_prefix="/collegestats")


