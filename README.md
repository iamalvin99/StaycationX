# [Staycation API branch]

- Added controllers/api.py and models/token.py
- requirements.txt `flask-httpauth` and `Flask-CORS` (which is to allow cross original calls form ReactJS)

## Containerization

- Added Dockerfile to run the flask app under Gunicorn as a container


# [Saycation Nginx branch]

- To run web, app and db server processes manually
  
* `gunicorn --bind 0.0.0.0:5000 -m 007 -e FLASK_ENV=development --workers=5 "app:create_app()"` 
* or `FLASK_ENV="development" gunicorn --bind 0.0.0.0:5000 -m 007 --workers=5 "app:create_app()"`
* `sudo nginx -c /d/Desktop/ICT381/tars/staycationX/nginx.conf`

# StaycationX API Documentation

## API Endpoints

### Authentication

#### POST /api/user/gettoken

**Description:** Generate an authentication token for API access

**HEADER PARAMETERS**
- None required

**BODY PARAMETERS**
- `email` (string, required): User's email address
- `password` (string, required): User's password

**Sample Request**
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

**Sample Response**
```json
{
    "token": "sha256$abc123def456..."
}
```

**Possible Error Responses**
- 400 - You have to enter a valid email address and valid password
- 401 - Authentication failed
- 404 - User is not registered

**Python Sample Code with Error Handling**
```python
import requests
import json
from requests.exceptions import RequestException, ConnectionError, Timeout

def get_auth_token(base_url, email, password):
    """
    Get authentication token for API access
    """
    url = f"{base_url}/api/user/gettoken"
    
    payload = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Token obtained successfully: {data.get('token', '')[:20]}...")
            return data.get('token')
        elif response.status_code == 400:
            print("Error 400: You have to enter a valid email address and valid password")
        elif response.status_code == 401:
            print("Error 401: Authentication failed")
        elif response.status_code == 404:
            print("Error 404: User is not registered")
        else:
            print(f"Unexpected error: {response.status_code} - {response.text}")
            
    except ConnectionError:
        print("Connection Error: Unable to connect to the server")
    except Timeout:
        print("Timeout Error: Request timed out")
    except RequestException as e:
        print(f"Request Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None

if __name__ == "__main__":
    BASE_URL = "http://localhost:5000"
    email = "user@example.com"
    password = "password123"
    
    token = get_auth_token(BASE_URL, email, password)
    if token:
        print(f"Token: {token}")
```

---

### Package Management

#### POST /api/package/getAllPackages

**Description:** Retrieve all available staycation packages

**HEADER PARAMETERS**
- `Authorization` (string, required): Basic authentication with email:token

**BODY PARAMETERS**
- None required

**Sample Request**
```bash
Authorization: Basic dXNlckBleGFtcGxlLmNvbTpzaGEyNTYkYWJjMTIzZGVmNDU2Li4u
```

**Sample Response**
```json
{
    "data": [
        {
            "id": 1,
            "hotel_name": "Marina Bay Sands",
            "duration": 2,
            "unit_cost": 500.0,
            "image_url": "https://example.com/mbs.jpg",
            "description": "Luxury hotel with iconic infinity pool"
        },
        {
            "id": 2,
            "hotel_name": "Shangri-La Singapore",
            "duration": 2,
            "unit_cost": 450.0,
            "image_url": "https://example.com/shangrila.jpg",
            "description": "Treat the entire family to a luxurious staycation experience complete with world-class culinary experiences at The Singapore."
        }
    ]
}
```

**Possible Error Responses**
- 401 - Authentication required

