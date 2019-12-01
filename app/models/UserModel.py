from app import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
