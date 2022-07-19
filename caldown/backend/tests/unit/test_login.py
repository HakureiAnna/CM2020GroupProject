import json
import jwt
import mysql.connector as mc
import requests

def test_login_no_data():
    url = 'https://localhost/api/login'
    retVal = requests.post(url,
        verify=False).status_code
    assert retVal == 400

def test_login_missing_data():
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser'
    }
    retVal = requests.post(url,
        verify=False,
        json=data).status_code
    assert retVal == 400


def test_login_invalid_credentials():
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'test123'
    }
    retVal = requests.post(url,
        verify=False,
        json=data).status_code
    assert retVal == 401


def test_login_valid_credentials():    
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }
    retVal = requests.post(url, 
            verify=False,
            json=data).json()
    sub = jwt.decode(retVal['token'], 'p@ssw0rd123', algorithms=['HS256'])['sub']
    assert len(sub) == 36

def test_login_already_logged_in():
    
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }
    # log in
    requests.post(url, 
            verify=False,
            json=data)
    # log in aggain
    retVal = requests.post(url, 
            verify=False,
            json=data).json()
    assert retVal['message'] == 'already logged in'
