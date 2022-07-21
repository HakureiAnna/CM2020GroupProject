from datetime import datetime, timedelta, timezone
import json
import jwt
import mysql.connector as mc
import requests

def test_signup_missing_data():    
    url = 'https://localhost/api/signup'
    data = {
        'user': 'haha'
    }
    retVal = requests.get(url, 
            verify=False,
            json=data).status_code
    assert retVal == 400

def test_signup_invalid_username():    
    url = 'https://localhost/api/signup'
    data = {
        'user': '1eeroyjenkins',
        'pass': 'password'
    }
    retVal = requests.post(url,
        verify=False,
        json=data).status_code
    assert retVal == 400

def test_signup_invalid_password():    
    url = 'https://localhost/api/signup'
    headers = {
        'user': 'leeroyjenkins',
        'pass': 'password'
    }
    retVal = requests.post(url,
        verify=False,
        headers=headers,
        json=data).status_code
    assert retVal == 400

def test_signup_existing_user():    
    url = 'https://localhost/api/signup'
    data = {
        'user': 'testuser',
        'pass': 'p@ssw0rd!234'
    }    
    retVal = requests.post(url, 
            verify=False,
            json=data).json()
    assert retVal['message'] == 'user already exists'


def test_signup_new_user():    
    url = 'https://localhost/api/signup'
    data = {
        'user': 'testuser1',
        'pass': 'p@ssw0rd!234'
    }
    retVal = requests.post(url, 
            verify=False,
            json=data).json()            
    assert len(retVal['token'] )== 36