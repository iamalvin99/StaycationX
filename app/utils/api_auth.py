from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.models.users import User
from app.models.token import UserTokens

api_auth = HTTPBasicAuth()

@api_auth.verify_password
def verify_password(email, token):
    """
    Verify password for HTTP Basic Auth.
    This function is used by Flask-HTTPAuth to authenticate API requests.
    """
    print(f"verify_password called with email: {email}")
    print(f"Token received: {token}")
    
    user_token = UserTokens.getToken(email=email)
    print(f"User token from DB: {user_token.token if user_token and user_token.token else 'No token found'}")
    
    if user_token and user_token.token == token:
        print(f"Authentication successful for {email}")
        return True
    else:
        print(f"Authentication failed for {email}")
        return False

def generate_user_token(email, password):
    """
    Generate a new token for a user.
    
    Args:
        email (string): User's email address
        password (string): User's password
        
    Returns:
        tuple: (success: bool, token: string or None, error_message: string or None)
    """
    # Request validation
    if not email or not password:
        return False, None, "You have to enter a valid email address and valid password"
    
    # Check if user exists and verify password
    user = User.getUser(email=email)
    if not user:
        return False, None, "User is not registered"
    
    if not check_password_hash(user.password, password):
        return False, None, "Authentication failed"
    
    # If token already exists, return the token
    existing_token = UserTokens.getToken(email=email)
    if existing_token:
        return True, existing_token.token, None
    
    # If there isn't already a token, generate a new token
    current_datetime = datetime.now()
    datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    token = generate_password_hash(user.email + datetime_str, method='sha256')
    
    UserTokens.createToken(email=user.email, token=token)
    
    saved_token = UserTokens.getToken(email=email)
    return True, saved_token.token, None