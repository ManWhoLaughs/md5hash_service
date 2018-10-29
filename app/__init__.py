from flask import Flask
from flask_mail import Mail
from redis import Redis
from rq import Queue
import os
import sqlite3

def init_db():
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    for cmd in open("init-db.sql").read().split('\n\n'):
        cursor.execute(cmd)
    connection.commit()
    connection.close()

app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)

redis_con = Redis()
queue = Queue(connection=redis_con)

from app import main

if (os.path.isfile('tasks.db') == False):
    init_db()
