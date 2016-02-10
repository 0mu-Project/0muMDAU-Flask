#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 0muMDAU Server
from muMDAU_app import app 
import logging, setting
from muMDAU_app.index import main
from muMDAU_app.editor import peditor
from muMDAU_app.editor import markdown
from werkzeug.contrib.fixers import ProxyFix 

# muMDAU_app setting 
app.secret_key = setting.yourkey
app.wsgi_app = ProxyFix(app.wsgi_app)
app.register_blueprint(peditor, url_prefix='/edit')
app.register_blueprint(markdown, url_prefix='/md')
app.register_blueprint(main)

# Main function of MDAUServer
if __name__ == '__main__':
    # log writeing
    logging.basicConfig(filename=setting.s_log, level=logging.DEBUG)
    print('0MuMDAU Server Run on ' + str(setting.host) + ':' + str(setting.port))
    # check debug
    if setting.debug == 0:
        debugB = False 
    else:
        debugB = True
        print('Debug Mode is run!')
    app.run(host=str(setting.host), port=setting.port, debug=debugB)