**Python Sample Code with Error Handling**
```python
import requests
import base64
import json
from requests.exceptions import RequestException, ConnectionError, Timeout

def get_all_packages(base_url, email, token):
    """
    Retrieve all available staycation packages
    """
    url = f"{base_url}/api/package/getAllPackages"
    
    # Create Basic Auth header
    credentials = f"{email}:{token}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            packages = data.get('data', [])
            print(f"Retrieved {len(packages)} packages successfully")
            return packages
        elif response.status_code == 401:
            print("Error 401: Authentication required")
        else:
            print(f"Unexpected error: {response.status_code} - {response.text}")
            
    except ConnectionError:
        print("Connection Error: Unable to connect to the server")
    except Timeout:
        print("Timeout Error: Request timed out")
    except RequestException as e:
        print(f"Request Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None

if __name__ == "__main__":
    BASE_URL = "http://localhost:5000"
    email = "user@example.com"
    token = "sha256$abc123def456..."
    
    packages = get_all_packages(BASE_URL, email, token)
    if packages:
        for package in packages:
            print(f"Package: {package.get('hotel_name')} - ${package.get('unit_cost')}")
```

---

### Booking Management

#### POST /api/book/newBooking

**Description:** Create a new booking for a staycation package

**HEADER PARAMETERS**
- `Authorization` (string, required): Basic authentication with email:token

**BODY PARAMETERS**
- `check_in_date` (string, required): Check-in date in YYYY-MM-DD format
- `user_email` (string, required): User's email address
- `hotel_name` (string, required): Name of the hotel

**Sample Request**
```json
{
    "check_in_date": "2024-12-25",
    "user_email": "user@example.com",
    "hotel_name": "Marina Bay Sands"
}
```

**Sample Response**
```json
{
    "message": "Booking created successfully"
}
```

**Possible Error Responses**
- 400 - Invalid data format
- 401 - Unauthorized Access

**Python Sample Code with Error Handling**
```python
import requests
import base64
import json
from requests.exceptions import RequestException, ConnectionError, Timeout

def create_booking(base_url, email, token, check_in_date, user_email, hotel_name):
    """
    Create a new booking for a staycation package
    """
    url = f"{base_url}/api/book/newBooking"
    
    # Create Basic Auth header
    credentials = f"{email}:{token}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "check_in_date": check_in_date,
        "user_email": user_email,
        "hotel_name": hotel_name
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"{data.get('message', 'Booking created successfully')}")
            return True
        elif response.status_code == 400:
            print("Error 400: Invalid data format")
        elif response.status_code == 401:
            print("Error 401: Unauthorized Access")
        else:
            print(f"Unexpected error: {response.status_code} - {response.text}")
            
    except ConnectionError:
        print("Connection Error: Unable to connect to the server")
    except Timeout:
        print("Timeout Error: Request timed out")
    except RequestException as e:
        print(f"Request Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return False

if __name__ == "__main__":
    BASE_URL = "http://localhost:5000"
    email = "user@example.com"
    token = "sha256$abc123def456..."
    
    success = create_booking(
        BASE_URL, email, token,
        "2024-12-25", "user@example.com", "Shangri-La Singapore"
    )
    if success:
        print("Booking created successfully!")
```

#### POST /api/book/manageBooking

**Description:** Retrieve all bookings for a user

**HEADER PARAMETERS**
- `Authorization` (string, required): Basic authentication with email:token

**BODY PARAMETERS**
- `user_email` (string, required): User's email address

**Sample Request**
```json
{
    "user_email": "user@example.com"
}
```

**Sample Response**
```json
{
    "data": [
        {
            "check_in_date": "Wed, 25 Dec 2024 00:00:00 GMT",
            "customer": "admin@abc.com",
            "package": "Shangri-La Singapore",
            "total_cost": 900.0
        }
    ],
    "message": "Booking retrieved successfully"
}
```

**Possible Error Responses**
- 400 - No booking under {user_email}
- 401 - Unauthorized Access

