from flask import Flask, request, jsonify, abort
import hashlib
import mysql.connector as mc
import os
import requests
from string import punctuation
from time import sleep
from datetime import datetime, date

from util import *

# this code sets up a connection to the MySQL database using
# environment variables injected by docker
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

# create an instance of Flask application
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

# BE1: /login
@app.route('/login', methods=['POST'])
def login():
    # get request data and parse them
    data = request.get_json()
    if 'user' not in data:
        return abort(400)
    if 'pass' not in data:
        return abort(400)
    user = data['user']
    pw = data['pass']

    # hash password
    pw = hashlib.sha256(pw.encode()).hexdigest()

    with conn.cursor() as c:
        # check if user with matching username and password exist        
        q = 'SELECT id FROM users WHERE username=%s AND password=%s'
        args = (user, pw)
        c.execute(q, args)
        retVal = c.fetchall()

        # if not found return error status
        if len(retVal) == 0:
            return abort(401)
        uid = retVal[0][0]

        # change matching user status to 'logged in'
        q = 'UPDATE users SET status=1 WHERE id=%s'
        args = (uid,)
        c.execute(q, args)    
        conn.commit()

    # return a new valid JWT token
    retVal = {
        'token': createToken(uid)
    }
    return jsonify(retVal)

# BE2: /logout
@app.route('/logout', methods=['POST'])
def logout():
    # get token from headers and validate it
    auth_hdr = request.headers.get('Authorization', None)
    if auth_hdr is None:
        return abort(401)
    uid = checkUser(conn, auth_hdr)
    if not uid:
        return abort(401)        

    with conn.cursor() as c:
        # get matching user from DB
        q = 'SELECT status FROM users WHERE id=%s'
        args = (uid,)
        c.execute(q, args)
        retVal = c.fetchall()
        if len(retVal) != 1:
            return abort(401)
        if retVal[0][0] == 1:
            # change matching user's status to 'logged out'
            q = 'UPDATE users SET status=0 WHERE id=%s'
            c.execute(q, args)
            conn.commit()

    # return success log out message
    return jsonify({'message':'logged off successfully'})

# BE5: /signup
@app.route('/signup', methods=['POST'])
def signup():
    # extract, parse and validate arguments
    data = request.get_json()
    if 'user' not in data:
        return abort(400)
    if 'pass' not in data:
        return abort(400)
    user = data['user']
    pw = data['pass']

    # check criteria for new user account
    # validate username
    userValid = len(user) >= 8
    userValid &= user[0].isalpha()
    # validate password
    passValid = len(pw) >= 12
    passValid &= any(ch.isdigit() for ch in pw) and any(ch.isalpha() for ch in pw) and any(p in pw for p in punctuation)
    # return error if validation fails
    if not userValid or not passValid:
        return abort(400)

    # hash password
    pw = hashlib.sha256(pw.encode()).hexdigest()
    with conn.cursor() as c:
        # check if user with matching username already exist
        q = 'SELECT id FROM users WHERE username=%s'
        args = (user,)
        c.execute(q, args)
        retVal = c.fetchall()
        # return messsage when username already exists
        if len(retVal) != 0:
            retVal = {
                'message': 'user already exists'
            }
            return jsonify(retVal)

        # insert new user if username does not exist in DB
        q = 'INSERT INTO users(id, username, password, status) VALUES (%s, %s, %s, %s)'
        args = (createUUID(), user, pw, '0')
        c.execute(q, args)
        conn.commit()
        q = 'SELECT id FROM users WHERE username=%s'
        args = (user,)
        c.execute(q, args)
        retVal = c.fetchall()
        uid = retVal[0][0]
    
    # create new JWT token and return to requestor
    retVal = {
        'token': createToken(uid)
    }
    return jsonify(retVal)

# BE8: /deactivate
@app.route('/deactivate', methods=['POST'])
def deactivate():
    # extract and validate token from header
    auth_hdr = request.headers.get('Authorization', None)
    if auth_hdr is None:
        return abort(401)

    # extract, parse, and validate data from body
    data = request.get_json()
    if 'user' not in data:
        return abort(400)
    if 'pass' not in data:
        return abort(400)
    user = data['user']
    pw = data['pass']
    pw = hashlib.sha256(pw.encode()).hexdigest()

    uid = checkUser(conn, auth_hdr)
    if not uid:
        return abort(401)

    with conn.cursor() as c:
        # delete user from DB ONLY if both a valid token and the username and password
        # matches record in the database, and due to the way the related tables are set up
        # (cascading delete through foreign keys), the user is effectively purged from the
        # from all relevant tables
        q = 'DELETE FROM users WHERE id=%s AND username=%s and password=%s'
        args = (uid, user, pw)        
        try:
            c.execute(q, args)
            conn.commit()
        except:
            return abort(401)
    
    # return success deactivation message
    return jsonify({
        'message': 'user account deactivated permanently'
    })       

# BE3: /profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():    
    # get token from headers and validation
    auth_hdr = request.headers.get('Authorization', None)
    if auth_hdr is None:
        return abort(401)
    uid = checkUser(conn, auth_hdr)
    if not uid:
        return abort(401)
        
    # call utility function to handle for GET method
    if request.method == 'GET':
        return getProfile(conn, uid)
    
    # otherwise call utility function to handle for POST method
    else:              
        data = request.get_json()
        return postProfile(conn, uid, data)

