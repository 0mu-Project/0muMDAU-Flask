# -*- coding: utf-8 -*-
# muMDAU_app editor main file 
# need to split Blueprint
from flask import request, session, Response, render_template, Blueprint, redirect, url_for
from muMDAU_app import app
import os, hashlib, subprocess
import setting
from subprocess import PIPE
from muMDAU_app.flask_imgur import Imgur

# muMDAU_app_config : imgur upload key
app.config['IMGUR_ID'] = setting.imgurkey
imgur_handler = Imgur(app)

# muMDAU_app_config : Blueprint map
peditor = Blueprint('peditor', __name__)
markdown = Blueprint('markdown', __name__)

# muMDAU_app imgur upload POST page
@app.route('/upload/imgur', methods=['GET', 'POST'])
def imgurupload():
    if request.method == 'POST':
        image = request.files['fileToUpload']
        image_data = imgur_handler.send_image(image)
        return image_data['data']['link'] 

# muMDAU_app del posts use git push page
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
                    # subprocess call bash todo autoauth github
                    subprocess.call(['bash script/autoAuth.sh ' + user + ' ' + passd + ' ./blog ' + message], shell=True)
                    return '文章已刪除..' 
                else:
                    return '密碼錯誤是要登入三小'
        else:
            return '帳號錯誤是要登入三小'
    else:
        return render_template('killfile.html', posts=listmd)

# muMDAU_editor main route page
@peditor.route('/')
def edit(username=None):
    if 'username' in session:
        return render_template('redit.html', username=session['username'])

# muMDAU_editor call list with json post page
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
                resp = '['']'
                for f in os.listdir(directory):
                    if os.path.isfile(os.path.join(directory, f)):
                        i = i + 1
                        data.insert(i, f)
                    import json
                    # transerfer list object to json data and replace ", ;"
                    jsondump = json.dumps(data, separators=(',', ':'))
                    resp = Response(response=jsondump, status=200, mimetype='application/json')
                return(resp)
        else:
            os.makedirs(postpath)
        return 'OK'
    else:
        return redirect(url_for('loginp'))

# muMDAU_markdown save local function route page
@markdown.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        argment = request.form['content']
        fil = request.form['title']
        import datetime
        now = datetime.datetime.now()
        filen = now.strftime('%Y-%m-%d') + '-' + fil

        if not fil.strip():
            return 'please enter title thanks!'
        else:
            f = open('_posts/' + filen + '.markdown', 'wb+') 
            f.write(argment.encode('UTF-8'))
            f.close()
            return 'system (save)'

# muMDAU_markdown submit github function route page
@markdown.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        argment = request.form['content']
        fil = request.form['title']
        import datetime
        now = datetime.datetime.now()
        directory = os.path.expanduser('./blog/_posts/')
        for f in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, f)):
                ldata = f.split('-', 3)
                name = str(ldata[-1]).split('.markdown')
                if str(name[0]) == str(fil):
                    os.remove('./blog/_posts/' + str(f))
        filen = now.strftime('%Y-%m-%d') + '-' + fil 
        if not fil.strip():
            return 'please eneter title thanks'
        else:
            user = request.form['username']
            passd = request.form['password']
            f = open('./blog/_posts/' + filen + '.markdown', 'wb+') 
            f.write(argment.encode('UTF-8'))
            f.close()
            message = 'add_new_posts_' + filen
            # subprocess call bash todo autoauth github
            gitdoit = subprocess.Popen(['bash script/autoAuth.sh ' + user + ' ' + passd + ' ./blog ' + message], shell=True, stdout=PIPE, stderr=PIPE)
            outcode, error = gitdoit.communicate()
            print(outcode)
            return outcode

# muMDAU_markdown open loacl markdown synx 
@markdown.route('/list/<listmd>', methods=['GET', 'POST'])
def markdownr(listmd):
    if request.method == 'POST':
        f = open('./_posts/' + listmd)
        return f.read()
    else:
        return '你怎摸不去吃大便'

# muMDAU_markdown del loacl post without github 
@markdown.route('/del/posts/<listmd>', methods=['GET', 'POST'])
def delposts(listmd):
    if request.method == 'POST':
        filepath = './_posts/' + str(listmd)
        os.remove(filepath)
        return 'OK'
    else:
        return '你怎摸不去吃大便'

# muMDAU_markdown open git branch markdown synx 
@markdown.route('/listed/<listposed>', methods=['GET', 'POST'])
def markdownrp(listposed):
    if request.method == 'POST':
        f = open('./blog/_posts/' + listposed)
        return f.read()
    else:
        return '在try我的後台嘛？你怎摸不去吃大便'