**Python Sample Code with Error Handling**
```python
import requests
import base64
import json
from requests.exceptions import RequestException, ConnectionError, Timeout

def get_user_bookings(base_url, email, token, user_email):
    """
    Retrieve all bookings for a user
    """
    url = f"{base_url}/api/book/manageBooking"
    
    # Create Basic Auth header
    credentials = f"{email}:{token}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "user_email": user_email
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            bookings = data.get('data', [])
            print(f"{data.get('message', 'Bookings retrieved successfully')}")
            print(f"Found {len(bookings)} bookings")
            return bookings
        elif response.status_code == 400:
            print(f"Error 400: No booking under {user_email}")
        elif response.status_code == 401:
            print("Error 401: Unauthorized Access")
        else:
            print(f"Unexpected error: {response.status_code} - {response.text}")
            
    except ConnectionError:
        print("Connection Error: Unable to connect to the server")
    except Timeout:
        print("Timeout Error: Request timed out")
    except RequestException as e:
        print(f"Request Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None

if __name__ == "__main__":
    BASE_URL = "http://localhost:5000"
    email = "user@example.com"
    token = "sha256$abc123def456..."
    user_email = "user@example.com"
    
    bookings = get_user_bookings(BASE_URL, email, token, user_email)
    if bookings:
        for booking in bookings:
            print(f"Booking: {booking.get('package')} - {booking.get('check_in_date')}")
```

#### POST /api/book/updateBooking

**Description:** Update an existing booking

**HEADER PARAMETERS**
- `Authorization` (string, required): Basic authentication with email:token

**BODY PARAMETERS**
- `user_email` (string, required): User's email address
- `old_check_in_date` (string, required): Original check-in date
- `new_check_in_date` (string, required): New check-in date
- `hotel_name` (string, required): Name of the hotel/package

**Sample Request**
```json
{
    "old_check_in_date": "2024-12-25",
    "new_check_in_date": "2024-12-26",
    "user_email": "admin@abc.com",
    "hotel_name": "Shangri-La Singapore"
}
```

**Sample Response**
```json
{
    "message": "Booking updated successfully"
}
```

**Possible Error Responses**
- 400 - No booking under {user_email}, {old_check_in_date} and {hotel_name}
- 400 - Booking update failed
- 401 - Unauthorized Access

**Python Sample Code with Error Handling**
```python
import requests
import base64
import json
from requests.exceptions import RequestException, ConnectionError, Timeout

def update_booking(base_url, email, token, user_email, old_check_in_date, new_check_in_date, hotel_name):
    """
    Update an existing booking
    """
    url = f"{base_url}/api/book/updateBooking"
    
    # Create Basic Auth header
    credentials = f"{email}:{token}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "user_email": user_email,
        "old_check_in_date": old_check_in_date,
        "new_check_in_date": new_check_in_date,
        "hotel_name": hotel_name
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"{data.get('message', 'Booking updated successfully')}")
            return True
        elif response.status_code == 400:
            error_msg = response.text
            if "No booking under" in error_msg:
                print(f"Error 400: No booking under {user_email}, {old_check_in_date} and {hotel_name}")
            elif "Booking update failed" in error_msg:
                print("Error 400: Booking update failed")
            else:
                print(f"Error 400: {error_msg}")
        elif response.status_code == 401:
            print("Error 401: Unauthorized Access")
        else:
            print(f"Unexpected error: {response.status_code} - {response.text}")
            
    except ConnectionError:
        print("Connection Error: Unable to connect to the server")
    except Timeout:
        print("Timeout Error: Request timed out")
    except RequestException as e:
        print(f"Request Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return False

if __name__ == "__main__":
    BASE_URL = "http://localhost:5000"
    email = "user@example.com"
    token = "sha256$abc123def456..."
    
    success = update_booking(
        BASE_URL, email, token,
        "admin@abc.com", "2024-12-25", "2024-12-26", "Shangri-La Singapore"
    )
    if success:
        print("Booking updated successfully!")
```

#### POST /api/book/deleteBooking

**Description:** Delete an existing booking

**HEADER PARAMETERS**
- `Authorization` (string, required): Basic authentication with email:token

**BODY PARAMETERS**
- `user_email` (string, required): User's email address
- `check_in_date` (string, required): Check-in date
- `hotel_name` (string, required): Name of the hotel/package

