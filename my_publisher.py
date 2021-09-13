import paho.mqtt.client as paho
from  Confidential.mqtt_account import user, password, broker, port

def on_publish(client,userdata,result): 
    print(result)            #create function for callback
    print("data published \n")

client1= paho.Client("control1")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.username_pw_set(user, password)
client1.connect(broker,port)                                 #establish connection
results, mid= client1.publish(f"{user}/you","It works!")                   #publish
results, mid= client1.publish(f"{user}/you","It works again!")                   #publish