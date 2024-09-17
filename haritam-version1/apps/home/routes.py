# -*- encoding: utf-8 -*-

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import db
from apps.home.models import Category
from apps.home.forms import CategoryForm


@blueprint.route('/index')
# @login_required
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/admin/category', methods=['GET', 'POST'])
@login_required
def create_category():
    if request.method == 'POST':
        category_form = CategoryForm(request.form)
        category = Users.query.filter_by(name=category_form['name']).first()
        if not category:
            category = Category(**request.form)
            db.session.add(category)
            db.session.commit()
        return render_template('home/admin.html')
    return render_template('home/admin.html')

@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'
        # Detect the current page
        segment = get_segment(request)
        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except:
        return render_template('home/page-500.html'), 500

# @app.route('/check-login')
# def check_login():
#     if 'user' in session:
#         return redirect(url_for('action_page'))
#     else:
#         flash("Please login first.", "danger")
#         return redirect(url_for('home'))


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