**Sample Request**
```json
{
    "user_email": "user@example.com",
    "check_in_date": "2024-12-25",
    "hotel_name": "Shangri-La Singapore"
}
```

**Sample Response**
```json
{
    "message": "Booking delete successfully"
}
```

**Possible Error Responses**
- 400 - No booking under {user_email}, {check_in_date} and {hotel_name}
- 400 - Booking deletion failed
- 401 - Authentication required

**Python Sample Code with Error Handling**
```python
import requests
import base64
import json
from requests.exceptions import RequestException, ConnectionError, Timeout

def delete_booking(base_url, email, token, user_email, check_in_date, hotel_name):
    """
    Delete an existing booking
    """
    url = f"{base_url}/api/book/deleteBooking"
    
    # Create Basic Auth header
    credentials = f"{email}:{token}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "user_email": user_email,
        "check_in_date": check_in_date,
        "hotel_name": hotel_name
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"{data.get('message', 'Booking deleted successfully')}")
            return True
        elif response.status_code == 400:
            error_msg = response.text
            if "No booking under" in error_msg:
                print(f"Error 400: No booking under {user_email}, {check_in_date} and {hotel_name}")
            elif "Booking deletion failed" in error_msg:
                print("Error 400: Booking deletion failed")
            else:
                print(f"Error 400: {error_msg}")
        elif response.status_code == 401:
            print("Error 401: Authentication required")
        else:
            print(f"Unexpected error: {response.status_code} - {response.text}")
            
    except ConnectionError:
        print("Connection Error: Unable to connect to the server")
    except Timeout:
        print("Timeout Error: Request timed out")
    except RequestException as e:
        print(f"Request Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return False

if __name__ == "__main__":
    BASE_URL = "http://localhost:5000"
    email = "user@example.com"
    token = "sha256$abc123def456..."
    
    success = delete_booking(
        BASE_URL, email, token,
        "user@example.com", "2024-12-25", "Shangri-La Singapore"
    )
    if success:
        print("Booking deleted successfully!")
```

---

### Review Management

#### POST /api/review/createReview

**Description:** Create a new review for a booking

**HEADER PARAMETERS**
- `Authorization` (string, required): Basic authentication with email:token

**BODY PARAMETERS**
- `hotel_name` (string, required): Name of the hotel/package
- `rating` (integer, required): Rating from 1-5
- `title` (string, required): Review title
- `comment` (string, required): Review comment
- `check_in_date` (string, required): Check-in date of the booking

**Sample Request**
```json
{
    "hotel_name": "Shangri-La Singapore",
    "rating": 5,
    "title": "Amazing Stay!",
    "comment": "Very good experience!",
    "check_in_date": "2025-10-11"
}
```

**Sample Response**
```json
{
    "data": {
        "comment": "Very good experience!",
        "customer": "admin@abc.com",
        "date": "Sun, 19 Oct 2025 16:58:33 GMT",
        "image_url": null,
        "package": "Shangri-La Singapore",
        "rating": 5,
        "suggested_theme": null,
        "title": "Amazing Stay!"
    },
    "message": "Review created successfully"
}
```

**Possible Error Responses**
- 400 - Missing required fields
- 400 - Invalid data format
- 401 - Authentication required
- 401 - Unauthorized Access
- 404 - User not found
- 404 - Package not found
- 404 - Booking not found
- 409 - Review already exists for this booking
- 500 - Failed to create review

