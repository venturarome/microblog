#flask_wtf is a wrapper of wtforms.
# https://wtforms.readthedocs.io/en/latest/fields.html
# https://flask-wtf.readthedocs.io/en/stable/
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, FileField    #, MultipleFileField (not working yet...)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # When you add any methods that match the pattern validate_<field_name>, WTForms takes those as custom validators and invokes them in addition to the stock validators.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=256)])
    submit = SubmitField('Submit')

    # Overloaded constructor that accepts the original username as an argument, saves it as an instance variable, and checks it in 'validate_username()'
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class CommentForm(FlaskForm):
    comment = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')





### Actual website (for future reference)

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

