# -*- encoding: utf-8 -*-

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('home_blueprint.index'))

# Default Admin and Agent creation

@blueprint.route('/init')
def init():
    print('admin is being created!')
    admin = Users.query.filter_by(username='admin').first()
    if not admin:
        admin = Users(username='admin', password='admin', email='admin@haritam.com', user='ADM')
        db.session.add(admin)
        db.session.commit()
        return 'Created successfully!'
    return 'Already found!'

@blueprint.route('/agent')
def agent():
    print('agent is being created!')
    agent = Users.query.filter_by(username='agent').first()
    if not agent:
        agent = Users(username='agent', password='agent', email='agent@haritam.com', user='AGT')
        db.session.add(agent)
        db.session.commit()
        return 'Created successfully!'
    return 'Already found!'

# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        # read form data
        username = request.form['username']
        password = request.form['password']
        # Locate user
        user = Users.query.filter_by(username=username).first()
        # Check the password
        if user and verify_pass(password, user.password):
            login_user(user)
            if user.user == 'ADM':
                return render_template('home/admin.html')
            if user.user == 'AGT':
                return render_template('home/agent.html')
            return redirect(url_for('authentication_blueprint.route_default'))
        # Something (user or pass) is not ok
        return render_template('accounts/login.html', msg='Wrong user or password', form=login_form)
    if not current_user.is_authenticated:
        return render_template('accounts/login.html', form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='User created please <a href="/login">login</a>',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.route_default'))

@blueprint.route('/index')
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/customer')
def check_login():
    if current_user.is_authenticated:
        return render_template('home/customer.html', segment='index')
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
