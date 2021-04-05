from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    try: 
        info = User.query.get(int(user_id))
    except:
        return
    else:
        return info
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    #image_file = db.Column(db.String(20), nullable=False, default='usericon.png')
    password = db.Column(db.String(60),nullable=False)
    user_key = db.Column(db.String(64),nullable=False)
    user_secret = db.Column(db.String(64),nullable=False)
    connections = db.relationship('Connection',backref='USER',lazy=True)

    def __repr__(self):
        return f"User('{self.username}'"

class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    key = db.Column(db.String(64),nullable=False)
    secret = db.Column(db.String(64),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Connection('{self.name}')"