**Python Sample Code with Error Handling**
```python
import requests
import base64
import json
from requests.exceptions import RequestException, ConnectionError, Timeout

def create_review(base_url, email, token, hotel_name, rating, title, comment, check_in_date):
    """
    Create a new review for a booking
    """
    url = f"{base_url}/api/review/createReview"
    
    # Create Basic Auth header
    credentials = f"{email}:{token}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "hotel_name": hotel_name,
        "rating": rating,
        "title": title,
        "comment": comment,
        "check_in_date": check_in_date
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"{data.get('message', 'Review created successfully')}")
            return data.get('data')
        elif response.status_code == 400:
            error_msg = response.text
            if "Missing required fields" in error_msg:
                print("Error 400: Missing required fields")
            elif "Invalid data format" in error_msg:
                print("Error 400: Invalid data format")
            else:
                print(f"Error 400: {error_msg}")
        elif response.status_code == 401:
            error_msg = response.text
            if "Authentication required" in error_msg:
                print("Error 401: Authentication required")
            elif "Unauthorized Access" in error_msg:
                print("Error 401: Unauthorized Access")
            else:
                print(f"Error 401: {error_msg}")
        elif response.status_code == 404:
            error_msg = response.text
            if "User not found" in error_msg:
                print("Error 404: User not found")
            elif "Package not found" in error_msg:
                print("Error 404: Package not found")
            elif "Booking not found" in error_msg:
                print("Error 404: Booking not found")
            else:
                print(f"Error 404: {error_msg}")
        elif response.status_code == 409:
            print("Error 409: Review already exists for this booking")
        elif response.status_code == 500:
            print("Error 500: Failed to create review")
        else:
            print(f"Unexpected error: {response.status_code} - {response.text}")
            
    except ConnectionError:
        print("Connection Error: Unable to connect to the server")
    except Timeout:
        print("Timeout Error: Request timed out")
    except RequestException as e:
        print(f"Request Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None

if __name__ == "__main__":
    BASE_URL = "http://localhost:5000"
    email = "user@example.com"
    token = "sha256$abc123def456..."
    
    review_data = create_review(
        BASE_URL, email, token,
        "Shangri-La Singapore", 5, "Amazing Stay!", "Very good experience!", "2025-10-11"
    )
    if review_data:
        print(f"Review created: {review_data.get('title')} - Rating: {review_data.get('rating')}")
```

#### POST /api/review/getAllReviews

**Description:** Retrieve all reviews

**HEADER PARAMETERS**
- `Authorization` (string, required): Basic authentication with email:token

**BODY PARAMETERS**
- None required

**Sample Response**
```json
{
    "data": [
        {
            "comment": "Very good experience!",
            "customer": "admin@abc.com",
            "date": "Mon, 20 Oct 2025 16:00:29 GMT",
            "image_url": null,
            "package": "Shangri-La Singapore",
            "rating": 5,
            "suggested_theme": null,
            "title": "Amazing Stay!"
        }
    ],
    "message": "Reviews retrieved successfully"
}
```

**Possible Error Responses**
- 401 - Unauthorized Access
- 500 - Failed to retrieve reviews

**Python Sample Code with Error Handling**
```python
import requests
import base64
import json
from requests.exceptions import RequestException, ConnectionError, Timeout

def get_all_reviews(base_url, email, token):
    """
    Retrieve all reviews
    """
    url = f"{base_url}/api/review/getAllReviews"
    
    # Create Basic Auth header
    credentials = f"{email}:{token}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            reviews = data.get('data', [])
            print(f"{data.get('message', 'Reviews retrieved successfully')}")
            print(f"Found {len(reviews)} reviews")
            return reviews
        elif response.status_code == 401:
            print("Error 401: Unauthorized Access")
        elif response.status_code == 500:
            print("Error 500: Failed to retrieve reviews")
        else:
            print(f"Unexpected error: {response.status_code} - {response.text}")
            
    except ConnectionError:
        print("Connection Error: Unable to connect to the server")
    except Timeout:
        print("Timeout Error: Request timed out")
    except RequestException as e:
        print(f"Request Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None

if __name__ == "__main__":
    BASE_URL = "http://localhost:5000"
    email = "user@example.com"
    token = "sha256$abc123def456..."
    
    reviews = get_all_reviews(BASE_URL, email, token)
    if reviews:
        for review in reviews:
            print(f"Review: {review.get('title')} - Rating: {review.get('rating')}/5")
```

