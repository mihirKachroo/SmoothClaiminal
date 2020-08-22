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

@blueprint.route('/upload.html',methods = ['POST', 'GET'])
def upload():
    message = ''
    if request.method == 'POST':
        message='works'
    return render_template('upload.html', message=message)