#! /usr/bin/python3
# -*- coding: UTF-8 -*-
from flask import Flask, session, redirect, url_for, escape, request, render_template
from idgen import gen_once 
from chatroom import myMessage

app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('bs-base.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        session['username'] = request.form['inputUsername']
        session['password'] = request.form['inputPassword']
        return redirect(url_for("index"))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/idgen', methods=['GET', 'POST'])
def idgen():
    if request.method == 'POST':
        region_code = request.form.get('region_code')
        region_code = int(region_code) if region_code else None
        date_code = request.form.get('date_code')
        date_code = int(date_code) if date_code else None
        prcid = gen_once(region_code, date_code)
        html = render_template('idgen.html', prcid=prcid)
    else:
        html = render_template('idgen.html')
    return html

@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    if 'username' not in session:
        return render_template('error.html', message="登陆后才能聊天")
    if request.method == 'POST':
        to = request.form.get('to')
        message = request.form.get('message')
        msg = myMessage(session['username'], to, message)
    messages = []
    messages.append(myMessage(session['username'], "system", "Hello, system"))
    messages.append(myMessage("system", session['username'], "Hello, user"))
    html = render_template('chatroom.html', messages=messages)
    return html

# @app.errorhandler(500)
# def page_error(e):
#     return render_template('error.html'), 500

# @app.errorhandler(404)
# def page_error(e):
#     return render_template('error.html', message="404 not found"), 404

# set the secret key.  keep this really secret:
app.secret_key = b'b\xd1\x10#\xe3\xca\xfd\\A\x10\xffh\xff\xbc\x92\x10<\x92\x11G[*\xa5['
app.permanent_session_lifetime = 3600*24*7

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=6778)