#### POST /api/review/getReviewByBooking

**Description:** Retrieve a specific review by booking details

**HEADER PARAMETERS**
- `Authorization` (string, required): Basic authentication with email:token

**BODY PARAMETERS**
- `user_email` (string, required): User's email address
- `hotel_name` (string, required): Name of the hotel/package
- `check_in_date` (string, required): Check-in date

**Sample Request**
```json
{
    "user_email": "admin@abc.com",
    "hotel_name": "Shangri-La Singapore",
    "check_in_date": "2024-12-26"
}
```

**Sample Response**
```json
{
    "data": {
        "comment": "Very good experience!",
        "customer": "admin@abc.com",
        "date": "Mon, 20 Oct 2025 16:00:29 GMT",
        "image_url": null,
        "package": "Shangri-La Singapore",
        "rating": 5,
        "suggested_theme": null,
        "title": "Amazing Stay!"
    },
    "message": "Review retrieved successfully"
}
```

**Possible Error Responses**
- 400 - Missing required fields
- 400 - Invalid data format
- 401 - Unauthorized Access
- 404 - User not found
- 404 - Booking not found
- 404 - Review not found for this booking
- 500 - Failed to retrieve review

**Python Sample Code with Error Handling**
```python
import requests
import base64
import json
from requests.exceptions import RequestException, ConnectionError, Timeout

def get_review_by_booking(base_url, email, token, user_email, hotel_name, check_in_date):
    """
    Retrieve a specific review by booking details
    """
    url = f"{base_url}/api/review/getReviewByBooking"
    
    # Create Basic Auth header
    credentials = f"{email}:{token}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "user_email": user_email,
        "hotel_name": hotel_name,
        "check_in_date": check_in_date
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            review = data.get('data')
            print(f"{data.get('message', 'Review retrieved successfully')}")
            return review
        elif response.status_code == 400:
            error_msg = response.text
            if "Missing required fields" in error_msg:
                print("Error 400: Missing required fields")
            elif "Invalid data format" in error_msg:
                print("Error 400: Invalid data format")
            else:
                print(f"Error 400: {error_msg}")
        elif response.status_code == 401:
            print("Error 401: Unauthorized Access")
        elif response.status_code == 404:
            error_msg = response.text
            if "User not found" in error_msg:
                print("Error 404: User not found")
            elif "Booking not found" in error_msg:
                print("Error 404: Booking not found")
            elif "Review not found for this booking" in error_msg:
                print("Error 404: Review not found for this booking")
            else:
                print(f"Error 404: {error_msg}")
        elif response.status_code == 500:
            print("Error 500: Failed to retrieve review")
        else:
            print(f"Unexpected error: {response.status_code} - {response.text}")
            
    except ConnectionError:
        print("Connection Error: Unable to connect to the server")
    except Timeout:
        print("Timeout Error: Request timed out")
    except RequestException as e:
        print(f"Request Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None

if __name__ == "__main__":
    BASE_URL = "http://localhost:5000"
    email = "user@example.com"
    token = "sha256$abc123def456..."
    
    review = get_review_by_booking(
        BASE_URL, email, token,
        "admin@abc.com", "Shangri-La Singapore", "2024-12-26"
    )
    if review:
        print(f"Review: {review.get('title')} - Rating: {review.get('rating')}/5")
```

#### POST /api/review/updateReview

**Description:** Update an existing review

**HEADER PARAMETERS**
- `Authorization` (string, required): Basic authentication with email:token

**BODY PARAMETERS**
- `hotel_name` (string, required): Name of the hotel/package
- `check_in_date` (string, required): Check-in date
- `rating` (integer, optional): New rating from 1-5
- `title` (string, optional): New review title
- `comment` (string, optional): New review comment
- `image_url` (string, optional): New image URL
- `suggested_theme` (string, optional): New suggested theme

