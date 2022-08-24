from datetime import datetime, timedelta, timezone, date
import json
import jwt
import mysql.connector as mc
import requests

def test_plan_post_invalid_method():  
    # login to get valid token
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
    
    # access endpoint with valid token but invalid method
    url = 'https://localhost/api/plan'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }    
    retVal = requests.put(url, 
            verify=False,
            headers=headers).status_code
    assert retVal == 405

def test_plan_post_no_credentials():
    url = 'https://localhost/api/plan'
    data = {
        'breakfast': {
            'name': 'chicken chops',
            'uri': 'https://www.google.com',
            'image': 'https://yahoo.com',
            'calories': 1000
        },
        'lunch': {
            'name': 'chicken chops',
            'uri': 'https://www.google.com',
            'image': 'https://yahoo.com',
            'calories': 1000
        },
        'dinner': {
            'name': 'chicken chops',
            'uri': 'https://www.google.com',
            'image': 'https://yahoo.com',
            'calories': 1000
        },
        'plannedDate': '2022/08/09'
    }
    retVal = requests.post(url,
        verify=False,
        json=data).status_code
    assert retVal == 401

def test_plan_post_missing_data(): 
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
    url = 'https://localhost/api/plan'
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

def test_plan_post_invalid_data():
    # login for valid token
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

    # access endpoint with valid token but with invalid data
    url = 'https://localhost/api/plan'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    data = {
        'breakfast': {
            'name': 'chicken chops',
            'uri': 'https://www.google.com',
            'image': 'https://yahoo.com',
            'calories': 1000
        },
        'lunch': {
            'name': 'chicken chops',
            'uri': 'https://www.google.com',
            'image': 'https://yahoo.com',
            'calories': 1000
        },
        'dinner': {
            'name': 'chicken chops',
            'uri': 'https://www.google.com',
            'image': 'https://yahoo.com',
            'calories': 1000
        },
        'plannedDate': '2022/07/31'
    }
    retVal = requests.post(url,
        verify=False,
        headers=headers,
        json=data).status_code
    assert retVal == 400


def test_plan_post_valid_data():  
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
    url = 'https://localhost/api/plan'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    d = date.today()
    d += timedelta(days=2)
    d = d.strftime('%Y/%m/%d')
    data = {
        'breakfast': {
            'name': 'chicken chops',
            'uri': 'https://www.google.com',
            'image': 'https://yahoo.com',
            'calories': 1000
        },
        'lunch': {
            'name': 'chicken chops',
            'uri': 'https://www.google.com',
            'image': 'https://yahoo.com',
            'calories': 1000
        },
        'dinner': {
            'name': 'chicken chops',
            'uri': 'https://www.google.com',
            'image': 'https://yahoo.com',
            'calories': 1000
        },
        'plannedDate': d
    }
    retVal = requests.post(url,
        verify=False,
        headers=headers,
        json=data).json()
    assert retVal['message'] == 'plan successfully created.'
