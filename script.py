from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
import time
import json
from os.path import dirname, join
from csv import reader

serviceUsername = "5849c9b8-7990-4a3e-9b69-934dad3cf956-bluemix"
servicePassword = "23fd529c3cfe8a54c19419ad83207f0806de2574d8ed1dc45cc69f898aecfb76"
serviceURL = "https://5849c9b8-7990-4a3e-9b69-934dad3cf956-bluemix:23fd529c3cfe8a54c19419ad83207f0806de2574d8ed1dc45cc69f898aecfb76@5849c9b8-7990-4a3e-9b69-934dad3cf956-bluemix.cloudantnosqldb.appdomain.cloud"

dbName = "soa"

client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
client.connect()

myDatabaseDemo = client[dbName]

file = "database.csv"
dest_topic = "SOATopic"

# in seconds
PERIOD = 5

try:
    with open(file, 'r') as read_obj:

        # pass the file object to reader() to get the reader object
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
                        "RH_percent": RH,
                        "topic": dest_topic
            }
            
            # Create a document using the Database API.
            newDocument = myDatabaseDemo.create_document(json_object)
            
            print(json_object)
            time.sleep(PERIOD)
            
except Exception as err:
    print(err)   
    
#python3 app.py "broker-5-1xx3ppkpxl38hmh1.kafka.svc03.us-south.eventstreams.cloud.ibm.com:9093,broker-4-1xx3ppkpxl38hmh1.kafka.svc03.us-south.eventstreams.cloud.ibm.com:9093,broker-1-1xx3ppkpxl38hmh1.kafka.svc03.us-south.eventstreams.cloud.ibm.com:9093,broker-0-1xx3ppkpxl38hmh1.kafka.svc03.us-south.eventstreams.cloud.ibm.com:9093,broker-2-1xx3ppkpxl38hmh1.kafka.svc03.us-south.eventstreams.cloud.ibm.com:9093,broker-3-1xx3ppkpxl38hmh1.kafka.svc03.us-south.eventstreams.cloud.ibm.com:9093" "https://1xx3ppkpxl38hmh1.svc03.us-south.eventstreams.cloud.ibm.com" "Rq2vCQH4OMgL-p-Ll9kVISdLOhAFIVDIo02QI_eYgxPJ" "/etc/ssl/certs" -consumer
