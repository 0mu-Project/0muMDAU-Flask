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


class ManageSQL:
    def addUser(user,password,admin):
        try:
            with sqlite3.connect(sets.sqliteFile) as conn:
                cursor = conn.cursor('INSERT INTO user (username,password,admin) VALUES (?,?,?)',user,password,admin)
                cursor.execute()
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

