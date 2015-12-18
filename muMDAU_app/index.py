from muMDAU_app import app , setting
from flask import request , render_template , Blueprint
import subprocess , os

main = Blueprint('main',__name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        blogpath = "./blog"
        if os.path.exists(blogpath) == True:
            subprocess.call(['git pull'], shell=True , cwd='./blog')
            return 'OK'
        else:
            subprocess.call(['git clone ' + setting.gitpath], cwd='./',shell=True)
            print("clone")
            return 'OK clone'
    else:
        return render_template('gitload.html')
