#!/opt/python/3.6.2/bin/python3
##

import yaml
import json
import os, pathlib
from collections import OrderedDict

print("Hello World!")
print (os.path.abspath(__file__))
print(os.getcwd())

dataPath = "C:\WS_EAODEPLOY3\Sandbox\data"
jsonFile1="data1.json"
jsonFile2="data2.json"

jsonFile1Full1=dataPath + "\\" + jsonFile1 
jsonFile1Full2=dataPath + "\\" + jsonFile2


def loadData(data):
    print ("Entering --- loadData")
    print ("---------------------")
    print (data)
    json_data = json.loads(open(data).read())  
#    print (json_data)
#    js = json.loads(data)

    print ("Entering --- loadData")
    print ("---------------------")
    return (json_data)
#    return json.loads(data)
#    return json.loads(data, object_pairs_hook=OrderedDict)


print (jsonFile1Full1)
myJSON1 = loadData(jsonFile1Full1)

print ("FIRST JSON FILE--- ")
print ("---------------------")
print (json.dumps(myJSON1, indent=4, sort_keys=True))

myJSON2 = loadData(jsonFile1Full2)

print ("2ND JSON FILE--- ")
print ("---------------------")
print (json.dumps(myJSON2, indent=4, sort_keys=True))

myJSON1.update(myJSON2)

print ("MERGED JSON --- RESULT")
print ("---------------------")
print (json.dumps(myJSON1, indent=4, sort_keys=True))
print ("---------------------")
#print (json.dumps(myJSON2, indent=4, sort_keys=True))

