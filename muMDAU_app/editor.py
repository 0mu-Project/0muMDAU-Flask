# -*- coding: utf-8 -*-

from flask import request, session, Response, render_template, Blueprint, redirect, url_for
from muMDAU_app import app 
import os, hashlib, subprocess
from subprocess import PIPE

peditor = Blueprint('peditor', __name__)
markdown = Blueprint('markdown', __name__)
@peditor.route('/')
def edit(username=None):
    if 'username' in session:
        return render_template('redit.html', username=session['username'])

@markdown.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        argment = request.form['content']
        fil = request.form['title']
        import datetime
        now = datetime.datetime.now()
        filen = now.strftime('%Y-%m-%d') + '-' + fil

        if not fil.strip():
            return '打標題啦,e04!'
        else:
            f = open('_posts/' + filen + '.markdown', 'wb+') 
            f.write(argment.encode('UTF-8'))
            f.close()
            return '文章已經存在本地的_posts,重新整理即可在佇列中看到'

@markdown.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        argment = request.form['content']
        fil = request.form['title']
        import datetime
        now = datetime.datetime.now()
        filen = now.strftime('%Y-%m-%d') + '-' + fil 
        if not fil.strip():
            return '打檔名拉,e04'
        else:
            user = request.form['username']
            passd = request.form['password']
            f = open('_posted/' + filen + '.markdown', 'wb+') 
            f.write(argment.encode('UTF-8'))
            f.close()
            import shutil
            shutil.copyfile('_posted/' + filen + '.markdown', './blog/_posts/' + filen + '.markdown')
            message = 'add_new_posts_' + filen
            gitdoit = subprocess.Popen(['bash script/autoAuth.sh ' + user + ' ' + passd + ' ./blog ' + message], shell=True, stdout=PIPE, stderr=PIPE)
            outcode, error = gitdoit.communicate()
            return outcode

@markdown.route('/list/<listmd>', methods=['GET', 'POST'])
def markdownr(listmd):
    if request.method == 'POST':
        f = open('./_posts/' + listmd)
        return f.read()
    else:
        return '你怎摸不去吃大便'
@app.route('/del/posted/<listmd>', methods=['GET', 'POST'])
def delped(listmd):
    if request.method == 'POST':
        user = request.form['buser']
        passd = request.form['bpass']
        hashsha = hashlib.sha256(passd.replace('\n', '').encode())
        pathuser = '../../pskey/' + user
        if os.path.exists(pathuser):
            with open(pathuser, 'r') as f:
                fline = f.readline()
                if fline.replace('\n', '') == hashsha.hexdigest():
                    filepath = './blog/_posts/' + str(listmd)
                    os.remove(filepath)
                    message = 'del_posts'
                    subprocess.call(['bash script/autoAuth.sh ' + user + ' ' + passd + ' ./blog ' + message], shell=True)
                    return '文章已刪除..' 
                else:
                    return '密碼錯誤是要登入三小'
        else:
            return '帳號錯誤是要登入三小'
    else:
        return render_template('killfile.html', posts=listmd)


@markdown.route('/del/posts/<listmd>', methods=['GET', 'POST'])
def delposts(listmd):
    if request.method == 'POST':
        filepath = './_posts/' + str(listmd)
        os.remove(filepath)
        return 'OK'
    else:
        return '你怎摸不去吃大便'


@markdown.route('/listed/<listposed>', methods=['GET', 'POST'])
def markdownrp(listposed):
    if request.method == 'POST':
        f = open('./blog/_posts/' + listposed)
        return f.read()
    else:
        return '在try我的後台嘛？你怎摸不去吃大便'

@peditor.route('/<lists>')
def jsonlist(lists):
    if 'username' in session:
        if lists == 'posts':
            postpath = './_posts'
        else:
            postpath = './blog/_posts'

        if os.path.exists(postpath):
            directory = os.path.expanduser(postpath)
            data = []
            i = 0
            if os.listdir(directory) is None:
                return('['']')
            else:
                for f in os.listdir(directory):
                    if os.path.isfile(os.path.join(directory, f)):
                        i = i + 1
                        data.insert(i, f)
                    import json
                    jsondump = json.dumps(data, separators=(',', ':'))
                    resp = Response(response=jsondump, status=200, mimetype='application/json')
                return(resp)
        else:
            os.makedirs(postpath)
        return 'OK'
    else:
        return redirect(url_for('loginp'))
