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

---

## Authentication

All API endpoints except `/api/user/gettoken` require HTTP Basic Authentication using the email and token obtained from the `/api/user/gettoken` endpoint.