**Sample Request**
```json
{
    "hotel_name": "Shangri-La Singapore",
    "rating": 4,
    "title": "Amazing Stay!",
    "comment": "Very good experience!",
    "check_in_date": "2024-12-26"
}
```

**Sample Response**
```json
{
    "data": {
        "comment": "Very good experience!",
        "customer": "admin@abc.com",
        "date": "Mon, 20 Oct 2025 16:00:29 GMT",
        "image_url": null,
        "package": "Shangri-La Singapore",
        "rating": 4,
        "suggested_theme": null,
        "title": "Amazing Stay!"
    },
    "message": "Review updated successfully"
}
```

**Possible Error Responses**
- 400 - Missing required fields
- 400 - Invalid data format
- 401 - Authentication required
- 401 - Unauthorized Access
- 404 - User not found
- 404 - Package not found
- 404 - Booking not found
- 404 - Review not found for this booking
- 500 - Failed to update review

**Python Sample Code with Error Handling**
```python
import requests
import base64
import json
from requests.exceptions import RequestException, ConnectionError, Timeout

def update_review(base_url, email, token, hotel_name, check_in_date, **kwargs):
    """
    Update an existing review
    """
    url = f"{base_url}/api/review/updateReview"
    
    # Create Basic Auth header
    credentials = f"{email}:{token}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "hotel_name": hotel_name,
        "check_in_date": check_in_date
    }
    
    optional_params = ['rating', 'title', 'comment', 'image_url', 'suggested_theme']
    for param in optional_params:
        if param in kwargs:
            payload[param] = kwargs[param]
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"{data.get('message', 'Review updated successfully')}")
            return data.get('data')
        elif response.status_code == 400:
            error_msg = response.text
            if "Missing required fields" in error_msg:
                print("Error 400: Missing required fields")
            elif "Invalid data format" in error_msg:
                print("Error 400: Invalid data format")
            else:
                print(f"Error 400: {error_msg}")
        elif response.status_code == 401:
            error_msg = response.text
            if "Authentication required" in error_msg:
                print("Error 401: Authentication required")
            elif "Unauthorized Access" in error_msg:
                print("Error 401: Unauthorized Access")
            else:
                print(f"Error 401: {error_msg}")
        elif response.status_code == 404:
            error_msg = response.text
            if "User not found" in error_msg:
                print("Error 404: User not found")
            elif "Package not found" in error_msg:
                print("Error 404: Package not found")
            elif "Booking not found" in error_msg:
                print("Error 404: Booking not found")
            elif "Review not found for this booking" in error_msg:
                print("Error 404: Review not found for this booking")
            else:
                print(f"Error 404: {error_msg}")
        elif response.status_code == 500:
            print("Error 500: Failed to update review")
        else:
            print(f"Unexpected error: {response.status_code} - {response.text}")
            
    except ConnectionError:
        print("Connection Error: Unable to connect to the server")
    except Timeout:
        print("Timeout Error: Request timed out")
    except RequestException as e:
        print(f"Request Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None

if __name__ == "__main__":
    BASE_URL = "http://localhost:5000"
    email = "user@example.com"
    token = "sha256$abc123def456..."
    
    updated_review = update_review(
        BASE_URL, email, token,
        "Shangri-La Singapore", "2024-12-26",
        rating=4, title="Updated Review", comment="Updated experience!"
    )
    if updated_review:
        print(f"Review updated: {updated_review.get('title')} - Rating: {updated_review.get('rating')}")
```

#### POST /api/review/deleteReview

**Description:** Delete an existing review

**HEADER PARAMETERS**
- `Authorization` (string, required): Basic authentication with email:token

**BODY PARAMETERS**
- `hotel_name` (string, required): Name of the hotel/package
- `check_in_date` (string, required): Check-in date

**Sample Request**
```json
{
    "hotel_name": "Shangri-La Singapore",
    "check_in_date": "2024-12-26"
}
```

**Sample Response**
```json
{
    "message": "Review deleted successfully"
}
```

