from datetime import datetime, timedelta, timezone
import json
import jwt
import mysql.connector as mc
import requests

def test_profile_post_missing_credentials():    
    url = 'https://localhost/api/profile'
    data = {
        'weight': 50,
        'height': 160,
        'gender': 0,
        'age': 25
    }
    retVal = requests.post(
        url, 
        verify=False,
        json=data
    ).status_code
    assert retVal == 401

def test_profile_post_missing_data():
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }
    retVal = requests.post(
        url,
        verify=False,
        json=data
    )
    url = 'https://localhost/api/profile'    
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    retVal = requests.post(
        url,
        verify=False,
        headers=headers
    ).status_code
    assert retVal == 400

def test_profile_post_invalid_data():
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }    
    retVal = requests.post(url,
        verify=False,
        headers=headers).status_code

    url = 'https://localhost/api/profile'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    data = {
        'weight': 39,
        'height': 160,
        'gender': 0,
        'age': 25
    }
    retVal = requests.get(url,
        verify=False,
        headers=headers,
        json=data).status_code
    assert retVal == 400

# def test_profile_post_create_new():
#     url = 'https://localhost/api/login'
#     data = {
#         'user': 'testuser',
#         'pass': 'password'
#     }    
#     retVal = requests.post(url, 
#             verify=False,
#             json=data).json()
#     sub = jwt.decode(retVal['token'], 'p@ssw0rd123', algorithms=['HS256'])['sub']    
#     now = datetime.now(tz=timezone.utc)
#     expiry = now + timedelta(seconds=-30)
#     tok = jwt.encode({
#         'iat': now,
#         'exp': expiry,
#         'sub': sub
#     }, 'p@ssw0rd123')
#     url = 'https://localhost/api/profile'
#     headers = {
#         'Authorization': 'Bearer ' + tok
#     }
#     retVal = requests.get(url,
#         verify=False,
#         headers=headers).status_code
#     assert retVal == 401


# def test_profile_post_update_existing():    
#     url = 'https://localhost/api/login'
#     data = {
#         'user': 'testuser',
#         'pass': 'password'
#     }
#     retVal = requests.post(url, 
#             verify=False,
#             json=data).json()

#     url = 'https://localhost/api/profile'
#     headers = {
#         'Authorization': 'Bearer ' + retVal['token']
#     }
#     retVal = requests.get(url,
#         verify=False,
#         headers=headers).json()
#     assert retVal['gender'] == 1
