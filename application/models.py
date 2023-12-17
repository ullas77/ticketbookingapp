from .database import db
from datetime import datetime
class user(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
class admin(db.Model):
    __tablename__ = 'admin'
    adminid = db.Column(db.Integer, primary_key=True)
    adminusername = db.Column(db.String(50), nullable=False)
    adminpassword = db.Column(db.Integer, nullable=False)

class venue(db.Model):
    __tablename__ = 'venue'
    venueid = db.Column(db.Integer, primary_key=True)
    venuename = db.Column(db.String(50), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    #nameofshows = db.relationship("show")
    

class show(db.Model):
    __tablename__ = 'show'
    showid = db.Column(db.Integer, primary_key=True)
    showname = db.Column(db.String(50), nullable=False)
    #venueid=db.column(db.Integer, db.ForeignKey("venue.venueid"))
    
    rating = db.Column(db.Float, nullable=False)
    tags = db.Column(db.String(100), nullable=False)
    ticketprice = db.Column(db.Float, nullable=False)
    maxticket = db.Column(db.String(100), nullable=False)




class booking(db.Model):
    __tablename__ = 'booking'
    bookingid = db.Column(db.Integer, primary_key=True)
    #userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    showid = db.Column(db.Integer, db.ForeignKey('show.showid'), nullable=False)
    nameofvenue= db.Column(db.String(100), nullable=False)
    numberoftickets = db.Column(db.Integer, nullable=False)
    bookingdate = db.Column(db.String(100), nullable=False)


