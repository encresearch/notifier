from flask import Flask
from flask_mail import Mail, Message
import datetime
import json
import psycopg2
from databaseConnect import Database



today= str(datetime.datetime.now().strftime("%m-%d-%y %H:%M"))

inspectorPackage = {
					'topic': 'gas_sensor',
					'location': 'NA-EAST',
					'time_init': today,
					'time_duration': 12
				   }





#Starting Flask Application
app = Flask(__name__)

#Initializing sending-email address information
from_email = "encearthquakenotification@gmail.com"
from_email_password = "kohyomumdlonqmtq"

#Configuring Flask
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = from_email
app.config['MAIL_PASSWORD'] = from_email_password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

#Initializing Flask-mail
mail = Mail(app)

db = None

while True:
	db = Database()
	
	if db.connected == False:
		print("Unable to connect: Trying again in 1s")
		sleep(1)
	else:
		break


@app.route('/<message>')


def hello_world(message):
	
	
	#Individual Emails for each contact
	with mail.connect() as conn:
	
		today= str(datetime.datetime.now().strftime("%m-%d-%y %H:%M"))
		
		emails = db.getEmails(inspectorPackage)
		
		emailsSent = 0
		
		for email in emails:
			
			#email is storing a one-element-long tuple. To isolated the string inside, address is
			#being assigned the one element in the tuple
			address = email[0]
			
			#The message for the email is taken from the URL
			messageToSend = f"{inspectorPackage['topic']} Anomaly: " + today + f"\nLocation: {inspectorPackage['location']}\nTime Detected: {inspectorPackage['time_init']}\nTime Duration: {inspectorPackage['time_duration']}"
			
			#The subject is taken from the current time
			subject = f"{inspectorPackage['topic']} Anomaly: " + today
			
			#Forming the message
			msg = Message(recipients=[address],
						  body=messageToSend,
						  sender = from_email,
						  subject=subject)

			conn.send(msg)
			emailsSent += 1
	
	return f"{str(emailsSent)} Email(s) Sent: " + today