from datetime import datetime, timedelta, timezone
import json
import jwt
import mysql.connector as mc
import requests

def test_deactivate_invalid_method():    
    url = 'https://localhost/api/deactivate'
    retVal = requests.get(url, 
            verify=False).status_code
    assert retVal == 405

def test_deactivate_no_token():
    url = 'https://localhost/api/deactivate'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }
    retVal = requests.post(url,
        verify=False,
        json=data).status_code
    assert retVal == 401

def test_deactivate_no_data():
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }
    retVal = requests.post(url,
        verify=False,
        json=data).json()
    url = 'https://localhost/api/deactivate'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    retVal = requests.post(url,
        verify=False,
        headers=headers).status_code
    assert retVal == 400

def test_deactivate_missing_data():
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }
    retVal = requests.post(url,
        verify=False,
        json=data).json()
    url = 'https://localhost/api/deactivate'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    data = {
        'user': 'testuser'
    }
    retVal = requests.post(url, 
            verify=False,
            headers=headers,
            json=data).status_code

    assert retVal == 400


def test_deactivate_valid_arguments():  
    url = 'https://localhost/api/signup'
    data = {
        'user': 'testuser1',
        'pass': 'p@ssw0rd!234'
    }
    retVal = requests.post(url,
        verify=False,
        json=data).json()
      
    url = 'https://localhost/api/deactivate'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    data = {
        'user': 'testuser',
        'pass': 'password'
    }
    retVal = requests.post(url, 
            verify=False,
            headers=headers,
            json=data).json()
    assert retVal['message'] == 'user account deactivated permanently'
