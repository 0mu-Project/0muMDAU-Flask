#!/usr/bin/pypy3 
import muMDAU_app.setting
import sys
import os 
import socket
import subprocess

def rungitpull():
    subprocess.call(['git pull'], shell=True)

def importapp():
    subprocess.call(['pypy3 MDAUServer.py'], shell=True)

def portcheck(port):
    s = socket.socket()
    s.settimeout(0.5)
    try:
         return s.connect_ex(('localhost', port)) != 0
    finally:
        s.close()

if __name__ == "__main__":
    while 1:
        if portcheck(muMDAU_app.setting.port) == True:
            if os.path.exists("_posted") == True :
                rungitpull()
                importapp()
            else:
                os.makedirs("_posted")
