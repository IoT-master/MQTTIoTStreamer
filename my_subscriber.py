import paho.mqtt.client as mqtt
from  Confidential.mqtt_account import user, password, broker, port
# https://pimylifeup.com/raspberry-pi-mosquitto-mqtt-server/
# mosquitto -v
# sudo apt install -y mosquitto mosquitto-clients
# sudo systemctl status mosquitto
# sudo systemctl start mosquitto
# sudo systemctl stop mosquitto
# apt-get install mosquitto-clients
# /etc/mosquitto
# sudo mosquitto_passwd -c /etc/mosquitto/pwfile pi
# https://www.digitalocean.com/community/questions/how-to-setup-a-mosquitto-mqtt-server-and-receive-data-from-owntracks
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe(f"{user}/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
# client= mqtt.Client("cname",transport="websockets")
# websockets is port 9001
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(user, password)
client.connect(broker, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

# sudo apt-get install software-properties-common
# sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
# sudo apt-get update

# wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
# sudo apt-key add mosquitto-repo.gpg.key
# cd /etc/apt/sources.list.d/
# sudo wget http://repo.mosquitto.org/debian/mosquitto-buster.list
# sudo apt-get update
# sudo apt-cache search mosquitto
# sudo apt-get install mosquitto
