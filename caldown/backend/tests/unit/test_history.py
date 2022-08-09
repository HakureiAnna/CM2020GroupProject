from datetime import datetime, timedelta, timezone, date
import json
import jwt
import mysql.connector as mc
import requests

def test_history_invalid_method():  
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
        headers=headers).json()
    assert len(retVal['plans']) > 0
