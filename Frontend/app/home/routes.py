# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename
import textract
import os

@blueprint.route('/index')
@login_required
def index():

    return render_template('index.html')


@blueprint.route('/<template>')
@login_required
def sdss(template):

    if TemplateNotFound:
        return render_template('page-404.html'), 404
    
    else:
        return render_template('page-500.html'), 500

@blueprint.route('/auth-signup.html')
@login_required
def fd():
    return render_template('auth-signup.html')

@blueprint.route('/auth-signin.html')
@login_required
def route_template():
    return render_template('auth-signin.html')

def IsFileType(filename, fileTypes):
    if not "." in filename:
        return False;
    
    ext = filename.rsplit(".", 1)[1]
    print(ext.upper())
    if ext.upper() in fileTypes:
        return True
    else:
        return False

@blueprint.route('/upload.html',methods = ['POST', 'GET'])
def upload():
    message = ''
    if request.method == "POST":
        if request.files:
            selectedFile = request.files["getFile"]
            if selectedFile.filename == "":
                print("No file selected")
                message = "**Please select a file. (Image, Word document, pdf)**"
                return render_template('upload.html', message = message)
            
            if not IsFileType(selectedFile.filename, ["DOCX", "PDF", "JPEG", "PNG"]):
                print("haha")
                message = "Incorrect image extension"
                return render_template('upload.html', message = message)
            else:
                if IsFileType(selectedFile.filename, ["DOCX", "PDF"]):
                    selectedFile.save(os.path.join("./app/base/static/files/", selectedFile.filename))
                    message = textract.process("./app/base/static/files/" + selectedFile.filename, encoding='utf-8')
                    return render_template('upload.html', message = message)
                else:
                    return render_template('upload.html', message = "It is an image file.")
    return render_template('upload.html', message = message)