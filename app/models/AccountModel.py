from app import db


class AccountModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)

    account_service = db.Column(db.String)
    account_name = db.Column(db.String)
    account_token = db.Column(db.String)

    def verify(self):
        pass

    def renew(self):
        pass

    def get_data(self, from_date, to_date):
        pass
