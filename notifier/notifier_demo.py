from flask import Flask
from flask_mail import Mail, Message
import datetime
import json

from flask_mqtt import Mqtt

#Global Variables (To Change to env variables)
HOST = "iot.eclipse.org"
PORT = 1883
KEEPALIVE = 60
topic =	 "data/anomalyDetected"
client_id = "/Notifier"

#Starting Flask Application
app = Flask(__name__)

#Initializing sending-email address information
from_email = "encearthquakenotification@gmail.com"
from_email_password = "kohyomumdlonqmtq"

#Configuring Flask
app.config['SECRET'] = '260892c601c030dbc35778a9184e127d'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = from_email
app.config['MAIL_PASSWORD'] = from_email_password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


#Configuring Flask-mqtt
app.config['MQTT_BROKER_URL'] = 'iot.eclipse.org'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

#Connecting to Database

emailArray = ['gstrenge01@gmail.com']

#Initializing Flask-mail
mail = Mail(app)
mqtt = Mqtt(app)




@app.route('/')
def index():
	return None

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
	mqtt.subscribe(topic, qos=2)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
	data = dict(
		topic=message.topic,
		payload=message.payload.decode()
	)

	print(data['payload'])

	inspectorPackageJSON = data['payload']

	inspectorPackageDict = json.loads(inspectorPackageJSON)




	#Individual Emails for each contact
	#print("EmailTime")
	with mail.connect() as conn:


		today = inspectorPackageDict['time_init']

		topicNum = 0
		for topic in inspectorPackageDict['topic']:

			if topicNum <2:
				topicNum+= 1
				continue
			emails = emailArray

			emailsSent = 0

			for email in emails:

				#email is storing a one-element-long tuple. To isolated the string inside, address is
				#being assigned the one element in the tuple
				address = email

				#The message for the email is taken from the URL
				topic = topic
				anomaly_status = inspectorPackageDict['anomaly_status']
				location = inspectorPackageDict['location']
				time_init = inspectorPackageDict['time_init']
				duration = str(inspectorPackageDict['time_duration'])

				messageToSend = f"{topic} Anomaly {anomaly_status}:\nLocation: {location}\nTime Detected: {time_init}\nDuration: {duration}"


				#The subject is taken from the current time
				subject = f"{topic} Anomaly {anomaly_status}: " + today

				#Forming the message
				msg = Message(recipients=[address],
							  body=messageToSend,
							  sender = from_email,
							  subject=subject)

				try:
					with app.app_context():
						conn.send(msg)
				except Exception as err:
					print(err)
				emailsSent += 1

	print(f"{str(emailsSent)} Email(s) Sent: " + today)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, use_reloader=False, debug=True)
