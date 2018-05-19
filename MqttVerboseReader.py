import paho.mqtt.client as mqtt #import the client1
import time

############ Printing Received Data Function

def on_message(client, userdata, message):
    
    dataLogFile = open("dataLog.txt", "a")
    dataLogFile.write('\n')
    dataLogFile.write(message.topic)
    dataLogFile.write(" said: ")
    dataLogFile.write(str(message.payload.decode("utf-8")))
    print(message.topic,"says: ",str(message.payload.decode("utf-8")))
    dataLogFile.close()
    
                
########################################



print("creating new instance")


client = mqtt.Client("VerboseReader") 
client.on_message=on_message #attach function to callback

print("connecting to broker")
client.connect("localhost") #connect to broker
dataLogFile = open("dataLog.txt","a")
dataLogFile.write("\n")
dataLogFile.write("started new session")
dataLogFile.close()


##SUBSCRIPTIONS

#to subscribe just type:
#client.subscribe("$SYS/formatted/ <formatted data Channel-name> ")

print("Subscribing to topic","formatted/gear")
client.subscribe("data/formatted/gear") #subscribing to OilPressure Channel

client.loop_forever() #start the loop
