from flask import Flask, request , session, redirect, url_for, escape , Response
from flask import render_template 
import sqlite3
import os
import setting
import hashlib
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        blogpath = "./blog"
        if os.path.exists(blogpath) == True:
            subprocess.call(['git pull'], shell=True)
            return 'OK'
        else:
            subprocess.call(['git clone ' + setting.gitpath], shell=True)
            return 'OK'
    else:
        return render_template('gitload.html')

@app.route('/login/panel')
def loginp():
    if 'username' in session:
        return redirect(url_for('edit'))
    else:
        return render_template('login.html')

@app.route('/root/userpanel' , methods=['GET','POST'])
def add():
    if request.method == "POST":
        username = request.form['useradd']
        dpass = request.form['passdd']
        try:
            print("adduser debug")
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
        return render_template('root/user.html')
        


@app.route('/login' , methods=['GET','POST'])
def login():
    if request.method == "POST":
        user = request.form['buser']
        passd = request.form['bpass']
        print(user)
        try:
            print("debug")
            with sqlite3.connect('../sqlite/0MuMDAU.db') as conn:
                cursor = conn.cursor()
                cursor.execute('select password from user where username=?',[user])
                password = cursor.fetchone() 
        except:
            print("erruser")
            return "帳號錯誤！"
        pathuser  = password[0]
        print(pathuser)
        hashsha =  hashlib.sha256(passd.replace('\n','').encode())
        if pathuser == hashsha.hexdigest():
            session['username'] = user
            return redirect(url_for('edit'))
        else:
            print("err pass")
            return "密碼錯誤"
    else:
        return "想try我後台？你怎摸不去吃大便"


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/edit')
def edit(username=None):
    if 'username' in session:
        return render_template('redit.html', username = session['username'])


@app.route('/save' , methods=['GET','POST'])
def save():
    if request.method == "POST":
        argment = request.form['content']
        fil =  request.form['title']
        import datetime
        now = datetime.datetime.now()
        filen = now.strftime("%Y-%m-%d")+"-"+fil

        if not fil.strip():
            return "打標題啦,e04!"
        else:
            f = open('_posts/'+ filen  +'.markdown', 'wb+') 
            f.write(argment.encode('UTF-8'))
            f.close()
            ans = "file open"
            return "文章已經存在本地的_posts,重新整理即可在佇列中看到"

@app.route('/submit' , methods=['GET','POST'])
def submit():
    if request.method == "POST":
        argment = request.form['content']
        fil = request.form['title']
        import datetime
        now = datetime.datetime.now()
        filen = now.strftime("%Y-%m-%d")+"-"+fil 
        if not fil.strip():
            return "打檔名拉,e04"
        else:
            user = request.form['username']
            passd = request.form['password']
            pathuser = "../pskey/" + user
            hashsha =  hashlib.sha256(passd.replace('\n','').encode())
            if os.path.exists(pathuser) == True :
                with open( pathuser ,'r' ) as f:
                    fline = f.readline()
                    if fline.replace('\n' , '')  == hashsha.hexdigest() :
                        f = open('_posted/'+ filen  +'.markdown', 'wb+') 
                        f.write(argment.encode('UTF-8'))
                        f.close()
                        ans = "file open"
                        import shutil
                        shutil.copyfile('_posted/' + filen +'.markdown','blog/_posts/' + filen +'.markdown')
                        message = 'add new posts' + filen
                        subprocess.call(['cd blog | git add . | git commit -m' + message], shell=True)
                        subprocess.call(['bash ./script/autoAuth.sh ' + user + ' ' + passd + ' ./blog'], shell=True)
                        return "文章已經存在本地的_posted,文章即將發布.." 
                    else:
                        return "密碼錯誤是要登入三小"
            else:
                return "帳號錯誤是要登入三小"
        
@app.route('/getmd/<listmd>', methods=['GET','POST'])
def markdownr(listmd):
    if request.method == "POST":
        f = open('_posts/' + listmd)
        return f.read()
    else:
        return "你怎摸不去吃大便"

@app.route('/getmdposted/<listposed>', methods=['GET','POST'])
def markdownrp(listposed):
    if request.method == "POST":
        f = open('blog/_posts/'+ listposed)
        return f.read()
    else:
        return "在try我的後台嘛？你怎摸不去吃大便"

@app.route('/jsonlist/<lists>')
def jsonlist(lists):
    if 'username' in session:
        if lists == "posts" :
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
            return(resp)
        else:
            os.makedirs(postpath)
        return 'OK'
    else:
        return 'Eat Shit Please!'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/update')
def update():
    shutdown_server()
    return "server updateing"


app.secret_key = 'aoksp=f^=qrt%%%___jrfw'
if __name__ == '__main__':
    app.run()
