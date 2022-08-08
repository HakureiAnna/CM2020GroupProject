from datetime import datetime, date, timedelta, timezone
from flask import jsonify, abort
import jwt
import os
import uuid

def createUUID():
    return str(uuid.uuid4())

def getProfileFromDb(conn, uid):    
    with conn.cursor() as c:
        q = 'SELECT weight, height, gender, age, goal, userid FROM profiles WHERE userid=%s ORDER BY datecreated DESC LIMIT 1'
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
            'goal': retVal[0][4],
            'uid': retVal[0][5]
        }

    return retVal

def getProfile(conn, uid):
    return jsonify(getProfileFromDb(conn, uid))
    
def postProfile(conn, uid, args):
    with conn.cursor() as c:
        q = 'INSERT INTO profiles (id, userid, weight, height, gender, age, goal) VALUES(%s, %s, %s, %s, %s, %s, %s)'
        args = (str(uuid.uuid4()), uid, args['weight'], args['height'], args['gender'], args['age'], args['goal'])
        c.execute(q, args)
        try:
            conn.commit()
        except:
            abort(500)
    return jsonify({
        'message': 'profile created/ updated successfully'
    })        

def parseMeal(meal):
    if 'name' not in meal:
        return False
    if 'uri' not in meal:
        return False
    if 'image' not in meal:
        return False
    if 'calories' not in meal:
        return False
    name = meal['name']
    uri = meal['uri']
    image = meal['image']
    calories = meal['calories']
    if name is None or uri is None or image is None or calories is None:
        return False
    try:
        calories = int(calories)
    except:
        return False
    return {
        'name': name,
        'uri': uri,
        'image': image,
        'calories': calories
    }

def getPlan(conn, uid, data):
    if 'planId' not in data:
        return abort(400)
    planId = data['planId']
    with conn.cursor() as c:
        q = 'SELECT breakfast_name, breakfast_uri, breakfast_image, breakfast_calories, lunch_name, lunch_uri, lunch_image, lunch_calories, dinner_name, dinner_uri, dinner_image, dinner_calories, DATE_FORMAT(dateplanned %Y/%m/%d) FROM plans WHERE userid=%s AND id=%s'
        args = (uid, planId)
        print(args)
        c.execute(q, args)
        retVal = c.fetchall()
    return jsonify({
        'breakfast': {
            'name': retVal[0][0],
            'uri': retVal[0][1],
            'image': retVal[0][2],
            'calories': retVal[0][3]
        },
        'lunch': {
            'name': retVal[0][4],
            'uri': retVal[0][5],
            'image': retVal[0][6],
            'calories': retVal[0][7]
        },
        'dinner': {
            'name': retVal[0][8],
            'uri': retVal[0][9],
            'image': retVal[0][10],
            'calories': retVal[0][11]
        },
        'plannedDate': retVal[0][12]
    })

def postPlan(conn, uid, data):       
    if 'breakfast' not in data:
        return abort(400)        
    if 'lunch' not in data:
        return abort(400)
    if 'dinner' not in data:
        return abort(400)
    if 'plannedDate' not in data:
        return abort(400)

    breakfast = parseMeal(data['breakfast'])
    lunch = parseMeal(data['lunch'])
    dinner = parseMeal(data['dinner'])
    plannedDate = data['plannedDate']
    if not breakfast or not lunch or not dinner or not plannedDate:
        return abort(400)
    try:
        dt = datetime.strptime(plannedDate, '%Y/%m/%d').date()
        today = date.today()
        if dt < today:
            return abort(400)
        plannedDate = dt.strftime('%Y-%m-%d')
    except:
        return abort(400)
    with conn.cursor() as c:
        q = 'INSERT INTO plans(id, breakfast_name, breakfast_uri, breakfast_image, breakfast_calories, lunch_name, lunch_uri, lunch_image, lunch_calories, dinner_name, dinner_uri, dinner_image, dinner_calories, datePlanned, userid) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        args = (createUUID(), breakfast['name'], breakfast['uri'], breakfast['image'], breakfast['calories'], lunch['name'], lunch['uri'], lunch['image'], lunch['calories'], dinner['name'], dinner['uri'], dinner['image'], dinner['calories'], plannedDate, uid)
        try:
            c.execute(q, args)
            conn.commit()
        except:
            return abort(500)
    return jsonify({
        'message': 'plan successfully created.'
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