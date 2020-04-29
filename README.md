# SOA_projekat
Overview of the demo

The data is read from the sensor and sent to the cloud. 
The record is then saved to Cloudant database instance and when this happens the trigger is fired. 
This triggers the sequence of actions in the following order:
1. read action - that will read the new data record from the database and send the result to the analyze action
2. analyze action - that will analyze the given record and based on data it received prepare the response message 
(if soil is too dry it will send message to turn on the irrigation system, or if it is at the optimal level to turn the system off)
3. publish action - that will receive the response and publish it to the designated Kafka topic
The Consumer app waits for the messages published to the Kafka topic to which is subscribed and based on the content of the message
it can take an appropriate action (here for this demo it only prints the content of the message received)

Trigger and sequence with actions are created and connected through web based interface. 
For this part the code for analyze action is provided and for the read and publish actions it isn't as they are already implemented as
part of Cloudant database and Kafka Event Streams.
IBM Cloud platform was used (Bluemix) and parts of the platform used are OpenWhisk, Kafka, and Cloudant.

Requirements

Python 3.6+ with pip
IMPORTANT: run pip install -r requirements.txt
to install the required libraries

How to start demo

To start the app that sends the data to the database run script.py from the terminal.
To start the Consumer app just copy paste the text command from startConsumer.txt to terminal. 
The command given is for Ubuntu based Operating Systems.
