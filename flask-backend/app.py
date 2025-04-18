from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import os
import subprocess
import mysql.connector
from mysql.connector import Error
import docker
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)
# Set up the upload folder path
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def create_db_connection():
    attempts = 0
    while attempts < 3:  # Retry a few times
        try:
            connection = mysql.connector.connect(
                host="localhost",     # e.g., "localhost" or your MySQL server IP
                user="root",     # MySQL username
                password="Roy.12345,",  # MySQL password
                database="secure_banking_db",  # The database you created
                port="3306"
            )
            if connection.is_connected():
                print("Connected to MySQL database")
            return connection
            break
        except Error as e:
            print(f"Error: {str(e)}")
            attempts += 1
            time.sleep(5)  # Retry after 5 seconds
    return None



@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    conn = create_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed", "status": "error"}), 500

    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and user[3] == password:  # Password check at index 3
        return jsonify({"message": "Login successful!", "status": "success", "role": user[4], "redirect": f"/{user[4]}-dashboard"}), 200
    else:
        return jsonify({"message": "Invalid credentials!", "status": "error"}), 401


# Route redirects to Vue frontend pages

@app.route('/')
def landing_page():
    return redirect("http://localhost:8080")

@app.route('/CustomerLogin')
def customer_login():
    return redirect("http://localhost:8080/CustomerLogin")

@app.route('/AdminLogin')
def admin_login():
    return redirect("http://localhost:8080/AdminLogin")

@app.route('/SecurityLogin')
def security_login():
    return redirect("http://localhost:8080/SecurityLogin")

@app.route('/AddUser')
def add_user():
    return redirect("http://localhost:8080/AddUser")

@app.route('/AdminDashboard')
def admin_dashboard():
    return redirect("http://localhost:8080/AdminDashboard")

@app.route('/ChangePassword')
def change_password():
    return redirect("http://localhost:8080/ChangePassword")

@app.route('/CustomerDashboard')
def customer_dashboard():
    return redirect("http://localhost:8080/CustomerDashboard")

@app.route('/DeleteUser')
def delete_user():
    return redirect("http://localhost:8080/DeleteUser")

@app.route('/EnableMFA')
def enable_mfa():
    return redirect("http://localhost:8080/EnableMFA")

@app.route('/LoginHistory')
def login_history():
    return redirect("http://localhost:8080/LoginHistory")

@app.route('/SecurityDashboard')
def security_dashboard():
    return redirect("http://localhost:8080/SecurityDashboard")

@app.route('/SystemLogs')
def system_logs():
    return redirect("http://localhost:8080/SystemLogs")

@app.route('/UserLogin')
def user_login():
    return redirect("http://localhost:8080/UserLogin")

@app.route('/UserNotifications')
def user_notifications():
    return redirect("http://localhost:8080/UserNotifications")

@app.route('/UserRegister')
def user_register():
    return redirect("http://localhost:8080/UserRegister")


