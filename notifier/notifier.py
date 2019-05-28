from flask import Flask
from flask_mail import Mail, Message
import datetime


app = Flask(__name__)

from_email = "encearthquakenotification@gmail.com"
from_email_password = "kohyomumdlonqmtq"
emails = ["gstrenge01@gmail.com"]  #emails = ["gstrenge01@gmail.com", "sebasarboleda22@gmail.com"]

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = from_email
app.config['MAIL_PASSWORD'] = from_email_password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



mail = Mail(app)



@app.route('/<message>')


def hello_world(message):
	
	
	#All Contacts in one email:
	"""
	today= str(datetime.datetime.now().strftime("%m-%d-%y %H:%M"))
	
	msg = Message("Warning: " + today, sender = from_email, recipients = emails)
	msg.body = message
	mail.send(msg)
	"""
	
	#Individual Emails for each contact
	with mail.connect() as conn:
		today= str(datetime.datetime.now().strftime("%m-%d-%y %H:%M"))
		for email in emails:
			messageToSend = message
			subject = "Warning: " + today
			msg = Message(recipients=[email],
						  body=messageToSend,
						  sender = from_email,
						  subject=subject)

			conn.send(msg)
	
	return "sent"