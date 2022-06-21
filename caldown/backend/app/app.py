from flask import Flask
import mysql.connector as mc
import os
from time import sleep

sleep(5)

conn = mc.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_DB']
)

app = Flask(__name__)

@app.route('/')
def index():
    q = 'SELECT * FROM users'
    retVal = ''
    with conn.cursor() as c:
        c.execute(q)
        for r in c.fetchall():
            for c in r:
                retVal += '{},'.format(c)
    return retVal