from flask import Flask
from flask_mail import Mail, Message
import datetime
import psycopg2


def getEmails():
	
	#Query to get all unique emails from the database
	get_email_query = "SELECT DISTINCT email FROM emails"
	
	#Initializing connection variable to allow the finally statement to execute without throwing
	#"UnboundLocalError: local variable 'connection' referenced before assignment"
	connection = None
	
	#Attempting to connect to the database
	try:
		connection = psycopg2.connect(user = "postgres",
									  password = "password",
									  host = "127.0.0.1",
									  port = "5432",
									  database = "ENC_Earthquake_Email_List")
									  
		cursor = connection.cursor()

		#Executing the query to get all email addresses
		cursor.execute(get_email_query)
		emailArray = cursor.fetchall()

	except (Exception, psycopg2.Error) as error :
		emailArray = []
		print ("Error while connecting to Email Database", error)
	
	finally:
		if(connection):
			cursor.close()
			connection.close()
			print("Email Database connection is closed")
		
		#Return the list of emails
		return emailArray




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


@app.route('/<message>')


def hello_world(message):
	
	
	#Individual Emails for each contact
	with mail.connect() as conn:
	
		today= str(datetime.datetime.now().strftime("%m-%d-%y %H:%M"))
		
		emails = getEmails()
		
		for email in emails:
			
			#email is storing a one-element-long tuple. To isolated the string inside, address is
			#being assigned the one element in the tuple
			address = email[0]
			
			#The message for the email is taken from the URL
			messageToSend = message
			
			#The subject is taken from the current time
			subject = "Warning: " + today
			
			#Forming the message
			msg = Message(recipients=[address],
						  body=messageToSend,
						  sender = from_email,
						  subject=subject)

			conn.send(msg)
	
	return "Email(s) Sent: " + today