from flask import Flask, request , session
from flask import render_template 
import sqlite3
app = Flask(__name__)

import subprocess
import setting 
import muMDAU_app.login 
import muMDAU_app.logout 
import muMDAU_app.panel

def restart_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def pkill_server():
    subprocess.call(["pkill pypy3"],shell=True)

@app.route('/update')
def update():
    if 'username' in session:
        restart_server()
        return "server updateing"
    else:
        return "eat shit"

@app.route('/shutdown')
def shutdown_server():
    if muMDAU_app.setting.debug == 1 :
        if 'username' in session:
            pkill_server()
            return "server go to shutdown"
        else:
            return "eat shit"
    else:
        return "eat shit"
        
