from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify, abort
import hashlib
import jwt
import mysql.connector as mc
import os
from time import sleep
import uuid

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
    
def checkUser(token, conn):
    data = checkToken(token)
    if data is None:
        return False
    
    uid = data['sub']
    with conn.cursor() as c:
        q = 'SELECT COUNT(*) FROM users WHERE id = %s'
        args = (uid,)
        c.execute(q, args)
        retVal = c.fetchall()
        if retVal[0][0] == 1:
            return uid
    return False

while True:
    try:
        conn = mc.connect(
            host=os.environ['MYSQL_HOST'],
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            database=os.environ['MYSQL_DB']
        )
        break
    except:
        sleep(10)

app = Flask(__name__)

#####################################
# THIS IS USED FOR ENDPOINT TESTING
# REMOVE IN FINAL VERSION
#####################################
@app.route('/users', methods=['GET'])
def users():
    data = [
        {
            'firstName': 'alice',
            'lastName': 'smith',
        },
        {
            'firstName': 'john',
            'lastName': 'smith'
        }
    ]
    return jsonify(data)
#####################################
        

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = data['user']
    pw = data['pass']
    pw = hashlib.sha256(pw.encode()).hexdigest()
    q = 'SELECT id FROM users WHERE username=%s AND password=%s'
    args = (user, pw)
    with conn.cursor() as c:
        c.execute(q, args)
        retVal = c.fetchall()
        if len(retVal) == 0:
            return abort(401)
        uid = retVal[0][0]
        q = 'UPDATE users SET status=1 WHERE id=%s'
        args = (uid,)
        c.execute(q, args)
    retVal = {
        'token': createToken(uid)
    }
    return jsonify(retVal)

@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    tok = data['token']
    uid = checkToken(tok)
    if uid is None:
        return abort(401)
    with conn.cursor() as c:
        q = 'SELECT status FROM users WHERE id=%s'
        args = (uid,)
        c.execute(q, args)
        retVal = c.fetchall()
        if len(retVal) != 1:
            return abort(401)
        if retVal[0][0] == 1:
            q = 'UPDATE users SET status=0 WHERE id=%s'
            c.execute(q, args)
    return jsonify(message='logged off successfully')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        tok = request.args.get('token')
        uid = checkToken(tok)
        return getProfile(uid)
    else:                
        data = request.get_json()
        tok = data['token']
        uid = checkToken(tok)
        # weight, height, gender, age
        if uid is None:
            return abort(401)
        weight = data['weight']
        height = data['height']
        gender = data['gender']
        age = data['age']
        if weight is None or height is None or gender is None or age is None:
            abort(400)
        try:
            weight = int(weight)
            height = int(height)
            gender = int(gender)
            age = int(age)
        except:
            abort(400)
        args = {
            'weight': weight,
            'height': height,
            'gender': gender,
            'age': age
        }
        return postProfile(uid, args)
    
def getProfile(uid):
    with conn.cursor() as c:
        q = 'SELECT weight, height, gender, age FROM profiles WHERE userid=%s'
        args = (uid,)
        c.execute(q, args)
        retVal = c.fetchall()
        if len(retVal) != 1:
            return abort(400)
        retVal = {
            'weight': retVal[0][0],
            'height': retVal[0][1],
            'gender': retVal[0][2],
            'age': retVal[0][3]
        }
    return jsonify(retVal)

def postProfile(uid, args):
    with conn.cursor() as c:
        q = 'SELECT COUNT(*) FROM profiles WHERE userid=%s'
        sargs = (uid,)
        c.execute(q, sargs)
        retVal = c.fetchall()
        print(retVal)
        if retVal[0][0] == 0:
            q = 'INSERT INTO profiles (id, userid, weight, height, gender, age) VALUES(%s, %s, %s, %s, %s, %s)'
            sargs = (str(uuid.uuid4()), uid, args['weight'], args['height'], args['gender'], args['age'])
            c.execute(q, sargs)
        else:
            q = 'UPDATE profiles SET weight=%s, height=%s, gender=%s, age=%s WHERE userid=%s'
            sargs = (args['weight'], args['height'], args['gender'], args['age'], uid)
            c.execute(q, sargs)
        try:
            conn.commit()
        except:
            abort(500)
    return jsonify({
        'message': 'ok'
    })        
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
