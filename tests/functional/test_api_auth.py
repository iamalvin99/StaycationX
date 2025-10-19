import json
import base64
import pytest
from app.models.users import User
from app.models.token import UserTokens
from app.utils.api_auth import generate_user_token
from werkzeug.security import generate_password_hash

class TestAPIAuthentication:
    """Test cases for API authentication"""

    def test_gettoken_success(self, client):
        """
        GIVEN a valid user with correct credentials
        WHEN requesting a token from /api/user/gettoken
        THEN should return a token string
        """
        try:
            hashpass = generate_password_hash("12345", method='sha256')
            user = User.createUser(email="testuser@example.com", password=hashpass, name="Test User")
            
            response = client.post("/api/user/gettoken", json={
                'email': 'testuser@example.com',
                'password': '12345'
            })
            
            print(f"Response status: {response.status_code}")
            print(f"Response data: {response.text}")
            
            assert response.status_code == 200
            response_data = json.loads(response.text)
            
            # Should return token
            assert 'token' in response_data
            assert isinstance(response_data['token'], str)
            assert response_data['token'].startswith('sha256$')
        except Exception as e:
            print(f"Test error: {e}")
            raise

    def test_gettoken_invalid_credentials(self, client):
        """
        GIVEN invalid credentials
        WHEN requesting a token from /api/user/gettoken
        THEN should return 404 Not Found
        """
        response = client.post("/api/user/gettoken", json={
            'email': 'test@test.com',
            'password': 'randomPassword123'
        })
        
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.text}")
        
        assert response.status_code == 404
        response_data = json.loads(response.text)
        assert 'error' in response_data

    def test_gettoken_missing_credentials(self, client):
        """
        GIVEN missing email or password
        WHEN requesting a token from /api/user/gettoken
        THEN should return 400 Bad Request
        """
        # Missing password
        response = client.post("/api/user/gettoken", json={
            'email': 'test@test.com'
        })
        print(f"Missing password - Status: {response.status_code}")
        assert response.status_code == 400
        
        # Missing email
        response = client.post("/api/user/gettoken", json={
            'password': 'randomPassword123'
        })
        print(f"Missing email - Status: {response.status_code}")
        assert response.status_code == 400

    def test_gettoken_wrong_password(self, client):
        """
        GIVEN a valid user with wrong password
        WHEN requesting a token from /api/user/gettoken
        THEN should return 401 Unauthorized
        """

        hashpass = generate_password_hash("correctpassword", method='sha256')
        user = User.createUser(email="wrongpass@example.com", password=hashpass, name="Wrong Pass User")
        
        # Try with wrong password
        response = client.post("/api/user/gettoken", json={
            'email': 'wrongpass@example.com',
            'password': 'wrongpassword'
        })
        
        print(f"Wrong password - Status: {response.status_code}")
        print(f"Wrong password - Response: {response.text}")
        
        assert response.status_code == 401
        response_data = json.loads(response.text)
        assert 'error' in response_data
        assert 'Authentication failed' in response_data['error']

    def test_gettoken_new_user_token_generation(self, client):
        """
        GIVEN a new user (no existing token)
        WHEN requesting a token from /api/user/gettoken
        THEN should generate a new token
        """
        # Create a new user
        hashpass = generate_password_hash("newuser123", method='sha256')
        user = User.createUser(email="newuser@example.com", password=hashpass, name="New User")
        
        # Make sure no existing token
        existing_token = UserTokens.getToken(email="newuser@example.com")
        if existing_token:
            existing_token.delete()
        
        response = client.post("/api/user/gettoken", json={
            'email': 'newuser@example.com',
            'password': 'newuser123'
        })
        
        print(f"New user token - Status: {response.status_code}")
        print(f"New user token - Response: {response.text}")
        
        assert response.status_code == 200
        response_data = json.loads(response.text)
        assert 'token' in response_data
        assert isinstance(response_data['token'], str)
        assert response_data['token'].startswith('sha256$')

    def test_generate_user_token_direct_empty_credentials(self):
        """
        GIVEN empty email or password
        WHEN calling generate_user_token directly
        THEN should return validation error
        """
        # Test empty email
        success, token, error = generate_user_token("", "password")
        assert success == False
        assert token is None
        assert error == "You have to enter a valid email address and valid password"
        
        # Test empty password
        success, token, error = generate_user_token("test@example.com", "")
        assert success == False
        assert token is None
        assert error == "You have to enter a valid email address and valid password"
        
        # Test both empty
        success, token, error = generate_user_token("", "")
        assert success == False
        assert token is None
        assert error == "You have to enter a valid email address and valid password"

    def test_protected_endpoint_with_valid_token(self, client):
        """
        GIVEN a valid token
        WHEN accessing a protected endpoint
        THEN should return 200 OK
        """
        try:
            # Create user and get token
            hashpass = generate_password_hash("12345", method='sha256')
            user = User.createUser(email="authuser@example.com", password=hashpass, name="Auth User")
            
            token_response = client.post("/api/user/gettoken", json={
                'email': 'authuser@example.com',
                'password': '12345'
            })
            
            print(f"Token response status: {token_response.status_code}")
            print(f"Token response data: {token_response.text}")
            
            assert token_response.status_code == 200
            token_data = json.loads(token_response.text)
            token = token_data['token']
            
            # Use token to access protected endpoint
            credentials = base64.b64encode(f"authuser@example.com:{token}".encode('utf-8')).decode('utf-8')
            headers = {'Authorization': f'Basic {credentials}'}
            
            response = client.post('/api/package/getAllPackages', headers=headers, json={})
            print(f"Protected endpoint status: {response.status_code}")
            print(f"Protected endpoint data: {response.text}")
            
            assert response.status_code == 201
        except Exception as e:
            print(f"Protected endpoint test error: {e}")
            raise

    def test_protected_endpoint_without_token(self, client):
        """
        GIVEN no authentication token
        WHEN accessing a protected endpoint
        THEN should return 401 Unauthorized
        """
        response = client.post('/api/package/getAllPackages', json={})
        print(f"No token response status: {response.status_code}")
        assert response.status_code == 401

    def test_protected_endpoint_with_invalid_token(self, client):
        """
        GIVEN an invalid token
        WHEN accessing a protected endpoint
        THEN should return 401 Unauthorized
        """
        credentials = base64.b64encode("user@example.com:invalidtoken".encode('utf-8')).decode('utf-8')
        headers = {'Authorization': f'Basic {credentials}'}
        
        response = client.post('/api/package/getAllPackages', headers=headers, json={})
        print(f"Invalid token response status: {response.status_code}")
        assert response.status_code == 401

    def test_gettoken_empty_credentials(self, client):
        """
        GIVEN empty email or password
        WHEN requesting a token from /api/user/gettoken
        THEN should return 400 Bad Request
        """
        # Empty email
        response = client.post("/api/user/gettoken", json={
            'email': '',
            'password': 'somepassword'
        })
        print(f"Empty email - Status: {response.status_code}")
        assert response.status_code == 400
        
        # Empty password
        response = client.post("/api/user/gettoken", json={
            'email': 'test@example.com',
            'password': ''
        })
        print(f"Empty password - Status: {response.status_code}")
        assert response.status_code == 400
        
        # Both empty
        response = client.post("/api/user/gettoken", json={
            'email': '',
            'password': ''
        })
        print(f"Both empty - Status: {response.status_code}")
        assert response.status_code == 400