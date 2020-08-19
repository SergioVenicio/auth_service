from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, id=None, username="", email="", password=""):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def set_password(self, password: str):
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        print(password)
        print(self.password)
        return check_password_hash(
            self.password, password
        )

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user

    @staticmethod
    def identity(payload):
        user_id = payload['identity']
        return User.query.get(user_id)

    def __str__(self):
        return f'User: {self.username}'
