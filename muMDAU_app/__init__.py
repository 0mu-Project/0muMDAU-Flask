from flask import Flask, request , session
from flask import render_template 
import sqlite3
app = Flask(__name__)

import muMDAU_app.setting 
import muMDAU_app.index 
import muMDAU_app.login 
import muMDAU_app.logout 
import muMDAU_app.editor

@app.route('/panel' , methods=['GET','POST'])
def panel():
    if request.method == "POST":
        username = request.form['useradd']
        dpass = request.form['passdd']
        try:
            with sqlite3.connect('../sqlite/0MuMDAU.db') as conn:
                cursor = conn.cursor()
                cursor.execute('select COUNT() as "Resault" from user where username = ?', [username])
                answer = cursor.fetchone
                if answer == 1 :
                    return "去吃大便"
                else:
                    return "Create!"
        except:
            print("dd")
    else:
        if 'username' in session:
            return render_template('panel.html', username = session['username'])
        else:
            return "EAT SHIT!"

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/update')
def update():
    if 'username' in session:
        shutdown_server()
        return "server updateing"
    else:
        return "eat shit"


