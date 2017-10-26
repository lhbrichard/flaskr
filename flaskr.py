# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 17:31:25 2017

@author: richard
"""

import sqlite3
from contextlib import closing
from flask import Flask,request,session,g,redirect,url_for,\
     abort,render_template,flash,jsonify,json,Blueprint
import pyodbc
import pandas as pd
import urllib.request

#import json

#DATABASE='/tmp/flaskr.db'
#DEBUG=True
#SECRET_KEY='development key'
#USERNAME='richard'
#PASSWORD='richard'

app=Flask(__name__)
app.config.update(dict
                  (SECRET_KEY='development key',
                   USERNAME='richard',
                   PASSWORD='richard'
                          ))
#date=mysqlcur.execute('select date from table2').fetchall()


def table(col_names,entries):
    string='<caption>{{tbname}}</caption><tr>'
    for col in col_names:
        string_seg='<th style="width: 160px;">'+col+'</th>'
        string=string+string_seg
    string=string+'</tr>'
    for entry in entries:
        string=string+'<tr>'
        for col in col_names:
            string=string+'<td>'+entry[col]+'</td>'
        string=string+'</tr>'
    string=string+'</table> '
 
    
    return string
  


@app.route('/',methods=['GET','POST'])
def login():
    error=None
    session['logged_in']=False
    if request.method=='POST':
        if request.form['username']!=app.config['USERNAME']:
            error='用户名不正确!'
        elif request.form['password']!=app.config['PASSWORD']:
            error='密码不正确!'
        else:
            session['logged_in']=True
            flash('登陆成功!')
            return redirect(url_for('select'))
    return render_template('login.html',error=error)

def db():
    conn_info=('Driver={MySQL ODBC 5.3 Unicode Driver};Server=%s;Port=%s;User=%s;\
    Password=%s;Option=3;'%('localhost',3306,'root','123456'))
    mysqlconn=pyodbc.connect(conn_info)
    mysqlcur=mysqlconn.cursor()

    sql_sentence='select schema_name from Information_schema.schemata'                              
    dbname_s=mysqlcur.execute(sql_sentence).fetchall()
    
    dbnames=[]
    for i in range(len(dbname_s)):
        dbnames.append(dbname_s[i][0])

    return dbnames

def tb(dbname):
    conn_info=('Driver={MySQL ODBC 5.3 Unicode Driver};Server=%s;Port=%s;User=%s;\
    Password=%s;Option=3;chartset=utf8;'%('localhost',3306,'root','123456'))
    mysqlconn=pyodbc.connect(conn_info)
    mysqlcur=mysqlconn.cursor()

    sql_sentence='select table_name from Information_schema.tables where table_schema="'+dbname+'"'                              
    tbname_s=mysqlcur.execute(sql_sentence).fetchall()
    
    tbnames=[]
    for i in range(len(tbname_s)):
        tbnames.append(tbname_s[i][0])

    return tbnames

dbnames=db()
dic={}
for i in range(len(dbnames)):
    dic[dbnames[i]]=tb(dbnames[i])


@app.route('/write')
def write(a):
    return jsonify(result=tb(a))


@app.route('/select',methods=['GET','POST'])
#@app.route('/select?dbname=richard',methods=['GET','POST'])
#@app.route('/select?dbname=<dbname>',methods=['GET','POST'])
def select():    
#    dbname=request.args.get("dbname","")
#    if dbname=="":
#        dbname='richard'
#    else:
#        dbname=dbname
#    tbnames=tb(dbname)

    if request.method=='POST':
        #print(1)
        #print(request.form)
        dbname=request.form['dbname']
        #print('i1',dbname)
        tbname=request.form['tbname']
        #print('i0',tbname)
        #print('i2',urllib.request.quote(tbname))
        flash('成功筛选')
        return redirect(url_for('show_entries',dbname=dbname,tbname=tbname))
    return render_template('select.html',dbnames=dbnames,dic=dic)

'''
@app.route('/select',methods=['GET','POST'])
def select():    
    if request.method=='POST':
        dbname=request.form['dbname']
        tbname=request.form['tbname']
        flash('You have already selected')
        return redirect(url_for('show_entries',dbname=dbname,tbname=tbname))
    return render_template('select.html')
'''

#@app.route('/show/<dbname>/<tbname>/user_list',methods=['GET','POST'])
#def user_list():
    


def df(dbname,tbname,limit_start):
    conn_info=('Driver={MySQL ODBC 5.3 Unicode Driver};Server=%s;Port=%s;Database=%s;User=%s;\
           Password=%s;Option=3;chartset=utf8;'%('localhost',3306,dbname,'root','123456'))
    mysqlconn=pyodbc.connect(conn_info)
    mysqlcur=mysqlconn.cursor()

    sql_sentence='select column_name from Information_schema.columns \
                              where table_schema="'+dbname+'" \
                              and table_Name="'+tbname+'" \
                              order by ORDINAL_POSITION'
    col_name=mysqlcur.execute(sql_sentence).fetchall()
    
    col_names=[]
    for i in range(len(col_name)):
        col_names.append(col_name[i][0])
    
    sql_sentence2='select * from '+tbname+' limit '+str(limit_start)+',10'
    cur=mysqlcur.execute(sql_sentence2)
    
    entries=[]
    for row in cur.fetchall():
        di={}
        for i in range(len(col_name)):
            di[col_name[i][0]]=str(row[i])
        entries.append(di)
    
    sql_sentence3='select count(*) from '+tbname
    count=mysqlcur.execute(sql_sentence3).fetchall()[0][0]
    
    return col_names,entries,count

def get_page(total,p):
    show_page=5
    pageoffset=2
    start=1
    end=total
    
    if total>show_page:
        if p>pageoffset:
            start=p-pageoffset
            if total>p+pageoffset:
                end=p+pageoffset
            else:
                end=total
        else:
            start=1
            if total>show_page:
                end=show_page
            else:
                end=total
        
        if p+pageoffset>total:
            start=start-(p+pageoffset-end)
    
    dic=range(start,end+1)
    return dic
'''
def writecss(num):
    file0=open("D:\\Richard\\Work\\Web\\microblog\\static\\style2bug.txt","r")
    a=file0.read()
    file0.close()
    if num<=5:
        d=str(50)
        b='.page          { margin: 4em auto; width:'+d+'%;'
        c=a.replace('.page          { margin: 4em auto; width:300%;',b)
    elif num<=10:
        d=str(100)
        b='.page          { margin: 4em auto; width:'+d+'%;'
        c=a.replace('.page          { margin: 4em auto; width:300%;',b)
    elif num<=15:
        d=str(200)
        b='.page          { margin: 4em auto; width:'+d+'%;'
        c=a.replace('.page          { margin: 4em auto; width:300%;',b)
    elif num<=30:
        d=str(300)
        b='.page          { margin: 4em auto; width:'+d+'%;'
        c=a.replace('.page          { margin: 4em auto; width:300%;',b)
    file=open("D:\\Richard\\Work\\Web\\microblog\\static\\style2"+d+".css","w")
    file.write(c)
    file.close()
    name="style2"+d+".css"
    return name
'''

    
@app.route('/show/<dbname>/<tbname>',methods=['GET','POST'])
@app.route('/show/<dbname>/<tbname>?p=1',methods=['GET','POST'])
@app.route('/show/<dbname>/<tbname>?p=<page>',methods=['GET','POST'])
def show_entries(dbname,tbname,page=1):
    p=request.args.get("p","")
    show_shouye_status=0
    
    if p=="":
        p=1
    else:
        p=int(p)
        if p>1:
            show_shouye_status=1
    
    limit_start=(int(p)-1)*10        
    col_names,entries,count=df(dbname,tbname,limit_start)
    long=len(col_names)
    #name=writecss(long)
    total=int(count/10)
    
    dic=get_page(total,p)
    datas={
            'col_names':col_names,
           'entries':entries,
           'p':int(p),
           'total':total,
           'show_shouye_status':show_shouye_status,
           'dic_list':dic
           }
    #string=table(col_names,entries)
    #num=1
    #if request.method=='POST':
    #    if int(request.form['turn-page'])<=total:
    #        num=int(request.form['turn-page'])
    #        print('asdf',num)
            
    if long<=5:
        return render_template('show_entries50.html',dbname=dbname,tbname=tbname,datas=datas)#,string=string num=num
    elif long<=10:
        return render_template('show_entries100.html',dbname=dbname,tbname=tbname,datas=datas)
    elif long<=20:
        return render_template('show_entries200.html',dbname=dbname,tbname=tbname,datas=datas)
    elif long<=30:
        return render_template('show_entries300.html',dbname=dbname,tbname=tbname,datas=datas)
    
    

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('退出成功!')
    return redirect(url_for('login'))

@app.route('/add',methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    mysqlcur.execute('insert into table2(date,positive_number) values (?,?)',\
                     [request.form['date'],request.form['num']])
    mysqlcur.commit()
    flash('New entry wa successfully posted')
    return redirect(url_for('show_entries'))


#http_server = HTTPServer(WSGIContainer(app))
#http_server.listen(5000)
#IOLoop.instance().start()

    
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',threaded = True)



'''
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('D:\\Richard\\Work\\Web\\microblog\\flaskr\\schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()
'''


