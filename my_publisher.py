import paho.mqtt.client as paho
from  Confidential.mqtt_account import user, password, broker, port
import pandas as pd
from pathlib import Path
from datetime import datetime
from time import sleep

turbine_df = pd.read_csv(Path.cwd().joinpath('turbine.csv'))


def on_publish(client,userdata,result): 
    print(result)            #create function for callback
    print("data published \n")

client1= paho.Client("control1")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.username_pw_set(user, password)
client1.connect(broker,port)                                 #establish connection
for index, row in turbine_df.iterrows():
    message = ';'.join((str(datetime.strftime(datetime.now(), '%c')), str(row['Tb_model']), str(row['Tb_mod_n'])))
    results, mid= client1.publish(f"{user}/you",message)    
    sleep(1)
