from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from backend_app.models.user import User
from backend_app.models.file_upload_model import FileUpload
from backend_app.models.malware_scan import MalwareScan  # ✅ FIXED
from backend_app.models.security_alert import SecurityAlert  # ✅ Added this line
from backend_app.models.system_log import SystemLog  # ✅ Added this line
from backend_app.models.transaction import Transaction  # ✅ Add this line

