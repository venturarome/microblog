#flask_wtf is a wrapper of wtforms.
# https://wtforms.readthedocs.io/en/latest/fields.html
# https://flask-wtf.readthedocs.io/en/stable/
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, FileField    #, MultipleFileField (not working yet...)
from wtforms.validators import DataRequired

# Tutorial
class LoginTutoForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


### Actual website

#=== Admin login
class AdminLoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Entrar')

#=== Admin: add blog entry
class AddBlogEntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = StringField('Image Name (located in /images/blog/)', validators=[DataRequired()])   # Migrar usando: https://flask-wtf.readthedocs.io/en/stable/form.html#module-flask_wtf.file o https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file  o MUCHO MEJOR https://wtforms.readthedocs.io/en/latest/fields.html#wtforms.fields.FileField
    category1 = StringField('Category 1')
    category2 = StringField('Category 2')
    category3 = StringField('Category 3')   # Migrar usando otro tipo de input.
    content = TextAreaField('Content')

#=== Admin: add event
class AddEventForm(FlaskForm):
    startdate = DateField('Fecha de inicio', format='%Y-%m-%d')
    # To check more info in wtforms page.
   

### Sample:
class SampleForm(FlaskForm):
    aStringField = StringField('StringField')
    aPasswordField = PasswordField('PasswordField')
    aTextAreaField = TextAreaField('TextAreaField')
    aDateField = DateField('DateField')
    aFileField = FileField('FileField')
