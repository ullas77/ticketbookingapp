import os
from flask import Flask
from application import config
from flask_restful import Resource,Api
from application.config import LocalDevelopmentConfig
from application.database import db
from celery_worker import make_celery
from application.models import show,venue,booking,admin
from application.models import user
import requests
from celery.result import AsyncResult
import time
import csv
from httplib2 import Http
from celery.schedules import crontab
from json import dumps
from datetime import timedelta
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template

from flask_caching import Cache
from api.resource import User, api

app = None
cache=None

def create_app():
    app = Flask(__name__, template_folder="templates")
    
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    
    app.app_context().push()
    return app
    

    


app = create_app()
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)
cache=Cache(app)
#cache=Cache(app)
    #app.app_context().push()
   # return cache
@celery.task()
def add_together(a, b):
    time.sleep(5)
    return a + b
#@celery.on_after_configure.connect
#def setup_periodic_tasks(sender, **kwargs):
#   sender.add_periodic_task(10.0, send_remainder.s(),name='daily-remainder')
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, send_remainder_via_email.s(),name='daily-remainder')

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, send_remainder.s(),name='daily-remainder-chat')

api.init_app(app)

@celery.task()
def generate_csv(updated_show_names=None):
    time.sleep(6)
    fields = ['Name', 'Rating']

    shows = show.query.all()

    rows = []
    for sho in shows:
        #show_name = updated_show_names.get(sho.showname, sho.rating)
        rows.append([sho.showname,sho.rating])

    with open("static/data.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

    return "CSV generation completed"

from application.controllers import *
@app.route("/trigger_celery_job", methods=["GET", "POST"])

def trigger_celery_job():
    updated_show_names = {
        "show1": "Updated Name 1",
        "show2": "Updated Name 2",
        "show3": "Updated Name 3",
        "show4": "Updated Name 4",
        "show5": "Updated Name 5",
        "show6": "Updated Name 6"
    }
    
    a = generate_csv.delay(updated_show_names)
    
    return {
        "Task ID": a.id,
        "Task State": a.state,
        "Task Result": a.result
    }
@app.route("/status/<id>")
def check_status(id):
    res = AsyncResult(id)
    
    return {
        "Task ID": res.id,
        "Task State": res.state,
        "Task Result": res.result
    }

import requests
import json

@celery.task()


def send_remainder():
    """Google Chat incoming webhook quickstart."""
    #users = user.query.all()
    current_time = datetime.now()
    users = user.query.all()


    for use in users:
        if use.timestamp <= (current_time - timedelta(seconds=50)):
            url =  "https://chat.googleapis.com/v1/spaces/AAAARb8O3AU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=C8eoGkvciq3IK0T31MgffhDULXxUo_8QzXlBWXat6zo"
            bot_message = {
                'text': f"Hello {use.username}, you have not logged in for 24 hours!"
            }
            message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
            http_obj = Http()
            response = http_obj.request(
                uri=url,
                method='POST',
                headers=message_headers,
                body=dumps(bot_message),
            )
            print(response)

#celery -A main.celery worker -l info
#celery -A main.celery beat --max-interval 2 -l info
#pip install flask flask-sqlalchemy celery[redis]
#source .env/bin/activate
#virtualenv .env
#sudo apt install python3-virtualenv
#cd "/mnt/c/Users/ullas/Desktop/mad2/ticket"
#http://localhost:8025/#
#Mailhog

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS= "email@owner.com"
SENDER_PASSWORD =""
def send_email(to_address, subject, message, content="text", attachment_file=None):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
                msg.attach(MIMEText(message, "plain"))

    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            part=MIMEBase("application","octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        msg.attach(part)
    S= smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    S.login(SENDER_ADDRESS, SENDER_PASSWORD)
    S.send_message(msg)
    S.quit()
    return True


    
@celery.task
def send_remainder_via_email():
    boo=booking.query.all()
    for b in boo:
        send_email(
        
            to_address="ullas@gmail.com",
            subject="Your movie app booking details",
            message = f"Hi! Booking id is {b.bookingid}, number of tickets are {b.numberoftickets}, name of venue is {b.nameofvenue}, show id is {b.showid}"


        )
    return "Email should arrive in inbox in short time"











if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)


