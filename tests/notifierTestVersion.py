
"""

A small Test application to show how to use Flask-MQTT.

"""

import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt


eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET'] = '260892c601c030dbc35778a9184e127d'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'iot.eclipse.org'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

topic = "data/anomalyDetected"

mqtt = Mqtt(app)



@app.route('/')
def index():
    return '1'

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(topic)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)


#@mqtt.on_log()
#def handle_logging(client, userdata, level, buf):
#    print(level, buf)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=False, debug=False)
