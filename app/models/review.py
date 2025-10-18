from app.models.users import User
from app.models.package import Package
from app.models.book import Booking
from mongoengine.queryset.visitor import Q
from app.extensions import db
from datetime import datetime

class Review(db.Document):

    meta = {'collection': 'reviews'}
    customer = db.ReferenceField(User, required=True)
    package = db.ReferenceField(Package, required=True)
    booking = db.ReferenceField(Booking) 
    rating = db.IntField(min_value=1, max_value=5, required=True)
    title = db.StringField(max_length=100)
    comment = db.StringField(max_length=1000)
    date = db.DateTimeField(default=datetime.utcnow)
    suggested_theme = db.StringField(max_length=100)
    image_url = db.StringField(max_length=1000)
    
    @staticmethod
    def getAllReviews():
        """Get all reviews from the database"""
        return Review.objects()
    
    @staticmethod
    def getReviewByPackage(package):
        """Get all reviews by package"""
        package = Package.getPackage(package)
        if package:
            return Review.objects(package=package)
        return []
    
    @staticmethod
    def getPackageAverageRating(package):
        """Get the average rating of a package"""
        reviews = Review.getReviewByPackage(package)
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    @staticmethod
    def getReviewsByCustomer(customer):
        """Get all reviews by customer"""
        customer = User.getUser(customer)
        if customer:
            return Review.objects(customer=customer)
        return []
    
        @staticmethod
    def getReview(customer, package):
        """Get a specific review by customer and package"""
        return Review.objects(Q(customer=customer) & Q(package=package)).first()

    @staticmethod
    def createReview(customer, package, booking, rating, title, comment):
        """Create and save a new review"""
        if Review.verify_review(Review(customer=customer, booking=booking, package=package)) is None:
            raise ValueError("Customer has not booked this package.")

        new_review = Review(
            customer=customer,
            package=package,
            booking=booking,
            rating=rating,
            title=title,
            comment=comment
        )
        new_review.save()
        return new_review

    @staticmethod
    def updateReview(customer, package, new_date, new_rating, new_comment, new_image_url, new_suggested_theme, new_title ):
        """Update a review"""
        review = Review.getReview(customer, package)
        if review:
            review.date = new_date
            review.rating = new_rating
            review.title = new_title
            review.comment = new_comment
            review.image_url = new_image_url
            review.suggested_theme = new_suggested_theme
            review.save()
            return review
        return None
    
    @staticmethod
    def deleteReview(customer, package):
        """Delete a review"""
        review = Review.getReview(customer, package)
        if review:
            review.delete()
            return True
        return False

    @staticmethod
    def verify_review(self):
        """Check if the reviewer has actually booked this package"""
        booking_exists = Booking.objects(Q(customer=self.customer) & Q(package=self.package)).first()
        return booking_exists
    
    # For the API branch to return JSON data
    @staticmethod
    def dereferenceReview(review):
        return {
            'date': review.date,
            'customer': review.customer.email,
            'package': review.package.hotel_name,
            'rating': review.rating,
            'title': review.title,
            'comment': review.comment,
            'image_url': review.image_url,
            'suggested_theme': review.suggested_theme
        }
    
    @staticmethod
    def dereferenceReviews(reviews):
        return [Review.dereferenceReview(review) for review in reviews]
    