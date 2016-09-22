from ajabpay.index import db
from decimal import Decimal as D

class MPesaProfile(db.Model):
    __tablename__ = "mpesaprofile"
    
    id = db.Column(db.Integer(), primary_key=True)

    # user = db.relationship('User', backref='mpesa_profile', uselist=False,
    #     primaryjoin='User.phone==MPesaProfile.mobile_phone_no')
    mobile_phone_no = db.Column(db.String(25), db.ForeignKey('user.phone'), 
        nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account', backref='mpesa_accounts')

    name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(10), nullable=False)
    
    date_created = db.Column(db.DateTime(), nullable=False)
    date_updated = db.Column(db.DateTime(), nullable=False)

    def __unicode__(self):
        return '[%s] %s' % (self.paypal_user_id, self.email)

