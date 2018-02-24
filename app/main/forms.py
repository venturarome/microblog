from flask import request
#flask_wtf is a wrapper of wtforms.
# https://wtforms.readthedocs.io/en/latest/fields.html
# https://flask-wtf.readthedocs.io/en/stable/
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=256)])
    submit = SubmitField(_l('Submit'))

    # Overloaded constructor that accepts the original username as an argument, saves it as an instance variable, and checks it in 'validate_username()'
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_l('Please use a different username.'))

                
class CommentForm(FlaskForm):
    comment = TextAreaField(_l('Say something'), validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))



### Actual website (for future reference)
from wtforms import PasswordField, DateField, FileField
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

