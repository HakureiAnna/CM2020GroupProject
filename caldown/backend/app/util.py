from datetime import datetime, timedelta, timezone
from flask import jsonify, abort
import jwt
import os
import uuid

def createUUID():
    return str(uuid.uuid4())

def getProfile(conn, uid):
    with conn.cursor() as c:
        q = 'SELECT weight, height, gender, age uid FROM profiles WHERE userid=%s ORDER BY datecreated DESC LIMIT 1'
        args = (uid,)
        c.execute(q, args)
        retVal = c.fetchall()
        if len(retVal) != 1:
            return abort(400)
        retVal = {
            'weight': retVal[0][0],
            'height': retVal[0][1],
            'gender': retVal[0][2],
            'age': retVal[0][3],
            'uid': retVal[0][4]
        }
    return jsonify(retVal)
    
def postProfile(conn, uid, args):
    with conn.cursor() as c:
        q = 'INSERT INTO profiles (id, userid, weight, height, gender, age) VALUES(%s, %s, %s, %s, %s, %s)'
        args = (str(uuid.uuid4()), uid, args['weight'], args['height'], args['gender'], args['age'])
        c.execute(q, args)
        try:
            conn.commit()
        except:
            abort(500)
    return jsonify({
        'message': 'profile created/ updated successfully'
    })        

def createToken(sub):
    delta = int(os.environ['JWT_DELTA'])
    secret = os.environ['JWT_SECRET']
    now = datetime.now(tz=timezone.utc)
    expiry = now + timedelta(seconds=delta)
    return jwt.encode({
        'iat': now,
        'exp': expiry,
        'sub': sub
    }, secret)

def checkToken(token):
    secret = os.environ['JWT_SECRET']
    try:
        return jwt.decode(token, secret, algorithms=['HS256'])['sub']
    except:
        return None
    
def checkUser(conn, token):
    token = token.replace('Bearer ', '')
    uid = checkToken(token)
    if uid is None:
        return False
    
    with conn.cursor() as c:
        q = 'SELECT COUNT(*) FROM users WHERE id = %s'
        args = (uid,)
        c.execute(q, args)
        retVal = c.fetchall()
        if retVal[0][0] == 1:
            return uid
    return False