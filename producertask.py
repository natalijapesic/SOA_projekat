"""
 Copyright 2015-2018 IBM

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

 Licensed Materials - Property of IBM
 © Copyright IBM Corp. 2015-2018
"""
import asyncio
from confluent_kafka import Producer
import time
import json
from os.path import dirname, join
from csv import reader

class ProducerTask(object):

    def __init__(self, conf, topic_name):
        self.topic_name = topic_name
        self.producer = Producer(conf)
        self.counter = 0
        self.running = True

    def stop(self):
        self.running = False

    def on_delivery(self, err, msg):
        if err:
            print('Delivery report: Failed sending message {0}'.format(msg.value()))
            print(err)
            # We could retry sending the message
        else:
            print('Message produced, offset: {0}'.format(msg.offset()))

    @asyncio.coroutine
    def run(self):
        print('The producer has started')
        file = "database.csv"
                
        try:
            with open(file, 'r') as read_obj:
                csv_reader = reader(read_obj)
                # Iterate over each row in the csv using reader object
                # row variable is a list that represents a row in csv
                for (i, row) in enumerate(csv_reader):
                    if i == 0:
                        continue
                        
                    soil = row[2]
                    airT = row[3]
                    RH = row[4]
                        
                    json_object = {
                                "tSoil_C_hummock": soil,
                                "tAir_C": airT,
                                "RH_percent": RH                    
                    }
                    
                    json_object = json.dumps(json_object)
            
                    key = 'key'
                    sleep = 5 # Sleep for flow control
                    try:
                        self.producer.produce(self.topic_name, json_object, key, -1, self.on_delivery)
                        self.producer.poll(0)
                        self.counter += 1
                    except Exception as err:
                        print('Failed sending message {0}'.format(json_object))
                        print(err)
                        sleep = 10 # Longer sleep before retrying
                    yield from asyncio.sleep(sleep) 
        except Exception as err:
            print(err)
        self.producer.flush()