# File upload route
@app.route('/files/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    user_type = request.form.get('userType', 'customer')  # Get user type from form
    user_email = request.form.get('user_email', 'anonymous')
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Save and analyze file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(filepath)
        
        # Analyze file for malware
        analysis_result = analyze_file_in_docker(filepath)
        scan_status = "malicious" if "malicious" in str(analysis_result).lower() else "safe"
        
        # Store in database
        conn = create_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        try:
            cursor = conn.cursor()
            
            # Insert file upload record with explicit user_type
            upload_query = """
                INSERT INTO file_uploads 
                (email, file_name, file_type, status, user_type, created_at) 
                VALUES (%s, %s, %s, %s, %s, NOW())
            """
            file_type = os.path.splitext(file.filename)[1][1:] or 'unknown'
            
            print(f"Inserting file upload - Email: {user_email}, Type: {user_type}")  # Debug log
            
            cursor.execute(upload_query, (
                user_email,
                file.filename,
                file_type,
                scan_status,
                user_type
            ))
            file_id = cursor.lastrowid
            
            # Insert scan result
            scan_query = """
                INSERT INTO malware_scan_results 
                (file_id, scan_report, scan_status, created_at) 
                VALUES (%s, %s, %s, NOW())
            """
            scan_report = f"File analyzed. Result: {str(analysis_result)[:500]}"
            cursor.execute(scan_query, (file_id, scan_report, scan_status))
            
            conn.commit()
            
            print(f"Successfully stored file upload and scan result for ID: {file_id}")  # Debug log
            
            return jsonify({
                'message': 'File uploaded and analyzed successfully',
                'scan_result': scan_status,
                'file_id': file_id,
                'scan_report': scan_report,
                'user_type': user_type  # Return user type for verification
            }), 200
            
        except Exception as e:
            print(f"Database error: {str(e)}")
            conn.rollback()
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500

@app.route('/files/run-script', methods=['POST'])
def run_script():
    data = request.json
    filename = data.get('filename')
    user_type = data.get('userType')
    
    if not filename or user_type not in ['admin', 'security']:
        return jsonify({"error": "Invalid request"}), 400
    
    try:
        # Get the latest scan result from database
        conn = create_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
            
        cursor = conn.cursor()
        query = "SELECT scan_result FROM file_uploads WHERE filename = %s ORDER BY upload_date DESC LIMIT 1"
        cursor.execute(query, (filename,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not result or result[0] != "Safe":
            return jsonify({"error": "File not found or not safe to run"}), 400
        
        # Run the script in a secure container
        client = docker.from_env()
        container = client.containers.run(
            "script-runner",
            f"python /scripts/{filename}",
            volumes={
                os.path.join(UPLOAD_FOLDER): {'bind': '/scripts', 'mode': 'ro'}
            },
            remove=True
        )
        
        return jsonify({
            "message": "Script executed successfully",
            "logs": container.decode('utf-8')
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Error running script: {str(e)}"}), 500

@app.route('/api/malware-reports', methods=['GET'])
def get_malware_reports():
    return jsonify({"message": "Malware reports will be here"}), 200

@app.route('/api/file-uploads', methods=['GET'])
def get_file_uploads():
    conn = create_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Modified query to get ALL uploads regardless of user type
        query = """
            SELECT 
                f.id,
                f.email,
                f.file_name,
                f.file_type,
                f.status,
                f.user_type,
                DATE_FORMAT(f.created_at, '%Y-%m-%d %H:%i:%s') as created_at,
                m.scan_report,
                m.scan_status,
                DATE_FORMAT(m.created_at, '%Y-%m-%d %H:%i:%s') as scanned_at
            FROM file_uploads f
            LEFT JOIN malware_scan_results m ON f.id = m.file_id
            ORDER BY f.created_at DESC
        """
        
        print("Executing file uploads query")  # Debug log
        
        cursor.execute(query)
        files = cursor.fetchall()
        
        print(f"Found {len(files)} file uploads")  # Debug log
        
        return jsonify({"files": files}), 200
    except Exception as e:
        print(f"Database error in get_file_uploads: {str(e)}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/file-report/<int:file_id>', methods=['GET'])
def get_file_report(file_id):
    conn = create_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                f.file_name,
                f.file_type,
                f.status,
                f.created_at,
                m.scan_report,
                m.scan_status
            FROM file_uploads f
            LEFT JOIN malware_scan_results m ON f.account_number = m.file_id
            WHERE f.account_number = %s
        """
        cursor.execute(query, (file_id,))
        report = cursor.fetchone()
        
        if report:
            return jsonify({
                "success": True,
                "report": report
            }), 200
        else:
            return jsonify({"error": "Report not found"}), 404
            
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

def analyze_file(filepath):
    try:
        # Run PEstudio inside Docker
        result = subprocess.run(
            ["docker", "exec", "your_pestudio_container", "pestudio", filepath],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return None

    
# Save file to the database
def save_file_to_db(filename, user_email, scan_result):
    conn = create_db_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO file_uploads (email, filename, scan_result) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_email, filename, scan_result))
        conn.commit()
        cursor.close()
        conn.close()

# Analyze file using Docker (PEstudio inside Docker container)
def analyze_file_in_docker(file_path):
    client = docker.from_env()
    try:
        # Run PEstudio container and scan the file
        container = client.containers.run(
            "pestudio-container",  # Ensure you have this image built and running
            f"wine /app/pestudio.exe {file_path}",
            remove=True
        )
        return container.logs().decode("utf-8")
    except Exception as e:
        return str(e)

def verify_database_tables():
    conn = create_db_connection()
    if not conn:
        print("Failed to connect to database")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Check if tables exist and create them if they don't
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_uploads (
                account_number INT AUTO_INCREMENT,
                email VARCHAR(255) NOT NULL,
                file_name VARCHAR(255) NOT NULL,
                file_type VARCHAR(20) NOT NULL,
                status VARCHAR(45) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (account_number)
            ) ENGINE=InnoDB;
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS malware_scan_results (
                id INT AUTO_INCREMENT,
                file_id INT NOT NULL,
                scan_report TEXT NOT NULL,
                scan_status ENUM('safe', 'malicious') NOT NULL,
                scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id),
                FOREIGN KEY (file_id) REFERENCES file_uploads(account_number)
            ) ENGINE=InnoDB;
        """)
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error verifying database tables: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    verify_database_tables()  # Verify tables exist before starting the app
    app.run(debug=True, host='127.0.0.1', port=5000)

