from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=25)])
    password = PasswordField('password',validators=[DataRequired()])
    password_confirm = PasswordField('confirm password',validators=[DataRequired(), EqualTo('password')])
    user_key = StringField('User Key', validators=[DataRequired(), Length(min=64,max=64)])
    user_secret = StringField('User secret', validators=[DataRequired(), Length(min=64,max=64)])
    
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        try:
            user = User.query.filter_by(username=username.data).first()
        except:
            print('The DataBase is empty')
        else:
            if user:
                raise ValidationError('That username is not available')
    def validate_key(self,user_key):
        # Check to see if its a valid binanace connection
        try:
            key = User.query.filter_by(username=user_key.data).first()
        except:
            print('The DataBase is empty')
        else:
            if key:
                raise ValidationError('That key is not unique')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=25)])
    password = PasswordField('password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class UpdateAccountForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=25)])
    
    user_key = StringField('User Key', validators=[DataRequired(), Length(min=64,max=64)])
    
    user_secret = StringField('User secret', validators=[DataRequired(), Length(min=64,max=64)])
    
    submit = SubmitField('Update')
    
    def validate_username(self,username):
        if username != current_user.username:
            try:
                user = User.query.filter_by(username=username.data).first()
            except:
                print('The DataBase is empty')
            else:
                if user:
                    raise ValidationError('That username is not available')
    def validate_key(self,user_key):
        if user_key != current_user.user_key:
            # Check to see if its a valid binanace connection
            try:
                key = User.query.filter_by(username=user_key.data).first()
            except:
                print('The DataBase is empty')
            else:
                if key:
                    raise ValidationError('That key is not unique')
    def validate_secret(self,user_secret):
        if user_secret != current_user.secret:
            # Check to see if its a valid binanace connection
            try:
                secret = User.query.filter_by(username=user_secret.data).first()
            except:
                print('The DataBase is empty')
            else:
                if secret:
                    raise ValidationError('That key is not unique')
class ConnectionForm(FlaskForm):
    name = StringField('name',validators=[DataRequired(),Length(min=2,max=25)])
    key = StringField('follower Key', validators=[DataRequired(), Length(min=64,max=64)])
    secret = StringField('follower Key', validators=[DataRequired(), Length(min=64,max=64)])
    submit = SubmitField('Create')
    def validate_name(self,name):
        try:
            check_name = User.query.filter_by(username=name.data).first()
        except:
            print('The DataBase is empty')
        else:
            if check_name:
                raise ValidationError('That username is not available')
    def validate_key(self,key):
        # Check to see if its a valid binanace connection
        try:
            check_key = User.query.filter_by(username=key.data).first()
        except:
            print('The DataBase is empty')
        else:
            if check_key:
                raise ValidationError('That key is not unique')
    def validate_secret(self,secret):

        # Check to see if its a valid binanace connection
        try:
            check_secret = User.query.filter_by(username=check_secret.data).first()
        except:
            print('The DataBase is empty')
        else:
            if check_secret:
                raise ValidationError('That key is not unique')
class UpdateConnectionForm(FlaskForm):
    
    name = StringField('name', validators=[DataRequired(), Length(min=2,max=25)])
    
    key = StringField('Connection Key', validators=[DataRequired(), Length(min=64,max=64)])
    
    secret = StringField('Connection Secret', validators=[DataRequired(), Length(min=64,max=64)])
    
    submit = SubmitField('Update')
    
    def validate_name(self,name):
        try:
            check_name = User.query.filter_by(username=name.data).first()
        except:
            print('The DataBase is empty')
        else:
            if check_name:
                raise ValidationError('That username is not available')
    def validate_key(self,key):
        # Check to see if its a valid binanace connection
        try:
            check_key = User.query.filter_by(username=key.data).first()
        except:
            print('The DataBase is empty')
        else:
            if check_key:
                raise ValidationError('That key is not unique')
    def validate_secret(self,secret):

        # Check to see if its a valid binanace connection
        try:
            check_secret = User.query.filter_by(username=check_secret.data).first()
        except:
            print('The DataBase is empty')
        else:
            if check_secret:
                raise ValidationError('That key is not unique')