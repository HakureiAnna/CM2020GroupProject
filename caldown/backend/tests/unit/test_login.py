import json
import requests
import jwt

def test_login():
    url = 'https://localhost/api/login'
    data = {
        'user': 'testuser',
        'pass': 'password'
    }
    retVal = requests.post(url, 
            verify=False,
            json=data).json()
    sub = jwt.decode(retVal['token'], 'p@ssw0rd123', algorithms=['HS256'])['sub']
    assert sub == 'e1fc7bf0-f3c5-11ec-bbd2-0242ac160003'