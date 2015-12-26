#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setting
import sys
import os 
import socket
import subprocess
from database import InitDB
def checkenvir():
    if sys.version_info[0] == 3:
        is_pypy = '__pypy__' in sys.builtin_module_names
        if is_pypy == True:
            try:
                import flask
                return "pypy3"
            except ImportError:
                print("環境檢測中...")
                print("您的電腦沒有flask請輸入密碼自動安裝")
                subprocess.call(['sudo pypy3 -m pip install Flask'],shell=True)
                return "pypy3"
        else:
            try:
                import flask
                return "python3"
            except ImportError:
                print("環境檢測中...")
                print("您的電腦沒有flask請輸入密碼自動安裝")
                subprocess.call(['sudo python3 -m pip install Flask'],shell=True)
                return "python3"
    else:
        print("Fuck U Python2")
        exit()
                

def rungitpull():
    subprocess.call(['git pull'], shell=True)

def importapp():
    subprocess.call([checkenvir() + ' MDAUServer.py'], shell=True)

def portcheck(port):
    s = socket.socket()
    s.settimeout(0.5)
    try:
         return s.connect_ex(('localhost', port)) != 0
    finally:
        s.close()

def preDB():
    InitDB.createTable()

if __name__ == "__main__":
    while 1:
        if portcheck(setting.port) == True:
            if os.path.exists("_posted") == True :
                importapp()
            else:
                os.makedirs("_posted")
