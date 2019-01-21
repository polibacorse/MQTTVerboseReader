#!/usr/bin/python3

import paho.mqtt.client as mqtt  # import the client1
import datetime
import argparse
import json

# Printing Received Data Function
enable = False
datalog = None
args = None

def on_message(client, userdata, message):
    global enable
    global datalog

    if message.topic == 'data/formatted/datalog_on-off':
        payload = json.loads(message.payload.decode('UTF-8'))
        
        if enable != payload['value']:
            if payload['value'] == True:
                datalog = open("datalog.txt", "a");
                datalog.write("\nStarted new session at {}".format(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
            else:
                datalog.close();

        enable = payload['value']

    if not enable:
        return

    # TODO: Open the file at program startup. Close it on SIGINT or flush periodically.
    # TODO: verify that file will be created with 'a' mode if it does not exist.
    datalog.write('\n{}: {}'.format(message.topic, message.payload.decode('utf-8')))
        
    if args.verbose:
        print(message.topic, "says: ", str(message.payload.decode("utf-8")))
        

def main():
    global datalog
    global args

    print("creating new instance")

    client = mqtt.Client("VerboseReader") 
    client.on_message = on_message  # attach function to callback

    print("connecting to broker")
    client.connect("localhost")  # connect to broker


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

    client.loop_forever()  # start the loop

if __name__ == '__main__':
    main()

