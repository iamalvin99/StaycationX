from flask import jsonify, request
from app.models.users import User
from app.models.package import Package
from app.models.book import Booking
from app.models.review import Review

class ReviewAPI:
    """Service layer for Review API"""
    
    @staticmethod
    def get_authenticated_user_email():
        """
        Extract the authenticated user's email from the request
        Use this method when creating, updating and deleting a review to prevent a user
        from changing the review of another user.
        """
        try:
            if request.authorization and request.authorization.username:
                return request.authorization.username
        except Exception as e:
            print(f"Error getting authenticated user email: {e}")
            return None
        return None
    
    @staticmethod
    def create_review(data):
        """
        Create a new review
        
        Args:
            data (dict): Review data containing user_email, hotel_name, rating, title, comment, check_in_date
            
        Returns:
            tuple: (success: bool, response_data: dict, status_code: int)
        """
        try:
            user_email = ReviewAPI.get_authenticated_user_email()
            if not user_email:
                return False, {"error": "Authentication required"}, 401
            hotel_name = data.get("hotel_name")
            rating = data.get("rating")
            title = data.get("title")
            comment = data.get("comment")
            check_in_date = data.get("check_in_date")

            # Validate required fields
            if not all([hotel_name, rating, title, comment, check_in_date]):
                return False, {"error": "Missing required fields"}, 400

            # Retrieve the relevant user, package and booking objects to create the review
            customer = User.getUser(email=user_email)
            if not customer:
                return False, {"error": "User not found"}, 404

            package = Package.getPackage(hotel_name=hotel_name)
            if not package:
                return False, {"error": "Package not found"}, 404

            booking = Booking.getBooking(check_in_date, customer, hotel_name)
            if not booking:
                return False, {"error": "Booking not found"}, 404

            # Check if review already exists for this booking
            existing_review = Review.objects(booking=booking).first()
            if existing_review:
                return False, {"error": "Review already exists for this booking"}, 409

            new_review = Review.createReview(
                customer=customer,
                package=package,
                booking=booking,
                rating=int(rating),
                title=title,
                comment=comment
            )

            return True, {
                "message": "Review created successfully",
                "data": Review.dereferenceReview(new_review)
            }, 201

        except ValueError as e:
            return False, {"error": str(e)}, 400
        except Exception as e:
            return False, {"error": "Failed to create review"}, 500

    @staticmethod
    def get_all_reviews():
        """
        Retrieve all reviews
        
        Returns:
            tuple: (success: bool, response_data: dict, status_code: int)
        """
        try:
            all_reviews = Review.getAllReviews()
            dereferenced_reviews = Review.dereferenceReviews(all_reviews)
            
            return True, {
                "message": "Reviews retrieved successfully",
                "data": dereferenced_reviews
            }, 200
        except Exception as e:
            return False, {"error": "Failed to retrieve reviews"}, 500

    @staticmethod
    def get_review_by_booking(data):
        """
        Retrieve a review by specific booking

        Args:
            data (dict): Data containing user_email, hotel_name, check_in_date

        Returns:
            tuple: (success: bool, response_data: dict, status_code: int)
        """
        try:
            user_email = data.get("user_email")
            hotel_name = data.get("hotel_name")
            check_in_date = data.get("check_in_date")

            # Validate required fields
            if not all([user_email, hotel_name, check_in_date]):
                return False, {"error": "Missing required fields"}, 400

            customer = User.getUser(email=user_email)
            if not customer:
                return False, {"error": "User not found"}, 404

            booking = Booking.getBooking(hotel_name=hotel_name, customer=customer, check_in_date=check_in_date)
            if not booking:
                return False, {"error": "Booking not found"}, 404

            review = Review.getReviewByBooking(booking)
            if not review:
                return False, {"error": "Review not found for this booking"}, 404

            return True, {
                "message": "Review retrieved successfully",
                "data": Review.dereferenceReview(review)
            }, 200

        except Exception:
            return False, {"error": "Failed to retrieve review"}, 500

    @staticmethod
    def update_review(data):
        """
        Update a review
        
        Args:
            data (dict): Data containing user_email, hotel_name, check_in_date, and update fields
            
        Returns:
            tuple: (success: bool, response_data: dict, status_code: int)
        """
        try:
            user_email = ReviewAPI.get_authenticated_user_email()
            if not user_email:
                return False, {"error": "Authentication required"}, 401
            hotel_name = data.get("hotel_name")
            check_in_date = data.get("check_in_date")
            new_rating = data.get("rating")
            new_title = data.get("title")
            new_comment = data.get("comment")
            new_image_url = data.get("image_url")
            new_suggested_theme = data.get("suggested_theme")

            # Validate required fields
            if not all([hotel_name, check_in_date]):
                return False, {"error": "Missing required fields"}, 400

            customer = User.getUser(email=user_email)
            if not customer:
                return False, {"error": "User not found"}, 404

            package = Package.getPackage(hotel_name=hotel_name)
            if not package:
                return False, {"error": "Package not found"}, 404

            booking = Booking.getBooking(check_in_date, customer, hotel_name)
            if not booking:
                return False, {"error": "Booking not found"}, 404

            review = Review.getReviewByBooking(booking)
            if not review:
                return False, {"error": "Review not found for this booking"}, 404

            # Perform update
            updated_review = Review.updateReview(
                customer=customer,
                package=package,
                new_date=review.date,  # Check-in date should still remain the same, hence use original date
                new_rating=int(new_rating) if new_rating else review.rating,
                new_comment=new_comment if new_comment else review.comment,
                new_image_url=new_image_url if new_image_url else review.image_url,
                new_suggested_theme=new_suggested_theme if new_suggested_theme else review.suggested_theme,
                new_title=new_title if new_title else review.title
            )

            if updated_review:
                return True, {
                    "message": "Review updated successfully",
                    "data": Review.dereferenceReview(updated_review)
                }, 200
            else:
                return False, {"error": "Failed to update review"}, 500

        except Exception as e:
            return False, {"error": "Failed to update review"}, 500

    @staticmethod
    def delete_review(data):
        """
        Delete a review
        
        Args:
            data (dict): Data containing user_email, hotel_name, check_in_date
            
        Returns:
            tuple: (success: bool, response_data: dict, status_code: int)
        """
        try:
            user_email = ReviewAPI.get_authenticated_user_email()
            if not user_email:
                return False, {"error": "Authentication required"}, 401
            hotel_name = data.get("hotel_name")
            check_in_date = data.get("check_in_date")

            # Validate required fields
            if not all([hotel_name, check_in_date]):
                return False, {"error": "Missing required fields"}, 400

            customer = User.getUser(email=user_email)
            if not customer:
                return False, {"error": "User not found"}, 404

            package = Package.getPackage(hotel_name=hotel_name)
            if not package:
                return False, {"error": "Package not found"}, 404

            booking = Booking.getBooking(check_in_date, customer, hotel_name)
            if not booking:
                return False, {"error": "Booking not found"}, 404

            review = Review.getReviewByBooking(booking)
            if not review:
                return False, {"error": "Review not found for this booking"}, 404

            success = Review.deleteReview(customer=customer, package=package)
            if success:
                return True, {"message": "Review deleted successfully"}, 200
            else:
                return False, {"error": "Failed to delete review"}, 500

        except Exception as e:
            return False, {"error": "Failed to delete review"}, 500