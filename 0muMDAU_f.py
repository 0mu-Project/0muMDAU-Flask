from flask import Flask, request , session, redirect, url_for, escape , Response
from flask import render_template
import git 
import os
import setting
import hashlib

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        blogpath = "./blog"
        if os.path.exists(blogpath) == True: 
            g = git.cmd.Git()
            g.pull()
            return redirect(url_for('loginp'))
        else:
            git.Git().clone(setting.gitpath)
            return redirect(url_for('loginp'))
    else:
        return render_template('gitload.html')

@app.route('/login/panel')
def loginp():
    if 'username' in session:
        print("data1")
        print(session['username'])
        return redirect(url_for('edit'))
    else:
        return render_template('login.html')

@app.route('/login' , methods=['GET','POST'])
def login():
    if request.method == "POST":
        user = request.form['buser']
        passd = request.form['bpass']
        print(user)
        pathuser  = "../pskey/" + user
        hashsha =  hashlib.sha256(passd.replace('\n','').encode())
        if os.path.exists(pathuser) == True :
            with open(pathuser , 'r') as f :
                fline = f.readline()
                if fline.replace('\n','') == hashsha.hexdigest():
                    session['username'] = user
                    return redirect(url_for('edit'))
@app.route('/edit')
def edit():
    if 'username' in session:
        return render_template('redit.html')

@app.route('/jsonlist/<list>')
def jsonlist(list):
    if list == "posts" :
        postpath = "_posts"
    else:
        postpath = "blog/_posts"
    
    if os.path.exists(postpath) == True:
        directory = os.path.expanduser(postpath)
        data = []
        i = 0
        for f in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, f)):
                i = i + 1
                data.insert(i,f)
            import json
            jsondump = json.dumps(data,separators=( ',' , ':'))
            resp = Response(response=jsondump,status=200, mimetype="application/json")
    else:
        os.makedirs(postpath)
        resp =""
    return(resp)


app.secret_key = 'aoksp=f^=qrt%%%___jrfw'
if __name__ == '__main__':
    app.run(debug=True)
