#!/usr/bin/python3 
import setting
import sys
import git 
import socket
import MDAUrun

def rungitpull():
    g = git.cmd.Git("./")
    g.pull()

def importapp():
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
            rungitpull()
            importapp()
