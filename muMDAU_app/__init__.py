# -*- coding: utf-8 -*-
# muMDAU_app init file 
# some debug code of server like update/restart code
from flask import Flask, request, session, redirect, url_for
from flask import render_template 

app = Flask(__name__)

import subprocess
import muMDAU_app.login 
import muMDAU_app.logout 
import muMDAU_app.panel

# private function - runtime error to catch restart
def restart_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
# private function - subprocess run git pull
def gitpull():
    subprocess.call(['git pull'], shell=True)
# private function - debug only pkill pypy3
def pkill_server():
    subprocess.call(['pkill pypy3'], shell=True)

# muMDAU_app: do server update and restart
@app.route('/update')
def update():
    if 'username' in session:
        gitpull()
        restart_server()
        return render_template('wait.html')
    else:
        return redirect(url_for('loginp'))

# muMDAU_app: do restart without update
@app.route('/restart')
def restart():
    if 'username' in session:
        restart_server()
        return render_template('wait.html')
    else:
        return redirect(url_for('loginp'))

# muMDAU_app: **debug** shutdown_server
@app.route('/shutdown')
def shutdown_server():
    if muMDAU_app.setting.debug == 1:
        if 'username' in session:
            pkill_server()
            return 'server go to shutdown'
        else:
            return redirect(url_for('loginp'))
    else:
        return 'debug mode is disable , please use restart function'
