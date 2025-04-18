from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from backend_app.config import Config

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)  # Enable CORS for frontend communication
    db.init_app(app)

    with app.app_context():
        from backend_app.models import user  # ✅ Import all models
        db.create_all()  # ✅ Ensure tables are created

    # ✅ Register Blueprints
    from backend_app.routes import main_routes
    app.register_blueprint(main_routes)  # Root route

    from backend_app.routes.auth_routes import auth_routes
    app.register_blueprint(auth_routes, url_prefix="/auth")

    from backend_app.routes.file_upload_routes import file_upload_routes
    app.register_blueprint(file_upload_routes, url_prefix="/files")

    from backend_app.routes.malware_scan_routes import malware_scan_routes
    app.register_blueprint(malware_scan_routes, url_prefix="/scan")

    from backend_app.routes.security_routes import security_routes
    app.register_blueprint(security_routes, url_prefix="/security")

    from backend_app.routes.system_log_routes import system_log_routes
    app.register_blueprint(system_log_routes, url_prefix="/logs")

    from backend_app.routes.transaction_routes import transaction_routes
    app.register_blueprint(transaction_routes, url_prefix="/transactions")

    from backend_app.routes.user_routes import user_routes
    app.register_blueprint(user_routes, url_prefix="/users")

    return app
