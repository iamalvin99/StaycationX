from flask import jsonify, request, Blueprint
from bson import json_util
import json

# Import the models
from app.models.users import User
from app.models.package import Package
from app.models.book import Booking

from app.utils.api import extract_keys
from app.utils.api_auth import api_auth, generate_user_token

api = Blueprint('api', __name__)

# The API route to get a token
@api.route('/api/user/gettoken', methods=['POST'])
def api_gettoken():
    if request.method == 'POST': 
        # Prioritize JSON data
        data = request.json
        if data:
            email = data.get('email')
            password = data.get('password')
        else:  # Fallback to form data
            email = request.form.get('email')
            password = request.form.get('password')
            
        if not email or not password:
            return jsonify({'error': 'You have to enter a valid email address and valid password'}), 400


        success, token, error_message = generate_user_token(email, password)
        
        if not success:
            if "not registered" in error_message:
                return jsonify({'error': error_message}), 404
            elif "Authentication failed" in error_message:
                return jsonify({'error': error_message}), 401
            else:
                return jsonify({'error': error_message}), 400
        
        return jsonify({'token': token}), 200

# The API route to get all packages  
@api.route('/api/package/getAllPackages', methods=['POST'])
@api_auth.login_required
def getAllPackages():
    print("getAllPackages endpoint accessed")
    allPackages = Package.getAllPackages()
    packages_list = [json.loads(json_util.dumps(package.to_mongo())) for package in allPackages]
    projected_list = [extract_keys(k, idx+1) for idx, k in enumerate(packages_list)]
    return jsonify({'data': projected_list}), 201

# The API route to get all packages  
@api.route('/api/book/newBooking', methods=['POST'])
@api_auth.login_required
def newBooking():
    try:
        # Prioritize JSON data
        data = request.json
        if data:
            check_in_date = data.get("check_in_date")
            user_email = data.get("user_email")
            hotel_name = data.get("hotel_name")
        else:  # Fallback to form data
            check_in_date = request.form.get("check_in_date")
            user_email = request.form.get("user_email")
            hotel_name = request.form.get("hotel_name")
    except Exception as e:
        return jsonify({"error": "Invalid data format"}), 400  # Bad Request

    # Process booking data (replace with your booking logic)
    # This is a placeholder, implement your booking logic here
    if check_in_date == '' or user_email == '' or hotel_name == '':
        return jsonify({"error": "Invalid data format"}), 400

    print(f"Booking received for: {user_email}, Hotel: {hotel_name}, Check-in: {check_in_date}")
    # You would typically save this data to a database or process the booking

    booking_user = User.getUser(email=user_email)
    booking_package = Package.getPackage(hotel_name=hotel_name)
    aBooking = Booking.createBooking(check_in_date, booking_user, booking_package) 

    return jsonify({"message": "Booking created successfully"}), 201  # Created

# The API route to manage bookings 
@api.route('/api/book/manageBooking', methods=['POST'])
@api_auth.login_required
def manageBooking():
    try:
        # Prioritize JSON data
        data = request.json
        if data:
            user_email = data.get("user_email")
        else:  # Fallback to form data
            user_email = request.form.get("user_email")
    except Exception as e:
        return jsonify({f"error": "No booking under {user_email}"}), 400  # Bad Request
    
    booking_user = User.getUser(email=user_email)
    allBookings = Booking.getUserBookingsFromDate(booking_user, '1900-01-01')
    sorted_data_desc = sorted(allBookings, key=lambda d: d['check_in_date'], reverse=True)
    dereferenced_data = Booking.dereferenceBookings(sorted_data_desc)

    return jsonify({"message": "Booking retrieved successfully",
                    "data": dereferenced_data}), 201  # retrieved

# The API route to update a booking
@api.route('/api/book/updateBooking', methods=['POST'])
@api_auth.login_required
def updateBooking():
    try:
        # Prioritize JSON data
        data = request.json
        if data:
            user_email = data.get("user_email")
            new_check_in_date = data.get("new_check_in_date")
            old_check_in_date = data.get("old_check_in_date")
            hotel_name = data.get("hotel_name")
        else:  # Fallback to form data
            user_email = request.form.get("user_email")
            new_check_in_date = request.form.get("new_check_in_date")
            old_check_in_date = request.form.get("old_check_in_date")
            hotel_name = request.form.get("hotel_name")
    except Exception as e:
        return jsonify({f"error": "No booking under {user_email}, {old_check_in_date} and {hotel_name}"}), 400  # Bad Request
    
    customer = User.getUser(email=user_email)
    if Booking.updateBooking(old_check_in_date, new_check_in_date, customer, hotel_name):
        return jsonify({"message": "Booking updated successfully"}), 201  # retrieved
    else:
        return jsonify({"message": "Booking update failed"}), 400

# The API route to delete a booking
@api.route('/api/book/deleteBooking', methods=['POST'])
@api_auth.login_required
def deleteBooking():
    try:
        # Prioritize JSON data
        data = request.json
        if data:
            user_email = data.get("user_email")
            check_in_date = data.get("check_in_date")
            hotel_name = data.get("hotel_name")
        else:  # Fallback to form data
            user_email = request.form.get("user_email")
            check_in_date = request.form.get("check_in_date")
            hotel_name = request.form.get("hotel_name")
    except Exception as e:
        return jsonify({f"error": "No booking under {user_email}, {check_in_date} and {hotel_name}"}), 400  # Bad Request
    
    customer = User.getUser(email=user_email)

    if Booking.deleteBooking(check_in_date, customer, hotel_name):
        return jsonify({"message": "Booking delete successfully"}), 201  # retrieved
    else:
        return jsonify({"message": "Booking deletion failed"}), 400

# Protected route for authorized users
@api.route('/api/protected')
@api_auth.login_required
def protected():
    return jsonify({'message': 'You are authorized to see this message'}), 201