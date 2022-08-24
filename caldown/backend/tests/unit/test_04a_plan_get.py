from datetime import datetime, timedelta, timezone, date
import json
import jwt
import mysql.connector as mc
import requests

def test_plan_get_no_credentials():
    url = 'https://localhost/api/plan'
        
    retVal = requests.get(url,
        verify=False).status_code
    assert retVal == 401

def test_plan_get_expired_credentials():
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
    
    # access endpoint with expired token
    url = 'https://localhost/api/plan'
    headers = {
        'Authorization': 'Bearer ' + tok
    }
    retVal = requests.get(url,
        verify=False,
        headers=headers).status_code
    assert retVal == 401

def test_plan_get_missing_data(): 
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
    
    retVal = requests.get(url,
        verify=False,
        headers=headers).status_code
    assert retVal == 400

def test_plan_get_invalid_data():
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
    url = 'https://localhost/api/plan'
    params = 'planId=007'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    retVal = requests.get(url + '?' + params,
        verify=False,
        headers=headers,).status_code
    assert retVal == 400


def test_plan_get_valid_data():  
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

    # insert new plan with valid token
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

    # get inserted plan id through history endpoint
    url = 'https://localhost/api/history'        
    d = date.today()
    d1 = d - timedelta(days=7)
    d2 = d + timedelta(days=7)
    d1 = d1.strftime('%Y/%m/%d')
    d2 = d2.strftime('%Y/%m/%d')
    params = 'startDate=' + d1 + '&endDate=' + d2
    retVal = requests.get(url + '?' + params,
        verify=False,
        headers=headers
    ).json()
    planId = retVal['plans'][0]['planId']

    # get inserted plan through plan GET endpoint
    url = 'https://localhost/api/plan'
    params = 'planId=' + planId
    retVal = requests.get(url + '?' + params,
        verify=False,
        headers=headers
    ).json()

    assert retVal['breakfast'] is not None
