import unittest
import os
import json
import time
from flask import Flask
from backend_app.routes.file_upload_routes import file_upload_routes
from backend_app.routes.auth_routes import auth_routes
from backend_app.malware_analysis.analyze import analyze_file

class TestSystem(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.app = Flask(__name__)
        self.app.register_blueprint(file_upload_routes)
        self.app.register_blueprint(auth_routes)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create test files directory
        self.test_files_dir = os.path.join(os.path.dirname(__file__), 'test_files')
        if not os.path.exists(self.test_files_dir):
            os.makedirs(self.test_files_dir)
        
        # Create test files
        self.clean_file = os.path.join(self.test_files_dir, 'clean.exe')
        self.malicious_file = os.path.join(self.test_files_dir, 'malicious.exe')
        
        with open(self.clean_file, 'wb') as f:
            f.write(b'This is a clean file')
        with open(self.malicious_file, 'wb') as f:
            f.write(b'This is a malicious file')

    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_files_dir):
            for file in os.listdir(self.test_files_dir):
                os.remove(os.path.join(self.test_files_dir, file))
            os.rmdir(self.test_files_dir)

    def test_complete_system_flow(self):
        """Test complete system flow from login to file analysis"""
        # 1. Login
        login_response = self.client.post('/auth/login', json={
            'username': 'test_user',
            'password': 'test_password'
        })
        self.assertEqual(login_response.status_code, 200)
        token = json.loads(login_response.data)['token']

        # 2. Upload clean file
        with open(self.clean_file, 'rb') as f:
            clean_upload_response = self.client.post('/upload', 
                data={'file': f, 'userType': 'customer'},
                headers={'Authorization': f'Bearer {token}'}
            )
        self.assertEqual(clean_upload_response.status_code, 200)
        clean_result = json.loads(clean_upload_response.data)
        self.assertFalse(clean_result['analysis_result']['is_malicious'])

        # 3. Upload malicious file
        with open(self.malicious_file, 'rb') as f:
            malicious_upload_response = self.client.post('/upload', 
                data={'file': f, 'userType': 'customer'},
                headers={'Authorization': f'Bearer {token}'}
            )
        self.assertEqual(malicious_upload_response.status_code, 200)
        malicious_result = json.loads(malicious_upload_response.data)
        self.assertTrue(malicious_result['analysis_result']['is_malicious'])

    def test_performance(self):
        """Test system performance"""
        # Login
        login_response = self.client.post('/auth/login', json={
            'username': 'test_user',
            'password': 'test_password'
        })
        token = json.loads(login_response.data)['token']

        # Measure upload and analysis time
        start_time = time.time()
        with open(self.clean_file, 'rb') as f:
            response = self.client.post('/upload', 
                data={'file': f, 'userType': 'customer'},
                headers={'Authorization': f'Bearer {token}'}
            )
        end_time = time.time()
        
        # Verify response time is within acceptable limits (e.g., < 5 seconds)
        self.assertLess(end_time - start_time, 5)
        self.assertEqual(response.status_code, 200)

    def test_error_handling(self):
        """Test system error handling"""
        # 1. Test invalid login
        invalid_login_response = self.client.post('/auth/login', json={
            'username': 'invalid_user',
            'password': 'invalid_password'
        })
        self.assertEqual(invalid_login_response.status_code, 401)

        # 2. Test file upload with invalid token
        with open(self.clean_file, 'rb') as f:
            response = self.client.post('/upload', 
                data={'file': f, 'userType': 'customer'},
                headers={'Authorization': 'Bearer invalid_token'}
            )
        self.assertEqual(response.status_code, 401)

        # 3. Test file upload with invalid file type
        invalid_file = os.path.join(self.test_files_dir, 'invalid.txt')
        with open(invalid_file, 'w') as f:
            f.write('This is not an executable')
        
        with open(invalid_file, 'rb') as f:
            response = self.client.post('/upload', 
                data={'file': f, 'userType': 'customer'},
                headers={'Authorization': f'Bearer {token}'}
            )
        self.assertEqual(response.status_code, 400)

    def test_security(self):
        """Test system security measures"""
        # 1. Test rate limiting
        for _ in range(10):  # Attempt multiple logins
            self.client.post('/auth/login', json={
                'username': 'test_user',
                'password': 'test_password'
            })
        
        # 11th attempt should be rate limited
        response = self.client.post('/auth/login', json={
            'username': 'test_user',
            'password': 'test_password'
        })
        self.assertEqual(response.status_code, 429)

        # 2. Test file size limit
        large_file = os.path.join(self.test_files_dir, 'large.exe')
        with open(large_file, 'wb') as f:
            f.write(b'0' * (10 * 1024 * 1024))  # 10MB file
        
        with open(large_file, 'rb') as f:
            response = self.client.post('/upload', 
                data={'file': f, 'userType': 'customer'},
                headers={'Authorization': f'Bearer {token}'}
            )
        self.assertEqual(response.status_code, 413)  # Payload Too Large

if __name__ == '__main__':
    unittest.main() 