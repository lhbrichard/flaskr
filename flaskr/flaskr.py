# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 17:31:25 2017

@author: richard
"""

import sqlite3
from contextlib import closing
from flask import Flask,request,session,g,redirect,url_for,\
     abort,render_template,flash
import pyodbc

#DATABASE='/tmp/flaskr.db'
DEBUG=True
SECRET_KEY='development key'
USERNAME='richard'
PASSWORD='richard'

app=Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS',silent=True)
conn_info=('Driver={MySQL ODBC 5.3 Unicode Driver};Server=%s;Port=%s;Database=%s;User=%s;\
           Password=%s;Option=3;'%('localhost',3306,'richard','root','123456'))
mysqlconn=pyodbc.connect(conn_info)
mysqlcur=mysqlconn.cursor()
#date=mysqlcur.execute('select date from table2').fetchall()

@app.route('/')
def show_entries():
    cur=mysqlcur.execute('select date,positive_number from table2')
    entries=[dict(date=row[0].strftime('%Y-%m-%d'),num=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html',entries=entries)

@app.route('/add',methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    mysqlcur.execute('insert into table2(date,positive_number) values (?,?)',\
                     [request.form['date'],request.form['num']])
    mysqlcur.commit()
    flash('New entry wa successfully posted')
    return redirect(url_for('show_entriesd'))
    
@app.route('/login',methods=['GET','POST'])
def login():
    error=None
    if request.method=='POST':
        if request.form['username']!=app.config['USERNAME']:
            error='Invalid username'
        elif request.form['password']!=app.config['PASSWORD']:
            error='Invalid password'
        else:
            session['logged_in']=True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html',error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))















'''
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('D:\\Richard\\Work\\Web\\microblog\\flaskr\\schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()
'''

    
if __name__=='__main__':
    app.run()
    
