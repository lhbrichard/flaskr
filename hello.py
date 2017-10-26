# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 19:35:40 2017

@author: richard
"""
import os
from flask import Flask,request,url_for,redirect,render_template,send_from_directory
from werkzeug import secure_filename

app=Flask(__name__)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html',name=name)

@app.route('/ri')
def helld():
    return "richard"

@app.route('/zj=<username>')
def show(username):
    return 'zj is %s'%username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

@app.route('/login',methods=['GET','POST'])
def login():
    error=None
    if request.method=='POST':
        do_login()
    else:
        show_the_login_form()


UPLOAD_FOLDER = 'D:\\Richard\\Work\\Web\\microblog'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@app.route('/upload',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!DOCTYPE html>
    <title>Upload new File</title>
    <h1>Upload new file</h1>
    <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=file>
            <input type=submit value Upload>
    </form>
    '''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)






if __name__=="__main__":
    app.run(debug=True)