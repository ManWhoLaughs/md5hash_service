from hashlib import md5
from flask_mail import Message, Mail
from rq import get_current_job, Queue
from app import app, mail
import requests
import os
import sqlite3

def run_sql(query):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    connection.commit()
    connection.close()
    return res

# I use streaming download with 4Kb chunks,
# in case of someone decide to hash full Game of Thrones in Blu-ray
def md5_sum(f):
    hash_md5 = md5()
    for chunk in f.iter_content(4096):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()

def send_email(result, url, status, email):
    try:
        with app.app_context():
            msg = Message(
                str({ "md5" : result, "url" : url, "status" : status}),
                sender = "veryveryuniquemail@gmail.com",
                recipients = [email]
                )
            mail.send(msg)
        return True
    except:
        return False

def failed(url, email, token, step):
    if (step == "Download"):
        run_sql("INSERT INTO tasks VALUES (\"%s\", \"\", \"%s\", -1);" % (token, url))
    elif (step == "Hash"):
        run_sql("UPDATE tasks SET md5 = \"\", status = -1 WHERE id = \"%s\";" % token)
    if (email != None):
        send_email("None", url, "%s error" % step, email)
    return

def run_task(url, email):
    token = get_current_job().id
    f = 0
    try:
        f = requests.get(url, stream=True)
        assert(f.status_code == 200)
    except:
        failed(url, email, token, "Download")
        return "Download error"

    run_sql("INSERT INTO tasks VALUES (\"%s\", \"\", \"%s\", 0);" % (token, url))
    result = ""
    try:
        result = md5_sum(f)
    except:
        failed(url, email, token, "Hash")
        return "Hash error"
    run_sql("UPDATE tasks SET md5 = \"%s\", status = 1 WHERE id = \"%s\";" % (result, token))
    status = "Done"
    if (email != None and send_email(result, url, status, email) == False):
        status = "Email sending error: %s" % email
    return status

