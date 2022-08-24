from datetime import datetime, timedelta, timezone
import json
import jwt
import mysql.connector as mc
import requests

def test_recommendations_invalid_method():  
    # login to get valid token
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }  
    retVal = requests.post(
        url,
        verify=False,
        json=data
    ).json()
    
    # access endpoint with valid token but invalid method
    url = 'https://localhost/api/recommendations'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    retVal = requests.post(url, 
            verify=False,
            headers=headers).status_code
    assert retVal == 405

def test_recommendations_no_credentials():
    # access endpoint with no credentials
    url = 'https://localhost/api/recommendations'
    params = 'mealType=Breakfast&keyword=chicken'
    retVal = requests.get(url + '?' + params,
        verify=False).status_code
    assert retVal == 401

def test_recommendations_missing_data(): 
    # login to get valid token
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }  
    retVal = requests.post(
        url,
        verify=False,
        json=data
    ).json()

    # access endpoint with valid token but missing data
    url = 'https://localhost/api/recommendations'
    params = 'mealType=Breakfast'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    retVal = requests.get(url + '?' + params,
        verify=False,
        headers=headers).status_code
    assert retVal == 400

def test_recommendations_invalid_data():
    # login to get valid token
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }  
    retVal = requests.post(
        url,
        verify=False,
        json=data
    ).json()

    # access endpoint with valid token but invalid data
    url = 'https://localhost/api/recommendations'
    params = 'mealType=Breakfast&keyword=chicken'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    retVal = requests.get(url + '?' + params,
        verify=False,
        headers=headers).status_code
    assert retVal == 400


def test_recommendations_valid_data():  
    # login to get valid token
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }  
    retVal = requests.post(
        url,
        verify=False,
        json=data
    ).json()

    # access endpoint with valid token and data
    url = 'https://localhost/api/recommendations'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    params = 'type=Breakfast&keyword=chicken'
    retVal = requests.get(url + '?' + params,
        verify=False,
        headers=headers
    ).json()
    assert len(retVal['recipes']) > 0
