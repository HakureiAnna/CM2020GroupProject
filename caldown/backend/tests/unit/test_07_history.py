from datetime import datetime, timedelta, timezone, date
import json
import jwt
import mysql.connector as mc
import requests

def test_history_invalid_method():  
    # login to get valid  token
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
    url = 'https://localhost/api/history'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }    
    d = date.today()
    d1 = d - timedelta(days=7)
    d2 = d + timedelta(days=7)
    d1 = d1.strftime('%Y/%m/%d')
    d2 = d2.strftime('%Y/%m/%d')
    params = 'startDate=' + d1 + '&' + 'endDate=' + d2
    retVal = requests.post(url + '?' + params, 
            verify=False,
            headers=headers).status_code
    assert retVal == 405

def test_history_no_credentials():
    # access endpoint with no credentials
    url = 'https://localhost/api/history'
    d = date.today()
    d1 = d - timedelta(days=7)
    d2 = d + timedelta(days=7)
    d1 = d1.strftime('%Y/%m/%d')
    d2 = d2.strftime('%Y/%m/%d')
    params = 'startDate=' + d1 + '&' + 'endDate=' + d2
    retVal = requests.get(url + '?' + params,
        verify=False).status_code
    assert retVal == 401

def test_history_missing_data(): 
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
    url = 'https://localhost/api/history'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    d = date.today()
    d1 = d - timedelta(days=7)
    d1 = d1.strftime('%Y/%m/%d')
    params = 'startDate=' + d1
    retVal = requests.get(url + '?' + params,
        verify=False,
        headers=headers,
        json=data).status_code
    assert retVal == 400

def test_history_invalid_data():
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
    url = 'https://localhost/api/history'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    d = date.today()
    d1 = d - timedelta(days=7)
    d2 = d + timedelta(days=7)
    d1 = d1.strftime('%Y/%m/%d')
    d2 = d2.strftime('%Y/%m/%d')
    params = 'startDate=' + d2 + '&' + 'endDate=' + d1
    retVal = requests.get(url + '?' + params,
        verify=False,
        headers=headers).status_code
    assert retVal == 400


def test_history_valid_data():  
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

    # insert new plan with valid token and data
    url = 'https://localhost/api/plan'
    d = date.today()
    d += timedelta(days=2)
    d = d.strftime('%Y/%m/%d')
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
        'plannedDate': d
    }
    retVal = requests.post(url,
        verify=False,
        headers=headers,
        json=data).json()

    # access endpoint with valid token and data to retrieve newly inserted plan
    url = 'https://localhost/api/history'    
    d = date.today()
    d1 = d - timedelta(days=7)
    d2 = d + timedelta(days=7)
    d1 = d1.strftime('%Y/%m/%d')
    d2 = d2.strftime('%Y/%m/%d')
    params = 'startDate=' + d1 + '&' + 'endDate=' + d2
    retVal = requests.get(url + '?' + params,
        verify=False,
        headers=headers).json()
    assert len(retVal['plans']) > 0
