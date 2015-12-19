from muMDAU_app import app
from flask import request , session , render_template  
import sqlite3 
import setting
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
            return render_template('login.html')

@app.route('/panel/server', methods=['GET','POST'])
def maintance():
    if request.method == "GET" :
        if 'username' in session:
            f = open(setting.s_log)
            return render_template('log.html',log = f.read())
        else: 
            return render_template('login.html')
