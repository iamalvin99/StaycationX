from flask import jsonify, request, Blueprint
from app.utils.api_auth import api_auth
from app.utils.api_review import ReviewAPI

api_review = Blueprint('api_review', __name__)

@api_review.route('/api/review/createReview', methods=['POST'])
@api_auth.login_required
def createReview():
    try:
        data = request.json
        if data:
            pass  # Data already in JSON format
        else:  # Fallback to form data
            data = request.form.to_dict()
    except Exception as e:
        return jsonify({"error": "Invalid data format"}), 400

    success, response_data, status_code = ReviewAPI.create_review(data)
    return jsonify(response_data), status_code

@api_review.route('/api/review/getAllReviews', methods=['POST'])
@api_auth.login_required
def getAllReviews():
    success, response_data, status_code = ReviewAPI.get_all_reviews()
    return jsonify(response_data), status_code

@api_review.route('/api/review/getReviewByBooking', methods=['POST'])
@api_auth.login_required
def getReviewByBooking():
    try:
        data = request.json
        if data:
            pass  # Data already in JSON format
        else:  # Fallback to form data
            data = request.form.to_dict()
    except Exception as e:
        return jsonify({"error": "Invalid data format"}), 400

    success, response_data, status_code = ReviewAPI.get_review_by_booking(data)
    return jsonify(response_data), status_code

@api_review.route('/api/review/updateReview', methods=['POST'])
@api_auth.login_required
def updateReview():
    try:
        data = request.json
        if data:
            pass  # Data already in JSON format
        else:  # Fallback to form data
            data = request.form.to_dict()
    except Exception as e:
        return jsonify({"error": "Invalid data format"}), 400

    success, response_data, status_code = ReviewAPI.update_review(data)
    return jsonify(response_data), status_code

@api_review.route('/api/review/deleteReview', methods=['POST'])
@api_auth.login_required
def deleteReview():
    try:
        data = request.json
        if data:
            pass  # Data already in JSON format
        else:  # Fallback to form data
            data = request.form.to_dict()
    except Exception as e:
        return jsonify({"error": "Invalid data format"}), 400

    success, response_data, status_code = ReviewAPI.delete_review(data)
    return jsonify(response_data), status_code