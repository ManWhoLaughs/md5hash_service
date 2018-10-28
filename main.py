from flask import Flask, request, abort
import sqlite3
import requests
import os
from hashlib import md5
from redis import Redis
from rq import Queue, get_current_job
from flask_mail import Message

app = Flask(__name__,  static_url_path='/static')

redis_con = Redis()
queue = Queue(connection=redis_con)

def init_db():
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    for cmd in open("init-db.sql").read().split('\n\n'):
        cursor.execute(cmd)
    connection.commit()
    connection.close()

def run_sql(query):
    connection = sqlite3.connect("users.db")
    print(os.getcwd())
    cursor = connection.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    connection.close()
    return res

@app.route('/')
def main_page():
    return 'Hello, World!'

@app.route('/check/<str:task_id>', methods=['GET'])
def get_task(task_id):
    task = run_sql("SELECT * FROM tasks WHERE id = %s;" % task_id)
    if (len(task) == 0):
        return jsonify({ "status" : "not exist" })
    elif task[0][3] == 0:
        return jsonify({ "status" : "running" })
    elif task[0][3] == -1:
        return jsonify({ "status" : "error" })
    return jsonify({"md5" : task[0][1], "url" : task[0][2], "status" : "done"})


@app.route('/submit', methods=['POST'])
def create_task():
    if not request.json:
        abort(400)
    url = request.args['url']
    email = ""
    if 'email' in request.json:
        email = request.args['email']
    token = queue.enqueue(run_task, url, email)
    return jsonify({ "id" : token.id })

def md5_sum(f):
    hash_md5 = md5()
    for chunk in f.iter_content(4096):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()

def run_task(url, email):
    token = get_current_job().id
    run_sql("INSERT INTO tasks VALUES (\"%s\", \"\", \"%s\", 0);" % token, %url)
    f = requests.get(url, stream=True)
    status = ""
    result = ""
    if f.status_code != 200:
        run_sql("UPDATE tasks SET status = -1 WHERE id = %s;" % token)
        status = "error"
     else:
        result = md5_sum(f)
        run_sql("UPDATE tasks SET md5 = \"%s\", status = 1 WHERE id = %s;" % result, % token)
        status = "done"

    if email != "":
        msg = Message(
            jsonify({ "md5" : result, "url" : url, "status" : status}),
            sender = "admin@coolapp.com",
            recipients = [email]
            )
        mail.send(msg)
    return result

if __name__=='__main__':
    if (os.path.isfile('tasks.db') == False):
        init_db()
    app.run(debug=False)
