from ajabpay.index import db, bcrypt
from decimal import Decimal as D

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    phone = db.Column(db.String(25))

    def __init__(self, first_name=None, last_name=None, email=None, password=None, phone=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.active = True
        self.phone = phone

        if password:
            self.password = User.hashed_password(password)

    @staticmethod
    def hashed_password(password):
        return bcrypt.generate_password_hash(password)

    @staticmethod
    def get_user_with_email_and_password(email, password):
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None
