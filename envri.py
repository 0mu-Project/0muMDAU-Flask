#!/usr/bin/python3 
import setting
import sys
import os 
import socket
import subprocess

def rungitpull():
    subprocess.call(['git pull'], shell=True)

def importapp():
    import MDAUrun
    MDAUrun.app.run(host='127.0.0.1', port=setting.port)

def portcheck(port):
    s = socket.socket()
    s.settimeout(0.5)
    try:
         return s.connect_ex(('localhost', port)) != 0
    finally:
        s.close()

if __name__ == "__main__":
    while 1:
        if portcheck(9002) == True:
            if os.path.exists("_posted") == True :
                rungitpull()
                importapp()
            else:
                os.makedirs("_posted")