# BE6: /recommendations
@app.route('/recommendations', methods=['GET'])
def recommendations():
    # extract and validate token from header
    auth_hdr = request.headers.get('Authorization', None)
    if auth_hdr is None:
        return abort(401)
    uid = checkUser(conn, auth_hdr)
    if not uid:
        return abort(401)

    # extract, prase and validate data
    data = request.args
    if 'type' not in data:
        return abort(400)
    if 'keyword' not in data:
        return abort(400)

    mealType = data['type']
    keyword = data['keyword']
    if mealType is None or keyword is None:
        return abort(400)

    # determine calories factor based on mealType
    if mealType == 'Breakfast':
        factor = 0.35
    elif mealType == 'Lunch':
        factor = 0.4
    elif mealType == 'Dinner':
        factor = 0.25
    else:
        return abort(400)

    # get latest profile matching the currently loggedin user using utility function
    profile = getProfileFromDb(conn, uid)

    # compute the allowed daily calories based on user's gender
    # Revised Harris-Benedict Equation
    if profile['gender'] == 'female':
        calories = 9.247*profile['weight'] + 309.8*profile['height'] -4.330*profile['age'] + 447.593
    else:
        calories = 13.397*profile['weight'] + 479.9*profile['height'] -5.677*profile['age'] + 88.362

    # compute calories allowed for the mealType using the daily calories limit and meal type factor
    calories = int(factor * calories)

    # obtain Edamam credentials from secret file injected by Jenkins CI/CD pipeline
    with open('secret', 'r') as f:
        lines = f.readlines()
        app_id = lines[0].split('=')[-1].strip()
        app_key = lines[1].split('=')[-1].strip()

    # construct recipe search API query using user provided data and computed calories
    uri = 'https://api.edamam.com/api/recipes/v2?type=public'
    uri += '&q=' + keyword
    uri += '&app_id=' + app_id
    uri += '&app_key=' + app_key
    uri += '&diet=' + profile['goal']
    uri += '&mealType=' + mealType
    uri += '&calories=' + '{:d}'.format(calories)
    uri += '&field=uri&field=image&field=calories&field=label'

    # get recipe recommendation by calling Edamam API
    data = requests.get(uri).json()
    results = data['hits']
    recipes = []

    # format the returned values as a list of recipes that can be handled by the front end
    for r in results:
        recipe = r['recipe']
        recipes.append({
            'uri': recipe['uri'],
            'image': recipe['image'],
            'calories': recipe['calories'],
            'name': recipe['label']
        })

    # turn dict into JSON and return to requestor
    return jsonify({
        'recipes': recipes
    })

# BE4: /plan
@app.route('/plan', methods=['POST', 'GET'])
def plan():
    # extract token from header and validate it
    auth_hdr = request.headers.get('Authorization', None)
    if auth_hdr is None:
        return abort(401)
    uid = checkUser(conn, auth_hdr)
    if not uid:
        return abort(401)

    # call GET utility handler when request uses GET method 
    if request.method == 'GET':
        return getPlan(conn, uid, request.args)
    # call POST utility handler when request uses POST method
    else:
        return postPlan(conn, uid, request.get_json())
 
# BE7: /history
@app.route('/history', methods=['GET'])
def history():
    # extract and validate token from header
    auth_hdr = request.headers.get('Authorization', None)
    if auth_hdr is None:
        return abort(401)
    uid = checkUser(conn, auth_hdr)

    # extract, parse and validate data from params
    startDate = request.args['startDate']
    endDate = request.args['endDate']
    try:
        tmp = datetime.strptime(startDate, '%Y/%m/%d').date()
        startDate = tmp.strftime('%Y-%m-%d')
        tmp = datetime.strptime(endDate, '%Y/%m/%d').date()
        endDate = tmp.strftime('%Y-%m-%d')
    except:
        return abort(400)

    # if endDate is earlier than startDate return error status
    if endDate < startDate:
        return abort(400)

    # get all profiles and plans in the specified period and format as a dict
    result = {
        'profiles': [],
        'plans': []
    }

    with conn.cursor() as c:
        # get relevant profiles from DB
        q = 'SELECT goal, weight, DATE_FORMAT(dateCreated, "%Y/%m/%d") FROM profiles WHERE userid=%s AND datecreated BETWEEN %s AND %s ORDER BY datecreated'
        args = (uid, startDate, endDate)
        c.execute(q, args)
        retVal = c.fetchall()
        for p in retVal:
            result['profiles'].append({
                'goal': p[0],
                'weight': p[1],
                'dateCreated': p[2]
            })

        # get relevant meal plans from DB
        q = 'SELECT id, DATE_FORMAT(dateplanned, "%Y/%m/%d"), breakfast_calories+lunch_calories+dinner_calories FROM plans WHERE userid=%s AND dateplanned BETWEEN %s AND %s ORDER BY dateplanned'
        args = (uid, startDate, endDate)
        c.execute(q, args)
        retVal = c.fetchall()
        for p in retVal:
            result['plans'].append({
                'planId': p[0],
                'plannedDate': p[1],
                'calories': p[2]
            })

    # format dict as JSON and return to requestor
    return jsonify(result)

# start the Flask app running
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
