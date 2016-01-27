# -*- coding: utf-8 -*-

from muMDAU_app import app
from flask import request, session, render_template, url_for, redirect
import setting
import os
@app.route('/panel')
def panel():
    if 'username' in session:
        return render_template('panel.html', username=session['username'])
    else:
        return redirect(url_for('loginp'))

@app.route('/panel/server', methods=['GET', 'POST'])
def maintance():
    if request.method == 'GET':
        if 'username' in session:
            f = open(setting.s_log)
            return render_template('log.html', log=f.read())
        else: 
            return redirect(url_for('loginp'))

@app.route('/panel/rmlog', methods=['GET', 'POST'])
def rmlog():
    if request.method == 'GET':
        if 'username' in session:
            os.remove(setting.s_log)
            open(setting.s_log, 'a').close()
            return redirect(url_for('restart'))
        else: 
            return redirect(url_for('loginp'))

@app.route('/dev/panel')
def mainten():
    if 'username' in session:
        return render_template('maintenancep.html', username=session['username'])
    else:
        return redirect(url_for('loginp'))

@app.route('/user/panel')
def userp():
    if 'username' in session:
        return render_template('userp.html', username=session['username'])
    else:
        return redirect(url_for('loginp'))
