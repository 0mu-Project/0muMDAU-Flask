from muMDAU_app import app 
import logging,setting

app.secret_key = 'aoksp=f^=qrt%%%___jrfw'
from werkzeug.contrib.fixers import ProxyFix 
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    logging.basicConfig(filename='../server.log',level=logging.DEBUG)
    print("0MuMDAU Server Run on 127.0.0.1:" + str(setting.port))
    app.run(host="127.0.0.1",port=setting.port)