**Possible Error Responses**
- 400 - Missing required fields
- 400 - Invalid data format
- 401 - Authentication required
- 401 - Unauthorized Access
- 404 - User not found
- 404 - Package not found
- 404 - Booking not found
- 404 - Review not found for this booking
- 500 - Failed to delete review

**Python Sample Code with Error Handling**
```python
import requests
import base64
import json
from requests.exceptions import RequestException, ConnectionError, Timeout

def delete_review(base_url, email, token, hotel_name, check_in_date):
    """
    Delete an existing review
    """
    url = f"{base_url}/api/review/deleteReview"
    
    # Create Basic Auth header
    credentials = f"{email}:{token}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "hotel_name": hotel_name,
        "check_in_date": check_in_date
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"{data.get('message', 'Review deleted successfully')}")
            return True
        elif response.status_code == 400:
            error_msg = response.text
            if "Missing required fields" in error_msg:
                print("Error 400: Missing required fields")
            elif "Invalid data format" in error_msg:
                print("Error 400: Invalid data format")
            else:
                print(f"Error 400: {error_msg}")
        elif response.status_code == 401:
            error_msg = response.text
            if "Authentication required" in error_msg:
                print("Error 401: Authentication required")
            elif "Unauthorized Access" in error_msg:
                print("Error 401: Unauthorized Access")
            else:
                print(f"Error 401: {error_msg}")
        elif response.status_code == 404:
            error_msg = response.text
            if "User not found" in error_msg:
                print("Error 404: User not found")
            elif "Package not found" in error_msg:
                print("Error 404: Package not found")
            elif "Booking not found" in error_msg:
                print("Error 404: Booking not found")
            elif "Review not found for this booking" in error_msg:
                print("Error 404: Review not found for this booking")
            else:
                print(f"Error 404: {error_msg}")
        elif response.status_code == 500:
            print("Error 500: Failed to delete review")
        else:
            print(f"Unexpected error: {response.status_code} - {response.text}")
            
    except ConnectionError:
        print("Connection Error: Unable to connect to the server")
    except Timeout:
        print("Timeout Error: Request timed out")
    except RequestException as e:
        print(f"Request Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return False

if __name__ == "__main__":
    BASE_URL = "http://localhost:5000"
    email = "user@example.com"
    token = "sha256$abc123def456..."
    
    success = delete_review(
        BASE_URL, email, token,
        "Shangri-La Singapore", "2024-12-26"
    )
    if success:
        print("Review deleted successfully!")
```

---

### Protected Route

#### GET /api/protected

**Description:** Test endpoint to verify authentication

**HEADER PARAMETERS**
- `Authorization` (string, required): Basic authentication with email:token

**Sample Response**
```json
{
    "message": "You are authorized to see this message"
}
```

**Possible Error Responses**
- 401 - Unauthorized Access

**Python Sample Code with Error Handling**
```python
import requests
import base64
import json
from requests.exceptions import RequestException, ConnectionError, Timeout

def test_protected_route(base_url, email, token):
    """
    Test endpoint to verify authentication
    """
    url = f"{base_url}/api/protected"
    
    # Create Basic Auth header
    credentials = f"{email}:{token}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"{data.get('message', 'Authentication successful')}")
            return True
        elif response.status_code == 401:
            print("Error 401: Unauthorized Access")
        else:
            print(f"Unexpected error: {response.status_code} - {response.text}")
            
    except ConnectionError:
        print("Connection Error: Unable to connect to the server")
    except Timeout:
        print("Timeout Error: Request timed out")
    except RequestException as e:
        print(f"Request Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return False

if __name__ == "__main__":
    BASE_URL = "http://localhost:5000"
    email = "user@example.com"
    token = "sha256$abc123def456..."
    
    success = test_protected_route(BASE_URL, email, token)
    if success:
        print("Authentication test successful!")
```

---

## Authentication

All API endpoints except `/api/user/gettoken` require HTTP Basic Authentication using the email and token obtained from the `/api/user/gettoken` endpoint.