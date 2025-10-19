import json
import base64
import os
from app.models.users import User
from werkzeug.security import generate_password_hash

def test_home_page_post_with_fixture(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is posted to (POST)
    THEN check that a '200' (Success) status code is returned
    """
    
    response = client.get('/')
    assert response.status_code == 200
    assert b"Flask User Management Example!" not in response.data

def test_view_hotel_with_fixture(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is posted to (GET)
    THEN check that a '200' (Success) status code is returned
    """
    response = client.get("/viewPackageDetail/Capella Singapore")
    assert response.status_code == 200
    assert b"Capella Singapore" in response.data

def test_gettoken_and_retrieve_package_with_fixture(client):
    """
    GIVEN a Flask API application configured for testing
    WHEN the '/api/user/gettoken' request path is sent (POST) with authentication information
    THEN if the user is authenticated then a token is returned for the user to query the '/api/package/getAllPackages' request path
    """
    useremail = 'peter@cde.com'
    hashpass = generate_password_hash("12345", method='sha256')
    user = User.createUser(email=useremail, password=hashpass, name="Peter Test")
    
    response = client.post("api/user/gettoken", json={'email': useremail, 'password': '12345'})
    response_data = json.loads(response.text)

    assert response.status_code == 200
    token = response_data['token']
    print(token)
    credentials = base64.b64encode(f"{useremail}:{token}".encode('utf-8')).decode('utf-8')
    headers = {'Authorization': f'Basic {credentials}'}
    response = client.post('api/package/getAllPackages', headers=headers, json={})
    response_data = json.loads(response.text)
    print(response_data)

def test_gettoken_and_new_booking_with_fixture(client):
    """
    GIVEN a Flask API application configured for testing
    WHEN the '/api/user/gettoken' request path is sent (POST) with authentication information
    THEN if the user is authenticated then a token is returned for the user to query the '/api/book/newBooking' request path
    """
    useremail = 'peter@cde.com'
    hashpass = generate_password_hash("12345", method='sha256')
    user = User.createUser(email=useremail, password=hashpass, name="Peter Test")
    
    response = client.post("api/user/gettoken", json={'email': useremail, 'password': '12345'})
    response_data = json.loads(response.text)

    assert response.status_code == 200
    token = response_data['token']
    print(token)
    credentials = base64.b64encode(f"{useremail}:{token}".encode('utf-8')).decode('utf-8')
    data = {
        'check_in_date': '2021-12-12',
        'user_email': useremail,
        'hotel_name': "Shangri-La Singapore",
    }
    headers = {'Authorization': f'Basic {credentials}'}
    response = client.post('api/book/newBooking', headers=headers, json=data)
    response_data = json.loads(response.text)
    print(response_data)

def test_gettoken_and_manage_booking_with_fixture(client):
    """
    GIVEN a Flask API application configured for testing
    WHEN the '/api/user/gettoken' request path is sent (POST) with authentication information
    THEN if the user is authenticated then a token is returned for the user to query the '/api/book/manageBooking' request path
    """
    useremail = 'peter@cde.com'
    hashpass = generate_password_hash("12345", method='sha256')
    user = User.createUser(email=useremail, password=hashpass, name="Peter Test")
    
    response = client.post("api/user/gettoken", json={'email': useremail, 'password': '12345'})
    response_data = json.loads(response.text)

    assert response.status_code == 200
    token = response_data['token']
    print(token)
    credentials = base64.b64encode(f"{useremail}:{token}".encode('utf-8')).decode('utf-8')
    data = {
        'user_email': useremail,
    }
    headers = {'Authorization': f'Basic {credentials}'}
    response = client.post('api/book/manageBooking', headers=headers, json=data)
    response_data = json.loads(response.text)
    print(response_data)
    print(len(response_data['data']))

def test_gettoken_and_update_booking_with_fixture(client):
    """
    GIVEN a Flask API application configured for testing
    WHEN the '/api/user/gettoken' request path is sent (POST) with authentication information
    THEN if the user is authenticated then a token is returned for the user to query the '/api/book/updateBooking' request path
    """
    useremail = 'peter@cde.com'
    hashpass = generate_password_hash("12345", method='sha256')
    user = User.createUser(email=useremail, password=hashpass, name="Peter Test")
    
    response = client.post("api/user/gettoken", json={'email': useremail, 'password': '12345'})
    response_data = json.loads(response.text)

    assert response.status_code == 200
    token = response_data['token']
    print(token)
    credentials = base64.b64encode(f"{useremail}:{token}".encode('utf-8')).decode('utf-8')
    data = {
        'old_check_in_date': '2021-12-12',
        'new_check_in_date': '2021-12-13',
        'user_email': useremail,
        'hotel_name': "Shangri-La Singapore"
    }
    headers = {'Authorization': f'Basic {credentials}'}
    response = client.post('api/book/updateBooking', headers=headers, json=data)
    assert response.status_code == 201
    # print(response.status_code)

def test_gettoken_and_delete_booking_with_fixture(client):
    """
    GIVEN a Flask API application configured for testing
    WHEN the '/api/user/gettoken' request path is sent (POST) with authentication information
    THEN if the user is authenticated then a token is returned for the user to query the '/api/book/deleteBooking' request path
    """
    useremail = 'peter@cde.com'
    hashpass = generate_password_hash("12345", method='sha256')
    user = User.createUser(email=useremail, password=hashpass, name="Peter Test")
    
    response = client.post("api/user/gettoken", json={'email': useremail, 'password': '12345'})
    response_data = json.loads(response.text)

    assert response.status_code == 200
    token = response_data['token']
    print(token)
    credentials = base64.b64encode(f"{useremail}:{token}".encode('utf-8')).decode('utf-8')
    data = {
        'check_in_date': '2021-12-13',
        'user_email': useremail,
        'hotel_name': "Shangri-La Singapore"
    }
    headers = {'Authorization': f'Basic {credentials}'}
    response = client.post('api/book/deleteBooking', headers=headers, json=data)
    assert response.status_code == 201
    # print(response.status_code)