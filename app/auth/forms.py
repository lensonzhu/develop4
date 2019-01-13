from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User


class ChangeEmailForm(FlaskForm):
    email=StringField('New email',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('password',validators=[Required()])
    submit=SubmitField('Update Email')

    def validate_email(self,field):
        if User.query.filter_by(email=fielf.data).first():
            raise ValidationError('Email already registered')


class ResetPasswordRequestForm(FlaskForm):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    submit=SubmitField('Fuck you Reset password')



class ResetPasswordForm(FlaskForm):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('New password',validators=[Required(),EqualTo('password2',message='PasswordField must be match')])
    password2=PasswordField('Confirm password')
    submit=SubmitField('Reset password')

    def validate_email(self,field):
        if User.query.filter_by(email=Field.data).first():
            raise ValidationError('Unknown email address')


class ChangePasswordForm(FlaskForm):
    old_password=PasswordField('Old password',validators=[Required()])
    password=PasswordField('New password',validators=[Required(),EqualTo('password2',message='Password must be match')])
    password2=PasswordField('Confirm new password')
    submit=SubmitField('Fuck Change PSD')


class LoginForm(FlaskForm):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('Password',validators=[Required()])
    remember_me=BooleanField('Keep me logged in')
    submit=SubmitField('Log in')


class RegisterForm(FlaskForm):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only      letters,numbers, dots or underscores')])
    password=PasswordField('Password',validators=[Required(),EqualTo('password2',message='Fuck you Passwords must be match.')])
    password2=PasswordField('Confirm password',validators=[Required()])
    submit=SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already register')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already be used')
