from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify, abort
import hashlib
import jwt
import mysql.connector as mc
import os
from time import sleep

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
    with conn.cursor() as c:
        q = 'SELECT COUNT(*) FROM users WHERE id == %s'
        args = (data['sub'])
        c.execute(q, args)
        retVal = c.fetchall()
        return len(retVal) == 1
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

@app.route('/login', methods=['POST'])
def login():
    user = request.form['user']
    pw = request.form['pass']
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
    return createToken(uid)

@app.route('/logoff', methods=['POST'])
def logoff():
    tok = request.form['tok']
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
        return abort(501)
    else:
        return abort(501)
