from muMDAU_app import app
from flask import request , session , render_template , url_for 
import sqlite3 
import setting
import os
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
            return redirect(url_for('loginp'))

@app.route('/panel/server', methods=['GET','POST'])
def maintance():
    if request.method == "GET" :
        if 'username' in session:
            f = open(setting.s_log)
            return render_template('log.html',log = f.read())
        else: 
            return redirect(url_for('loginp'))

@app.route('/panel/rmlog', methods=['GET','POST'])
def rmlog():
    if request.method == "GET" :
        if 'username' in session:
            os.remove(setting.s_log)
            return redirect(url_for('panel'))
        else: 
            return redirect(url_for('loginp'))

