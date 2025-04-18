from flask import Blueprint, request, jsonify
from backend_app.models import db
from backend_app.models.file_upload_model import FileUpload
from backend_app.models.malware_scan import MalwareScan
import os
import docker
import time
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

file_upload_routes = Blueprint("file_upload_routes", __name__)

def check_docker_environment():
    """Check if Docker is running and the pestudio image is available"""
    try:
        client = docker.from_env()
        client.ping()  # Check if Docker daemon is running
        try:
            client.images.get("pestudio")
            return True, "Docker and pestudio image are ready"
        except docker.errors.ImageNotFound:
            return False, "pestudio image not found"
    except Exception as e:
        return False, f"Docker error: {str(e)}"

@file_upload_routes.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    user_type = request.form.get('userType', 'customer')
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
         print("Step 1: File received")
         file.save(os.path.join(UPLOAD_FOLDER, filename))
         print("Step 2: File saved")

    # Check Docker environment first
    docker_ready, docker_message = check_docker_environment()
    if not docker_ready:
        logger.error(f"Docker environment not ready: {docker_message}")
        return jsonify({"error": f"Docker environment not ready: {docker_message}"}), 500
            #Send to Docker/PEstudio static malware scanner
             result = run_static_analysis(file_path)
             print("Step 3: Analysis result =", result)
    # Create uploads directory if it doesn't exist
    upload_folder = os.path.join(os.getcwd(), 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Save file to local directory for analysis
    filepath = os.path.join(upload_folder, file.filename)
    try:
        file.save(filepath)
        logger.info(f"File saved successfully: {filepath}")
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        return jsonify({"error": f"Error saving file: {str(e)}"}), 500

    try:
        # Analyze file using Docker container with PEstudio
        client = docker.from_env()
        
        # Run PEstudio in a container
        logger.info(f"Starting PEstudio analysis for file: {file.filename}")
        container = client.containers.run(
            "pestudio",
            f"scan_file.sh {file.filename}",
            volumes={upload_folder: {'bind': '/app/uploads', 'mode': 'rw'}},
            detach=True
        )
        
        # Wait for the container to finish with timeout
        try:
            container.wait(timeout=60)  # 60 seconds timeout
            logs = container.logs().decode('utf-8')
            logger.info(f"PEstudio analysis completed. Logs: {logs[:200]}...")  # Log first 200 chars
        except Exception as e:
            logger.error(f"Error waiting for container: {str(e)}")
            container.stop()
            container.remove()
            return jsonify({"error": "Analysis timed out or failed"}), 500
        finally:
            container.remove()
        
        # Determine if file is malicious based on PEstudio output
        is_malicious = "malicious" in logs.lower()
        scan_status = "Malicious" if is_malicious else "Safe"
        logger.info(f"Scan result for {file.filename}: {scan_status}")
        
        # For customer users, store the file if it's safe
        if user_type == 'customer' and scan_status == "Safe":
            file_upload = FileUpload(
                filename=file.filename,
                file_type=file.content_type,
                file_size=os.path.getsize(filepath),
                uploaded_by=request.form.get('user_email', 'anonymous'),
                storage_path=filepath,
                is_analyzed=True,
                analysis_result=scan_status
            )
            db.session.add(file_upload)
            logger.info(f"File stored in database for customer: {file.filename}")
        
        # Save scan result to database
        malware_scan = MalwareScan(
            filename=file.filename,
            file_size=os.path.getsize(filepath),
            file_type=file.content_type,
            scan_result=scan_status,
            scan_details=logs,
            analysis_time=time.time()
        )
        db.session.add(malware_scan)
        db.session.commit()
        logger.info(f"Scan result stored in database: {file.filename}")
        
        # Clean up the uploaded file if it's malicious or if user is admin/security
        if scan_status == "Malicious" or user_type in ['admin', 'security']:
            try:
                os.remove(filepath)
                logger.info(f"File cleaned up: {filepath}")
            except Exception as e:
                logger.error(f"Error cleaning up file: {str(e)}")
        
        return jsonify({
            "message": "File uploaded and analyzed successfully",
            "scan_result": scan_status,
            "can_run_script": scan_status == "Safe" and user_type in ['admin', 'security']
        }), 200
        
    except Exception as e:
        logger.error(f"Error in file upload process: {str(e)}")
        # Clean up the file in case of error
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                logger.info(f"File cleaned up after error: {filepath}")
            except Exception as cleanup_error:
                logger.error(f"Error cleaning up file after error: {str(cleanup_error)}")
        return jsonify({"error": f"Error analyzing file: {str(e)}"}), 500

@file_upload_routes.route("/run-script", methods=["POST"])
def run_script():
    data = request.get_json()
    filename = data.get('filename')
    user_type = data.get('userType')
    
    if not filename or user_type not in ['admin', 'security']:
        return jsonify({"error": "Invalid request"}), 400
    
    try:
        # Get the scan result from database
        scan = MalwareScan.query.filter_by(filename=filename).order_by(MalwareScan.scanned_at.desc()).first()
        
        if not scan or scan.scan_result != "Safe":
            return jsonify({"error": "File not found or not safe to run"}), 400
        
        # Run the script in a secure container
        client = docker.from_env()
        container = client.containers.run(
            "script-runner",  # Your script runner Docker image
            f"run_script.sh {filename}",
            volumes={'/app/scripts': {'bind': '/app/scripts', 'mode': 'ro'}},
            detach=True
        )
        
        container.wait()
        logs = container.logs().decode('utf-8')
        container.remove()
        
        return jsonify({
            "message": "Script executed successfully",
            "logs": logs
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Error running script: {str(e)}"}), 500
