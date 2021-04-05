from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 


app = Flask(__name__)
app.config['SECRET_KEY'] = '90e8cd840b209978dbde202e3b28c2f0'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appDB.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' 

from app import routes