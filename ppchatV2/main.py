from flask import Flask, session, redirect, url_for, escape, request, render_template
from idgen import gen_once 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for("index"))
    html = render_template('main.html.j2' )
    return html

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
        html = render_template('idgen.html.j2', prcid=prcid)
    else:
        html = render_template('idgen.html.j2')
    return html

@app.route('/chatroom')
def chatroom():
    html = render_template('main.html.j2')
    return html

# set the secret key.  keep this really secret:
app.secret_key = b'b\xd1\x10#\xe3\xca\xfd\\A\x10\xffh\xff\xbc\x92\x10<\x92\x11G[*\xa5['
app.permanent_session_lifetime = 3600*24*7

if __name__ == "__main__":
    app.run(host='192.168.0.107')