from muMDAU_app import app , setting
from flask import request , render_template , Blueprint, url_for , redirect
from database import countUSER , ManageSQL
import subprocess , os
from subprocess import PIPE

main = Blueprint('main',__name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        blogpath = "./blog"
        if os.path.exists(blogpath) == True:
            p = subprocess.Popen(['git pull'], shell=True , cwd='./blog',stdout=PIPE)
            outcode , error = p.communicate()
            f = open(setting.s_log,'ab')
            f.write(str.encode('INFO:pull_blog:git -- ') + outcode)
            f.close()
            return 'OK'
        else:
            p = subprocess.Popen(['git clone ' + setting.gitpath], cwd='./',shell=True , stdout = PIPE,stderr=PIPE )
            outcode , gitlog = p.communicate()
            f = open(setting.s_log,'ab')
            f.write(str.encode('INFO:cloneblog:git -- ') + gitlog )
            f.close()
            return 'OK clone'
    else:
        answer = countUSER.countAdmin()
        print(answer)
        if answer[0] == 0 :
            return redirect(url_for('init'))
        else:
            return render_template('gitload.html')

@app.route('/init', methods=['GET', 'POST'])
def init():
    if request.method == 'POST':
        user = request.form['buser']
        passd = request.form['bpass']
        import hashlib
        hashsha = hashlib.sha256(passd.replace('\n','').encode())
        ManageSQL.addUser(user,hashsha.hexdigest(),"1")
        return redirect(url_for('main.index'))
    else:
        return render_template('first.html')
    

