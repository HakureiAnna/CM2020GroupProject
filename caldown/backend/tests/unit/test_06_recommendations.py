from datetime import datetime, timedelta, timezone
import json
import jwt
import mysql.connector as mc
import requests

def test_recommendations_invalid_method():  
    data = {
        'user': 'testuser',
        'pass': 'password'
    }  
    url = 'https://localhost/api/login'
    retVal = requests.post(
        url,
        verify=False,
        json=data
    ).json()
    
    url = 'https://localhost/api/recommendations'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    retVal = requests.post(url, 
            verify=False,
            headers=headers).status_code
    assert retVal == 405

def test_recommendations_no_credentials():
    url = 'https://localhost/api/recommendations'
    params = 'mealType=Breakfast&keyword=chicken'
    retVal = requests.get(url + '?' + params,
        verify=False).status_code
    assert retVal == 401

def test_recommendations_missing_data(): 
    data = {
        'user': 'testuser',
        'pass': 'password'
    }  
    url = 'https://localhost/api/login'
    retVal = requests.post(
        url,
        verify=False,
        json=data
    ).json()

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
    data = {
        'user': 'testuser',
        'pass': 'password'
    }  
    url = 'https://localhost/api/login'
    retVal = requests.post(
        url,
        verify=False,
        json=data
    ).json()

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
    data = {
        'user': 'testuser',
        'pass': 'password'
    }  
    url = 'https://localhost/api/login'
    retVal = requests.post(
        url,
        verify=False,
        json=data
    ).json()

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
