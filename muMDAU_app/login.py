from muMDAU_app import app 
from flask import session,redirect,url_for,request,render_template
import sqlite3,hashlib
from database import LoginSQL

@app.route('/login/panel')
def loginp():
    if 'username' in session:
        return redirect(url_for('panel'))
    else:
        return render_template('login.html')


@app.route('/login' , methods=['GET','POST'])
def login():
    if request.method == "POST":
        user = request.form['buser']
        passd = request.form['bpass']

        password = LoginSQL.login(user)

        if password == False:
            return '帳號錯誤'
        else:
            pathuser  = password[0]
            hashsha =  hashlib.sha256(passd.replace('\n','').encode())

            if pathuser == hashsha.hexdigest():
                session['username'] = user
                return redirect(url_for('panel'))
            else:
                return "密碼錯誤"

    else:
        return "想try我後台？你怎摸不去吃大便"

