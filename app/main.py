from app import app, queue
from flask import Flask, request, abort, jsonify
from rq import Queue
from app.funcs import run_task, run_sql
import requests
import os
import sqlite3

# Just for lulz
@app.route('/')
def main_page():
    return 'Hello, md5-World!'

# Don't doing URL and email validation in the light of
# assumption that app is internal corporate and all channels are trusted
# (and for not to suffer with tons of checks)

@app.route('/check', methods=['GET'])
def get_task():
    task_id = request.args.get('id')
    if (task_id == None):
        abort(400)
    task_info = run_sql("SELECT * FROM tasks WHERE id = \"%s\";" % task_id)
    if (len(task_info) == 0):
        return jsonify({ "status" : "not exist" }), 404
    elif task_info[0][3] == 0:
        return jsonify({ "status" : "running" }), 200
    elif task_info[0][3] == -1:
        return jsonify({ "status" : "error" }), 500
    return jsonify({"md5" : task_info[0][1], "url" : task_info[0][2], "status" : "done"}), 200


@app.route('/submit', methods=['POST'])
def create_task():
    if (len(request.form) == 0):
        abort(400)
    url = request.form.get('url')
    if (url == None):
        abort(400)
    email = request.form.get('email')
    token = queue.enqueue(run_task, url, email)
    return jsonify({ "id" : token.id })

