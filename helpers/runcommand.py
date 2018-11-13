import os
import sys
from pymongo import MongoClient

command = sys.argv[1]

#client = MongoClient("mongodb://reader:%s@127.0.0.1:27017/dax"%os.environ["MONGO_PASSWORD"])
client = MongoClient("mongodb://dax:%s@ds129770.mlab.com:29770/dax"%os.environ["MONGO_PASSWORD"])

db = client['dax']
collection = db['control']

try:
    hostname = sys.argv[2]
except:
    hostname = os.uname()[1]
    print("No hostname provided so assuming it's running locally at %s"%hostname)

hostname = ['fdaq00_0', 'fdaq00_1']

try:
    run_num = int(sys.argv[4])
except:
    run_num = 1
    print("Didn't provide a run number so trying 1")


doc = {}
if command == 'start':
    
    doc = {
        "detector" : "TPC",
        "command": "start",
        "run": run_num,
        "mode": "test",
        "host": hostname,
        "user": os.getlogin()        
    }
    
elif command == 'stop':

    doc = {
        "command": "stop",
        "host": hostname,
        "user": os.getlogin()
    }

elif command == 'arm':

    try:
        runmode = sys.argv[3]
    except:
        runmode = 'test'
        print("Didn't provide a run mode so trying 'test'")

    doc = {
        "mode": runmode,
        "command": "arm",
        "host": hostname,
        "user": os.getlogin()
    }
                   
else:
    print("Usage: python runcommand.py {start/stop/arm} {host} {runmode} {run}")
    exit(0)

try:
    collection.insert(doc)
    print("Command sent!")
except Exception as e:
    print("Failed!")
    print(str(e))
