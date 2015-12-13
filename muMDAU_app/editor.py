from muMDAU_app import app
from flask import request , session , Response , render_template
import os , hashlib , subprocess

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
            pathuser = "../../pskey/" + user
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
                        shutil.copyfile('_posted/' + filen +'.markdown','./blog/_posts/' + filen +'.markdown')
                        message = 'add_new_posts_' + filen
                        subprocess.call(['bash ./script/autoAuth.sh ' + user + ' ' + passd + ' ../blog ' + message ], shell=True)
                        return "文章已經存在本地的_posted,文章即將發布.." 
                    else:
                        return "密碼錯誤是要登入三小"
            else:
                return "帳號錯誤是要登入三小"
        
@app.route('/getmd/<listmd>', methods=['GET','POST'])
def markdownr(listmd):
    if request.method == "POST":
        f = open('./_posts/' + listmd)
        return f.read()
    else:
        return "你怎摸不去吃大便"

@app.route('/getmdposted/<listposed>', methods=['GET','POST'])
def markdownrp(listposed):
    if request.method == "POST":
        f = open('./blog/_posts/'+ listposed)
        return f.read()
    else:
        return "在try我的後台嘛？你怎摸不去吃大便"

@app.route('/jsonlist/<lists>')
def jsonlist(lists):
    if 'username' in session:
        if lists == "posts" :
            postpath = "./_posts"
        else:
            postpath = "./blog/_posts"
            
        if os.path.exists(postpath) == True:
            directory = os.path.expanduser(postpath)
            data = []
            i = 0
            if os.listdir(directory) ==None:
                return("[""]")
            else:
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

