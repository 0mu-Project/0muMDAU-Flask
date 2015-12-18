from muMDAU_app import app 
import logging,setting
from muMDAU_app.index import main
from muMDAU_app.editor import peditor
from muMDAU_app.editor import markdown
app.secret_key = 'aoksp=f^=qrt%%%___jrfw'
from werkzeug.contrib.fixers import ProxyFix 
app.wsgi_app = ProxyFix(app.wsgi_app)
app.register_blueprint(peditor, url_prefix='/edit')
app.register_blueprint(markdown, url_prefix='/md')
app.register_blueprint(main)


if __name__ == "__main__":
    logging.basicConfig(filename=setting.s_log,level=logging.DEBUG)
    print("0MuMDAU Server Run on 127.0.0.1:" + str(setting.port))
    app.run(host="127.0.0.1",port=setting.port)

