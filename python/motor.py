import paho.mqtt.client as mqtt

from ftShield import FTShield
from conf import Config


def printme(text):
    Config.printme("MOTION:",text)
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    printme("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Config.mqtt_channel+"/motor")
    printme("subscribing to minimop/motion")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    printme(msg.topic+" "+str(msg.payload))
    befehl = msg.payload.decode('utf8').split(',')
    if 3 == len(befehl):
        ftShield.set_motor(befehl[0], befehl[2], befehl[1])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect device

printme("Connecting to Shield")
maxSpeed = 204

ftShield = FTShield()
ftShield.debug = Config.debug
ftShield.maxSpeed = maxSpeed


client.connect(Config.mqtt_server, Config.mqtt_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()