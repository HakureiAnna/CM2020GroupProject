from datetime import datetime, timedelta, timezone
import json
import jwt
import mysql.connector as mc
import requests

def test_createPlan_invalid_method():  
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
    
    url = 'https://localhost/api/createPlan'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }    
    retVal = requests.get(url, 
            verify=False,
            headers=headers).status_code
    assert retVal == 405

def test_createPlan_no_credentials():
    url = 'https://localhost/api/createPlan'
    data = {
        'breakfast': {
            'uri': 'https://www.google.com',
            'calories': 1000
        },
        'lunch': {
            'uri': 'https://www.google.com',
            'calories': 1000
        },
        'dinner': {
            'uri': 'https://www.google.com',
            'calories': 1000
        },
        'plannedDate': '2022/08/09'
    }
    retVal = requests.post(url,
        verify=False,
        json=data).status_code
    assert retVal == 401

def test_createPlan_missing_data(): 
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

    url = 'https://localhost/api/createPlan'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    data = {
        'breakfast': {
            'uri': 'https://www.google.com',
            'calories': 1000
        },
        'dinner': {
            'uri': 'https://www.google.com',
            'calories': 1000
        },
        'plannedDate': '2022/08/09'
    }
    retVal = requests.post(url,
        verify=False,
        headers=headers,
        json=data).status_code
    assert retVal == 400

def test_createPlan_invalid_data():
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

    url = 'https://localhost/api/createPlan'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    data = {
        'breakfast': {
            'uri': 'https://www.google.com',
            'calories': 1000
        },
        'lunch': {
            'uri': 'https://www.google.com',
            'calories': 1000
        },
        'dinner': {
            'uri': 'https://www.google.com',
            'calories': 1000
        },
        'plannedDate': '2022/07/31'
    }
    retVal = requests.post(url,
        verify=False,
        headers=headers,
        json=data).status_code
    assert retVal == 400


def test_createPlan_valid_data():  
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

    url = 'https://localhost/api/createPlan'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    data = {
        'breakfast': {
            'uri': 'https://www.google.com',
            'calories': 1000
        },
        'lunch': {
            'uri': 'https://www.google.com',
            'calories': 1000
        },
        'dinner': {
            'uri': 'https://www.google.com',
            'calories': 1000
        },
        'plannedDate': '2022/08/09'
    }
    retVal = requests.post(url,
        verify=False,
        headers=headers,
        json=data).json()
    assert retVal['message'] == 'plan successfully created.'
