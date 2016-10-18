from flask import session

from sqlalchemy import UniqueConstraint

from ajabpay.index import app, db, bcrypt, login_manager
from decimal import Decimal as D

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    email = db.Column(db.String(255), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False)

    phone = db.Column(db.String(25), unique=True, nullable=False)
    phone_verified = db.Column(db.Boolean, default=False)

    date_joined = db.Column(db.DateTime(), nullable=False)
    last_login = db.Column(db.DateTime(), nullable=True)

    date_updated = db.Column(db.DateTime(), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False)

    accounts = db.relationship('Account', lazy='dynamic')

    def __init__(self, password=None, *args, **kwargs):
        if password:
            self.password = User.hashed_password(password)

        super(User, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def is_authenticated(self):
        return (int(session.get('user_id', 0)) == self.id)
 
    @property
    def is_active(self):
        return (self.email_verified and self.phone_verified)
 
    @property
    def is_anonymous(self):
        return not self.is_authenticated
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.email)

    @staticmethod
    def hashed_password(password):
        return bcrypt.generate_password_hash(password)

    @staticmethod
    def get_user_with_email_and_password(email, password):
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            return user

class AccountVerification(db.Model):
    __tablename__ = "accountverification"
    __table_args__ = (
        db.UniqueConstraint('mobile_code', 'email_code'),
    )

    id = db.Column(db.Integer(), primary_key=True)
    
    email_code = db.Column(db.String(15), nullable=False)
    mobile_code = db.Column(db.String(10), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')

    expiry_date  = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)    

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))