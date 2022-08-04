from datetime import datetime, timedelta, timezone
import json
import jwt
import mysql.connector as mc
import requests

def test_profile_post_missing_credentials():    
    url = 'https://localhost/api/profile'
    data = {
        'weight': 50,
        'height': 160,
        'gender': 0,
        'age': 25
    }
    retVal = requests.post(
        url, 
        verify=False,
        json=data
    ).status_code
    assert retVal == 401

def test_profile_post_missing_data():
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
    url = 'https://localhost/api/profile'    
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    retVal = requests.post(
        url,
        verify=False,
        headers=headers
    ).status_code
    assert retVal == 400

def test_profile_post_invalid_data():
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

    url = 'https://localhost/api/profile'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    data = {
        'weight': 39,
        'height': 160,
        'gender': 0,
        'age': 25,
        'goal': 'balanced'
    }
    retVal = requests.post(
        url,
        verify=False,
        headers=headers,
        json=data
    ).status_code
    assert retVal == 400

def test_profile_post_create_new():
    # sign up for new user
    url = 'https://localhost/api/signup'
    data = {
        'user': 'testuser3',
        'pass': 'p@ssw0rd!234'
    }    
    retVal = requests.post(url, 
            verify=False,
            json=data).json()
            
    # create profile
    url = 'https://localhost/api/profile'  
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }  
    data = {
        'weight': 45,
        'height': 160,
        'gender': 'female',
        'age': 25,
        'goal': 'balanced'
    }
    retVal = requests.post(
        url,
        verify=False,
        headers=headers,
        json=data
    ).json()
    assert retVal['message'] == 'profile created/ updated successfully'

    # check profile exists
    url = 'https://localhost/api/profile'  
    retVal = requests.get(
        url,
        verify=False,
        headers=headers
    ).json()
    
    assert retVal['weight'] == 45

    # deactivate new user
    url = 'https://localhost/api/deactivate'
    data = {
        'user': 'testuser3',
        'pass': 'p@ssw0rd!234'
    }    
    requests.post(
        url,
        verify=False,
        headers=headers,
        json=data
    )

def test_profile_post_update_existing():    
    # log in
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }
    retVal = requests.post(url, 
            verify=False,
            json=data).json()

    # check current profile valid
    url = 'https://localhost/api/profile'
    headers = {
        'Authorization': 'Bearer ' + retVal['token']
    }
    retVal = requests.get(url,
        verify=False,
        headers=headers).json()
    assert retVal['weight'] == 50

    # update profile
    data = {
        'age': retVal['age'],
        'weight': 46,
        'height': retVal['height'],
        'gender': retVal['gender'],
        'userid': retVal['uid'],
        'goal': retVal['goal']
    }
    retVal = requests.post(
        url,
        verify=False,
        headers=headers,
        json=data
    ).json()
    assert retVal['message'] == 'profile created/ updated successfully'

    # check updated profile
    retVal = requests.get(url,
        verify=False,
        headers=headers).json()
    assert retVal['weight'] == 46

