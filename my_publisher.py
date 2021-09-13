import paho.mqtt.client as paho
from  Confidential.mqtt_account import user, password, broker, port

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass
client1= paho.Client("control1")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.username_pw_set(user, password)
client1.connect(broker,port)                                 #establish connection
ret= client1.publish("pi/you","It works!")                   #publish