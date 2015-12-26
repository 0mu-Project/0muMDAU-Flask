#!/usr/bin/pypy3

import sqlite3
import setting as sets

class InitDB:
    def createTable():
        try:
            with sqlite3.connect(sets.sqliteFile) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE user(username PRIMARY KEY, password, admin)')
                conn.close
                return True
        except:
            conn.close
            return False

class LoginSQL:
    def getPass(user):
        try:
            with sqlite3.connect(sets.sqliteFile) as conn:
                cursor = conn.cursor()
                cursor.execute('select password from user where username=?',[user])
                password = cursor.fetchone()
                conn.close
        except:
            conn.close
            password = False 
        return password

class countUSER:
    def countAdmin():
        try:
            with sqlite3.connect(sets.sqliteFile) as conn:
                cursor = conn.cursor()
                cursor.execute('select count(*) as numers from user where admin = 1')
                usercount = cursor.fetchone()
                conn.close
        except:
            conn.close
            usercount = False 
        return usercount
    def countUser():
        try:
            with sqlite3.connect(sets.sqliteFile) as conn:
                cursor = conn.cursor()
                cursor.execute('select count(*) as numers from user')
                usercount = cursor.fetchone()
                conn.close
        except:
            conn.close
            usercount = False 
        return usercount


class ManageSQL:
    def addUser(user,password,admin):
        try:
            with sqlite3.connect(sets.sqliteFile) as conn:
                values=[(str(user),str(password),int(admin)),]
                conn.executemany('INSERT INTO user VALUES (?,?,?)',values)
                conn.commit()
                conn.close
                return True
        except:
            conn.close
            return False

    def setAdmin(username,admin):
        try:
            with sqlite3.connect(sets.sqliteFile) as conn:
                cursor = conn.cursor('UPDATE user SET admin=? WHERE username=?',admin,username)
                cursor.execute()
                conn.commit()
                conn.close
                return True
        except:
            conn.close
            return False 

    def setPassword(username,password):
        try:
            with sqlite3.connect(sets.sqliteFile) as conn:
                cursor = conn.cursor('UPDATE user SET password=? WHERE username=?',username,username)
                cursor.execute()
                conn.commit()
                conn.close
                return True
        except:
            conn.close
            return False 

