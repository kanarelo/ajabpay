from ajabpay.index import db, bcrypt
from decimal import Decimal as D

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(25), unique=True, nullable=False)

    date_joined = db.Column(db.DateTime(), nullable=False)
    last_login = db.Column(db.DateTime(), nullable=True)

    active = db.Column(db.Boolean(), default=False, nullable=False)

    date_updated = db.Column(db.DateTime(), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False)

    def __init__(self, password=None, *args, **kwargs):
        if password:
            self.password = User.hashed_password(password)

        super(User, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

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
