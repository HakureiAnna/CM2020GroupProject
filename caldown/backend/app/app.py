from flask import Flask, request, jsonify, abort
import hashlib
import mysql.connector as mc
import os
from string import punctuation
from time import sleep

from util import *

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

#############################################
# test use
@app.route('/users', methods=['GET'])
def getUsers():
    return jsonify([
            {
                'firstName': 'John',
                'lastName': 'Smith'
            },
            {
                'firstName': 'Jane',
                'lastName': 'Smith'
            }
        ]        
    )

# test use
#############################################

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'user' not in data:
        return abort(400)
    if 'pass' not in data:
        return abort(400)
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
    auth_hdr = request.headers.get('Authorization', None)
    if auth_hdr is None:
        return abort(401)
    uid = checkUser(conn, auth_hdr)
    if not uid:
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
    return jsonify({'message':'logged off successfully'})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if 'user' not in data:
        return abort(400)
    if 'pass' not in data:
        return abort(400)
    user = data['user']
    pw = data['pass']

    # check conditions
    # user name valid
    userValid = len(user) >= 8
    userValid &= user[0].isalpha()
    # password valid
    passValid = len(pw) >= 12
    passValid &= any(ch.isdigit() for ch in pw) and any(ch.isalpha() for ch in pw) and any(p in pw for p in punctuation)
    if not userValid or not passValid:
        return abort(400)

    pw = hashlib.sha256(pw.encode()).hexdigest()
    with conn.cursor() as c:
        q = 'SELECT id FROM users WHERE username=%s'
        args = (user,)
        c.execute(q, args)
        retVal = c.fetchall()
        if len(retVal) != 0:
            retVal = {
                'message': 'user already exists'
            }
            return jsonify(retVal)
        q = 'INSERT INTO users(id, username, password, status) VALUES (%s, %s, %s, %s)'
        args = (createUUID(), user, pw, '0')
        c.execute(q, args)
        q = 'SELECT id FROM users WHERE username=%s'
        args = (user,)
        c.execute(q, args)
        retVal = c.fetchall()
        uid = retVal[0][0]
    retVal = {
        'token': createToken(uid)
    }
    return jsonify(retVal)

@app.route('/deactivate', methods=['POST'])
def deactivate():
    auth_hdr = request.headers.get('Authorization', None)
    if auth_hdr is None:
        return abort(401)
    data = request.get_json()
    if 'user' not in data:
        return abort(400)
    if 'pass' not in data:
        return abort(400)
    user = data['user']
    pw = data['pass']

    uid = checkUser(conn, auth_hdr)
    if not uid:
        return abort(401)

    with conn.cursor() as c:
        q = 'DELETE FROM users WHERE id=%s AND username=%s and password=%s'
        args = (uid, user, pw)
        try:
            c.execute(q, args)
        except:
            return abort(401)
    
    return jsonify({
        'message': 'user account deactivated permanently'
    })       

@app.route('/profile', methods=['GET', 'POST'])
def profile():    
    auth_hdr = request.headers.get('Authorization', None)
    if auth_hdr is None:
        return abort(401)
    uid = checkUser(conn, auth_hdr)
    if not uid:
        return abort(401)
        
    if request.method == 'GET':
        return getProfile(conn, uid)
    else:                
        data = request.get_json()
        # weight, height, gender, age
        weight = data['weight']
        height = data['height']
        gender = data['gender']
        age = data['age']
        goal = data['goal']
        if weight is None or height is None or gender is None or age is None or goal is None:
            return abort(400)
        try:
            weight = int(weight)            
            height = int(height)
            gender = int(gender)
            age = int(age)
        except:
            return abort(400)

        if weight < 40:
            return abort(400)
        if height < 120:
            return abort(400)
        if gender < 0 or gender > 1:
            return abort(400)
        if age < 16 or age > 110:
            return abort(400)
        if len(goal) < 1:
            return abort(400)
            
        args = {
            'weight': weight,
            'height': height,
            'gender': gender,
            'age': age,
            'goal': goal
        }
        return postProfile(conn, uid, args)

@app.route('/recommendations', method=['POST'])
def getRecommendations():
    auth_hdr = request.headers.get('Authorization', None)
    if auth_hdr is None:
        return abort(401)
    uid = checkUser(conn, auth_hdr)

    data = request.get_json()
    mealType = data['type']
    keyword = data['keyword']
    if mealType is None or keyword is None:
        return abort(400)

    if mealType == 'Breakfast':
        factor = 0.35
    elif mealType == 'Lunch':
        factor = 0.4
    else mealType == 'Dinner':
        factor = 0.25

    profile = getProfileFromDb(conn, uid)
    # Revised Harris-Benedict Equation
    if profile['gender'] == 0:
        calories = 9.247*profile['weight'] + 309.8*profile['height'] -4.330*profile['age'] + 447.593
    else:
        calories = 13.397*profile['weight'] + 479.9*profile['height'] -5.677*profile['age'] + 88.362
    calories = int(factor * calories)

    with open('./secrets/secret', 'r') as f:
        lines = f.readlines()
        app_id = lines[0].split('=')[-1]
        app_key = lines[1].split('=')[-1]

    uri = 'https://api.edamam.com/api/recipes/v2?type=public'
    uri += 'q=' + keyword
    uri += '&app_id=' + app_id
    uri += '&app_key=' + app_key
    uri += '&diet=balanced'
    uri += '&mealType=' + mealType
    uri += '&calories=' + '{:d}'.format(calories)
    uri += '&field=uri&field=image&field=calories'

    return jsonify({
        'uri': uri
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
