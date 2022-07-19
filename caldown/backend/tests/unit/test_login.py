import json
import jwt
import mysql.connector as mc
import requests

def test_login():    
    uid = requests.post(url, verify=False).json()['id']
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }
    retVal = requests.post(url, 
            verify=False,
            json=data).json()
    try:
        sub = jwt.decode(retVal['token'], 'p@ssw0rd123', algorithms=['HS256'])['sub']
    except:
        pass
    assert len(sub) == 36