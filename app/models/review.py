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
    review_date = db.DateTimeField(default=datetime.utcnow)

    @staticmethod
    def verify_review(self):
        """Check if the reviewer has actually booked this package"""
        booking_exists = Booking.objects(Q(customer=self.customer) & Q(package=self.package)).first()
        return booking_exists

    @staticmethod
    def setReview(customer, package, booking, rating, title, comment):
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
    def getReview(customer, package):
        """Get a specific review by customer and package"""
        return Review.objects(Q(customer=customer) & Q(package=package)).first()
