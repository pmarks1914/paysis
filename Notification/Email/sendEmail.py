from flask import Flask
from flask_mail import Mail, Message
from dotenv import dotenv_values



get_env = dotenv_values(".env")  
app = Flask(__name__)

# Configuration for email sending
app.config['MAIL_SERVER'] = get_env['MAIL_SERVER']
app.config['MAIL_PORT'] = get_env['MAIL_PORT']
app.config['MAIL_USE_TLS'] = get_env['MAIL_USE_TLS']
app.config['MAIL_USE_SSL'] = get_env['MAIL_USE_SSL']
app.config['MAIL_USERNAME'] =  get_env['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = get_env['MAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = get_env['MAIL_DEFAULT_SENDER']


mail = Mail(app)

def send_notification_email(to, subject, body):
    with app.app_context():
        message = Message(subject, recipients=[to])
        message.body = body

        try:
            mail.send(message)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
# send_notification_email("pmarks1914@gmail.com", "test", "test body")