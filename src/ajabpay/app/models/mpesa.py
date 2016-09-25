from ajabpay.index import db
from decimal import Decimal as D

class MPesaProfile(db.Model):
    __tablename__ = "mpesaprofile"
    
    id = db.Column(db.Integer(), primary_key=True)

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False, unique=True)
    user = db.relationship('User', backref='mpesa_profile', uselist=False)# primaryjoin='User.phone==MPesaProfile.mobile_phone_no')

    mobile_phone_no = db.Column(db.String(25), unique=True, nullable=False)
    registered_name = db.Column(db.String(100), nullable=True)

    date_created = db.Column(db.DateTime(), nullable=False)
    date_updated = db.Column(db.DateTime(), nullable=False)

    def __unicode__(self):
        return '[%s] %s' % (self.paypal_user_id, self.email)

