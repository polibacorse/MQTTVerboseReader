#!/usr/bin/python3

import paho.mqtt.client as mqtt  # import the client1
import time
import argparse
import json

# Printing Received Data Function


def on_message(client, userdata, message):

    # TODO: Open the file at program startup. Close it on SIGINT or flush periodically.
    # TODO: verify that file will be created with 'a' mode if it does not exist.
    with open('datalog.txt', 'a') as f:
        f.write('\n{}: {}'.format(message.topic, message.payload.decode('utf-8')))
        
    if args.verbose:
        print(message.topic, "says: ", str(message.payload.decode("utf-8")))
        

########################################


print("creating new instance")


client = mqtt.Client("VerboseReader") 
client.on_message = on_message  # attach function to callback

print("connecting to broker")
client.connect("localhost")  # connect to broker
dataLogFile = open("dataLog.txt", "a")
dataLogFile.write("\n")
dataLogFile.write("started new session")
dataLogFile.close()


# SUBSCRIPTIONS

# to subscribe just type:
# client.subscribe("data/formatted/ <formatted data Channel-name> ")

print("Subscribing")
client.subscribe("data/formatted/#")
client.subscribe("data/raw")


# code to handle verbose mode
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="shows output", action="store_true");
args = parser.parse_args()
###############################################

client.loop_forever()  # start the loop
