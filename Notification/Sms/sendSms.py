from flask import Flask, render_template
from flask_mail import Mail, Message
from dotenv import dotenv_values
from Model import *

get_env = dotenv_values(".env")  

app = Flask(__name__)
# db = SQLAlchemy(app)

def send_notification_sms(to, subject):
    with app.app_context():
        try:
            return True
        except Exception as e:
            print(f"Failed to send sms: {e}")
            return False
