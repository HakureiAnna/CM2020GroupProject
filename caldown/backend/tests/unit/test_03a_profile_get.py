from datetime import datetime, timedelta, timezone
import json
import jwt
import mysql.connector as mc
import requests

def test_profile_get_invalid_method():    
    url = 'https://localhost/api/profile'
    retVal = requests.put(url, 
            verify=False).status_code
    assert retVal == 405

def test_profile_get_no_credentials():
    url = 'https://localhost/api/profile'
    retVal = requests.get(url,
        verify=False).status_code
    assert retVal == 401

def test_profile_get_invalid_credentials():
    url = 'https://localhost/api/profile'
    headers = {
        'Authorization': 'Bearer test123'
    }
    retVal = requests.get(url,
        verify=False,
        headers=headers).status_code
    assert retVal == 401

def test_profile_get_expired_credentials():
    # login to get valid token
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }    
    retVal = requests.post(url, 
            verify=False,
            json=data).json()

    # extract subject and create token with expired date
    sub = jwt.decode(retVal['token'], 'p@ssw0rd123', algorithms=['HS256'])['sub']    
    now = datetime.now(tz=timezone.utc)
    expiry = now + timedelta(seconds=-30)
    tok = jwt.encode({
        'iat': now,
        'exp': expiry,
        'sub': sub
    }, 'p@ssw0rd123')

    # try endpoint with expired token
    url = 'https://localhost/api/profile'
    headers = {
        'Authorization': 'Bearer ' + tok
    }
    retVal = requests.get(url,
        verify=False,
        headers=headers).status_code
    assert retVal == 401


def test_profile_get_valid_credentials():    
    # login for valid token
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }
    retVal = requests.post(url, 
            verify=False,
            json=data).json()

    # call endpoint with valid token
    url = 'https://localhost/api/profile'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    retVal = requests.get(
        url,
        verify=False,
        headers=headers
    ).json()
    assert retVal['gender'] == 'male'
