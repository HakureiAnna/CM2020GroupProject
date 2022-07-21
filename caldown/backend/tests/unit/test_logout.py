from datetime import datetime, timedelta, timezone
import json
import jwt
import mysql.connector as mc
import requests

def test_logout_invalid_method():    
    url = 'https://localhost/api/logout'
    retVal = requests.get(url, 
            verify=False).status_code
    assert retVal == 405

def test_logout_no_data():
    url = 'https://localhost/api/logout'
    retVal = requests.post(url,
        verify=False).status_code
    assert retVal == 401

def test_logout_invalid_token():
    url = 'https://localhost/api/logout'
    headers = {
        'Authorization': 'Bearer test123'
    }
    retVal = requests.post(url,
        verify=False,
        headers=headers).status_code
    assert retVal == 401

def test_login_expired_token():
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }    
    retVal = requests.post(url, 
            verify=False,
            json=data).json()
    sub = jwt.decode(retVal['token'], 'p@ssw0rd123', algorithms=['HS256'])['sub']    
    now = datetime.now(tz=timezone.utc)
    expiry = now + timedelta(seconds=-30)
    tok = jwt.encode({
        'iat': now,
        'exp': expiry,
        'sub': sub
    }, 'p@ssw0rd123')
    url = 'https://localhost/api/logout'
    headers = {
        'Authorization': 'Bearer ' + tok
    }
    retVal = requests.post(url,
        verify=False,
        headers=headers).status_code
    assert retVal == 401


def test_logout_valid_token():    
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }
    retVal = requests.post(url, 
            verify=False,
            json=data).json()

    url = 'https://localhost/api/logout'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    retVal = requests.post(url,
        verify=False,
        headers=headers).json()
    assert retVal['message'] == 'logged off successfully'
