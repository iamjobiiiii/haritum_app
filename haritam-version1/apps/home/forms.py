from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

# Category

class CategoryForm(FlaskForm):
    name = StringField('Name', id='name_category', validators=[DataRequired()])
    details = StringField('Details', id='details_category', validators=[DataRequired()])

