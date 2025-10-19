import json
import base64
import pytest
from app.models.users import User
from app.models.package import Package
from app.models.book import Booking
from app.models.review import Review
from app.models.token import UserTokens
from app.utils.api_auth import generate_user_token
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

class TestReviewApiFunction:
    """Test cases for Review API"""

    @pytest.fixture(autouse=True)
    def setup_test_data(self, client):
        """Setup test data for each test"""
        # Create test user
        hashpass = generate_password_hash("12345", method='sha256')
        self.test_user = User.createUser(
            email="reviewuser@example.com", 
            password=hashpass, 
            name="Review Test User"
        )
        
        # Create test package
        self.test_package = Package.createPackage(
            hotel_name="Test Hotel",
            image_url="https://example.com/hotel.jpg",
            description="A test hotel",
            unit_cost=100.0,
            duration=2
        )
        
        # Create test booking
        check_in_date = "2025-10-11"
        self.test_booking = Booking.createBooking(
            check_in_date=check_in_date,
            customer=self.test_user,
            package=self.test_package
        )
        
        # Get authentication token
        success, token, error = generate_user_token("reviewuser@example.com", "12345")
        self.auth_token = token
        
        yield
        
        # Cleanup after each test
        Review.objects().delete()
        Booking.objects().delete()
        Package.objects().delete()
        User.objects().delete()
        UserTokens.objects().delete()

    def get_auth_headers(self):
        """Get authentication headers for API requests"""
        auth_string = base64.b64encode(f'reviewuser@example.com:{self.auth_token}'.encode()).decode()
        return {'Authorization': f'Basic {auth_string}'}

    def test_create_review_success(self, client):
        """
        GIVEN a valid user with a booking
        WHEN creating a review with valid data
        THEN should create the review successfully
        """
        review_data = {
            "hotel_name": "Test Hotel",
            "rating": 5,
            "title": "Excellent stay!",
            "comment": "The hotel was amazing with great service.",
            "check_in_date": "2025-10-11"
        }
        
        response = client.post(
            "/api/review/createReview",
            json=review_data,
            headers=self.get_auth_headers()
        )
        
        assert response.status_code == 201
        response_data = json.loads(response.text)
        assert response_data["message"] == "Review created successfully"
        assert "data" in response_data
        assert response_data["data"]["rating"] == 5
        assert response_data["data"]["title"] == "Excellent stay!"

    def test_create_review_duplicate(self, client):
        """
        GIVEN a user who already has a review for a booking
        WHEN trying to create another review for the same booking
        THEN should return 409 Conflict
        """
        # Create first review
        review_data = {
            "hotel_name": "Test Hotel",
            "rating": 5,
            "title": "First review",
            "comment": "Great stay!",
            "check_in_date": "2025-10-11"
        }
        
        client.post(
            "/api/review/createReview",
            json=review_data,
            headers=self.get_auth_headers()
        )
        
        # Try to create duplicate review
        duplicate_data = {
            "user_email": "reviewuser@example.com",
            "hotel_name": "Test Hotel",
            "rating": 3,
            "title": "Second review",
            "comment": "Another review",
            "check_in_date": "2025-10-11"
        }
        
        response = client.post(
            "/api/review/createReview",
            json=duplicate_data,
            headers=self.get_auth_headers()
        )
        
        assert response.status_code == 409
        response_data = json.loads(response.text)
        assert "Review already exists for this booking" in response_data["error"]

    def test_create_review_invalid_booking(self, client):
        """
        GIVEN a user without a booking for the specified hotel/date
        WHEN trying to create a review
        THEN should return 404 Not Found
        """
        review_data = {
            "hotel_name": "Non-existent Hotel",
            "rating": 5,
            "title": "Review for non-existent booking",
            "comment": "This should fail",
            "check_in_date": "2025-10-11"
        }
        
        response = client.post(
            "/api/review/createReview",
            json=review_data,
            headers=self.get_auth_headers()
        )
        
        assert response.status_code == 404
        response_data = json.loads(response.text)
        assert "Package not found" in response_data["error"]

    def test_get_all_reviews_success(self, client):
        """
        GIVEN multiple reviews exist in the system
        WHEN retrieving all reviews
        THEN should return all reviews successfully
        """
        # Create multiple reviews
        for i in range(3):
            review = Review.createReview(
                customer=self.test_user,
                package=self.test_package,
                booking=self.test_booking,
                rating= i + 1,
                title=f"Review {i + 1}",
                comment=f"Comment {i + 1}"
            )
        
        response = client.post(
            "/api/review/getAllReviews",
            headers=self.get_auth_headers()
        )
        
        assert response.status_code == 200
        response_data = json.loads(response.text)
        assert response_data["message"] == "Reviews retrieved successfully"
        assert len(response_data["data"]) == 3

    def test_get_all_reviews_empty(self, client):
        """
        GIVEN no reviews exist in the system
        WHEN retrieving all reviews
        THEN should return empty list successfully
        """
        response = client.post(
            "/api/review/getAllReviews",
            headers=self.get_auth_headers()
        )
        
        assert response.status_code == 200
        response_data = json.loads(response.text)
        assert response_data["message"] == "Reviews retrieved successfully"
        assert response_data["data"] == []

    def test_get_all_reviews_unauthorized(self, client):
        """
        GIVEN no authentication token
        WHEN trying to retrieve all reviews
        THEN should return 401 Unauthorized
        """
        response = client.post("/api/review/getAllReviews")
        
        assert response.status_code == 401

    def test_update_review_success(self, client):
        """
        GIVEN an existing review
        WHEN updating the review with new data
        THEN should update the review successfully
        """
        # Create initial review
        review = Review.createReview(
            customer=self.test_user,
            package=self.test_package,
            booking=self.test_booking,
            rating=3,
            title="Original title",
            comment="Original comment"
        )
        
        update_data = {
            "hotel_name": "Test Hotel",
            "check_in_date": "2025-10-11",
            "rating": 5,
            "title": "Updated title",
            "comment": "Updated comment",
            "image_url": "https://example.com/new-image.jpg",
            "suggested_theme": "Romantic"
        }
        
        response = client.post(
            "/api/review/updateReview",
            json=update_data,
            headers=self.get_auth_headers()
        )
        
        assert response.status_code == 200
        response_data = json.loads(response.text)
        assert response_data["message"] == "Review updated successfully"
        assert response_data["data"]["rating"] == 5
        assert response_data["data"]["title"] == "Updated title"
        assert response_data["data"]["comment"] == "Updated comment"

    def test_update_review_partial_update(self, client):
        """
        GIVEN an existing review
        WHEN updating only some fields
        THEN should update only the specified fields
        """
        # Create initial review
        review = Review.createReview(
            customer=self.test_user,
            package=self.test_package,
            booking=self.test_booking,
            rating=3,
            title="Original title",
            comment="Original comment"
        )
        
        # Update only rating
        update_data = {
            "hotel_name": "Test Hotel",
            "check_in_date": "2025-10-11",
            "rating": 5
        }
        
        response = client.post(
            "/api/review/updateReview",
            json=update_data,
            headers=self.get_auth_headers()
        )
        
        assert response.status_code == 200
        response_data = json.loads(response.text)
        assert response_data["data"]["rating"] == 5
        assert response_data["data"]["title"] == "Original title"
        assert response_data["data"]["comment"] == "Original comment"

    def test_update_review_not_found(self, client):
        """
        GIVEN no existing review for the booking
        WHEN trying to update a review
        THEN should return 404 Not Found
        """
        update_data = {
            "hotel_name": "Test Hotel",
            "check_in_date": "2025-10-11",
            "new_rating": 5,
            "new_title": "Updated title"
        }
        
        response = client.post(
            "/api/review/updateReview",
            json=update_data,
            headers=self.get_auth_headers()
        )
        
        assert response.status_code == 404
        response_data = json.loads(response.text)
        assert "Review not found for this booking" in response_data["error"]

    def test_delete_review_success(self, client):
        """
        GIVEN an existing review
        WHEN deleting the review
        THEN should delete the review successfully
        """
        # Create review
        review = Review.createReview(
            customer=self.test_user,
            package=self.test_package,
            booking=self.test_booking,
            rating=4,
            title="Review to delete",
            comment="This will be deleted"
        )
        
        delete_data = {
            "hotel_name": "Test Hotel",
            "check_in_date": "2025-10-11"
        }
        
        response = client.post(
            "/api/review/deleteReview",
            json=delete_data,
            headers=self.get_auth_headers()
        )
        
        assert response.status_code == 200
        response_data = json.loads(response.text)
        assert response_data["message"] == "Review deleted successfully"
        
        # Verify review is actually deleted
        deleted_review = Review.objects(booking=self.test_booking).first()
        assert deleted_review is None

    def test_delete_review_not_found(self, client):
        """
        GIVEN no existing review for the booking
        WHEN trying to delete a review
        THEN should return 404 Not Found
        """
        delete_data = {
            "hotel_name": "Test Hotel",
            "check_in_date": "2025-10-11"
        }
        
        response = client.post(
            "/api/review/deleteReview",
            json=delete_data,
            headers=self.get_auth_headers()
        )
        
        assert response.status_code == 404
        response_data = json.loads(response.text)
        assert "Review not found for this booking" in response_data["error"]

    def test_delete_review_unauthorized(self, client):
        """
        GIVEN no authentication token
        WHEN trying to delete a review
        THEN should return 401 Unauthorized
        """
        delete_data = {
            "hotel_name": "Test Hotel",
            "check_in_date": "2025-10-11"
        }
        
        response = client.post("/api/review/deleteReview", json=delete_data)
        
        assert response.status_code == 401