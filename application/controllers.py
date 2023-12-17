from flask import Flask
from flask import request,jsonify
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

from flask import current_app as app
from application.models import show,venue,booking,user,admin
from .database import db
from flask import redirect, url_for
from flask import flash
from sqlalchemy.orm import query
from datetime import datetime

@app.route('/booktickets/<int:showid>', methods=['GET', 'POST'])
def book_show(showid):
    if request.method == 'POST':
        Show = show.query.get(showid)
        Cap = int(Show.maxticket)

        numberoftickets = int(request.form['numberoftickets'])
        bookingdate = request.form['bookingdate']
        nameofvenue = request.form['nameofvenue']
        if numberoftickets > Cap:
            return jsonify({"message": "Sorry the house is full."}), 201

        else:
            book = booking(showid=showid, numberoftickets=numberoftickets,bookingdate=bookingdate,nameofvenue=nameofvenue)
            db.session.add(book)
            db.session.commit()
            
        return jsonify({"message": "Tickets booked successfully."}), 201

    ven=venue.query.all()
    return render_template('booktickets.html',showid=showid,ven=ven)


    
@app.route('/editshow/<string:showname>', methods=['GET', 'POST'])
def editshow(showname):
    if request.method == 'POST':
        sname= show.query.filter_by(showname=showname).first()
        newsname=request.form['newsname']
        
        sname.showname=newsname
        db.session.add(sname)
        
        

        
        
        
        
        
        
        
        
        
        db.session.commit()
        return render_template("edits.html")

    

    

    
    
    return render_template('editshow.html',show=showname)
@app.route('/createshow', methods=['GET', 'POST'])
def createsh():
    if request.method == 'POST':
        showname = request.form['showname']
        
        rating = request.form['rating']
        tags = request.form['tags']
        ticketprice = request.form['ticketprice']
        maxticket = request.form['maxticket']

        
        
        
        
        
        
        
        
        
        
        
        new_show = show(showname=showname,tags=tags, rating=rating, ticketprice=ticketprice,maxticket=maxticket)
        db.session.add(new_show)
        db.session.commit()
        return render_template("cs.html")

    return render_template("createshow.html")
@app.route('/deleteshow/<string:showname>', methods=['GET', 'POST'])
def deleteshow(showname):
    # Get the venue by venueid
    
    if request.method == 'POST':
        
        Show=show.query.filter_by(showname=showname).first()
        
        db.session.delete(Show)
        db.session.commit()
        
        return render_template("ds.html")


    
    return render_template('deleteshow.html',show=showname)

@app.route('/createvenue', methods=['GET', 'POST'])
def createvenue():
    if request.method == 'POST':
        venuename = request.form['venuename']
        place = request.form['place']
        capacity = request.form['capacity']
        new_venue = venue(venuename=venuename, place=place, capacity=capacity)
        db.session.add(new_venue)
        db.session.commit()

        return render_template("ad.html")



    else:
        return render_template('createvenue.html')


@app.route('/editvenue/<string:venuename>', methods=['GET', 'POST'])
def editvenue(venuename):
    if request.method == 'POST':
        name= venue.query.filter_by(venuename=venuename).first()
        
        newvname=request.form['newvname']
        
        #venue=venue.query.filter_by(venue).first()
        
        name.venuename=newvname
        db.session.add(name)
        db.session.commit()
        return render_template("edit.html")

    
    return render_template('editvenue.html',venue=venuename)

@app.route('/deletevenue/<string:venuename>', methods=['GET', 'POST'])
def deletevenue(venuename):
    
    if request.method == 'POST':
        
        Venue=venue.query.filter_by(venuename=venuename).first()
        db.session.delete(Venue)
        db.session.commit()
        return render_template("dv.html")


    
    return render_template('deletevenue.html',venue=venuename)





        

@app.route('/searchresults', methods=['GET', 'POST'])
def search_shows():
    if request.method == 'POST':
        serch = request.form['searchby']
        searchterm = request.form['searchterm']
        shows = []
        if serch == 'showname':
            shows = show.query.filter(show.showname.contains(searchterm)).all()
            return render_template('shows.html', shows=shows)
        elif serch == 'tags':
            shows = show.query.filter(show.tags.contains(searchterm)).all()
            return render_template('shows.html', shows=shows)
        elif serch == 'rating':
            shows = show.query.filter(show.rating == int(searchterm)).all()
            return render_template('shows.html', shows=shows)
        elif serch == 'location':
            venues = venue.query.filter(venue.place.contains(searchterm)).all()
            return render_template('venues.html', venues=venues)
        elif serch == 'venuename':
            venues = venue.query.filter(venue.venuename.contains(searchterm)).all()
            return render_template('venues.html', venues=venues)



        
    return render_template('shows.html')



@app.route('/')
#@cache.cached(timeout=50)
def ullas():
    return render_template('ullas.html')

@app.route('/userlogin', methods=['GET', 'POST'])
def ullaslogin():
    ven=venue.query.all()

    sho=show.query.all()
    username = request.form['username']
    password = request.form['password']
    use = user(username=username,password=password)
    db.session.add(use)
    db.session.commit()


    return render_template('userlogin.html',ven=ven,sho=sho)
    
    

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    ven=venue.query.all()
    sho=show.query.all()
    adminusername = request.form['adminusername']
    adminpassword = request.form['adminpassword']
    if adminpassword=="ullas":
        adm = admin(adminusername=adminusername,adminpassword=adminpassword)
        db.session.add(adm)
        db.session.commit()
        return render_template('adminlogin.html',ven=ven,sho=sho)
    else:
        return "Invalid password"
@app.route('/admindashboard', methods=['GET', 'POST'])
def admindashboard():
    ven=venue.query.all()
    sho=show.query.all()
    
    return render_template('admindashboard.html',ven=ven,sho=sho)
@app.route('/userdashboard', methods=['GET', 'POST'])
def userdashboard():
    ven=venue.query.all()
    sho=show.query.all()
    boo=booking.query.all()
    return render_template('userdashboard.html',ven=ven,sho=sho,boo=boo)

@app.route('/list_shows', methods=['GET','POST'])
def list_shows():
    shows=show.query.all()
    return render_template('showlist.html',shows=shows)
@app.route('/list_venues', methods=['GET','POST'])
def list_venues():
    venues=venue.query.all()
    return render_template('venuelist.html',venues=venues)