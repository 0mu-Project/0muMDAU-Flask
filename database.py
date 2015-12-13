#!/usr/bin/pypy3

import sqlite3
import setting as sets

class LoginSQL:
    def login(user):
        try:
            with sqlite3.connect(sets.sqliteFile) as conn:
                cursor = conn.cursor()
                cursor.execute('select password from user where username=?',[user])
                password = cursor.fetchone()
        except:
            password = False 
        return password
