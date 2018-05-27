#!/opt/python/3.6.2/bin/python3

import yaml
import os
from pathlib import Path
import json

dataPath = "/Users/gr0005/git/Python/sandbox/data"
heiraFile1="sample.yaml"
jsonFile2="data2.json"

heiraFull1=dataPath + "//" + heiraFile1 
jsonFile1Full2=dataPath + "//" + jsonFile2

def loadJSONData(data):
    json_data = json.loads(open(data).read())  
    return (json_data)

def mergeJSON(baseDict,overrideDict):
    # loop thru each key on level of override dictionary
    for key,value in overrideDict.items():
        # if the value of key is a dictionary traverse the value 
        if isinstance(value, dict):
            # update the base dictionary for the specific key with the value in the overideDict - this is a dictionary merge
            if key in baseDict: 
                baseDict[key].update(overrideDict[key])
            else:
                baseDict[key]=overrideDict[key]  
        else:
            # When the value of key is not a dictionary and exists in the base dictionary update the value with the value from overrideDict
            if key in baseDict: 
                baseDict[key]=overrideDict[key]
            # When the key is not in the baseDict add it as new key value pair
            else:
                baseDict[key]=value         
    return baseDict                 

def readYaml():
    with open(heiraFull1) as f:
        yaml_data = yaml.load(f)
        print (yaml_data)
    paths =     yaml_data[":hierarchy"]
    json_data_dir =     yaml_data[":json"]
    json_root = json_data_dir[":datadir"]
        
    json_paths = []
    for path in paths[::-1]:
        newpath = path.format(environment="env03", application="test0222", clientcert="", datacenter="")
        newpath = json_root+newpath
        if os.path.exists(newpath):
            for pth in Path(newpath).iterdir():
                if pth.suffix == '.json':
                    json_paths.append(pth) 
    mergedJSON2=""
    for file in json_paths:
        myJSON = loadJSONData(file)
        if mergedJSON2 == "":
            mergedJSON2 = myJSON.copy()
        mergedJSON2= mergeJSON(mergedJSON2, myJSON)
    print ("===================================================")    
    print ("===================================================")  
    print (json.dumps(mergedJSON2, indent=4, sort_keys=True))  
    
readYaml()