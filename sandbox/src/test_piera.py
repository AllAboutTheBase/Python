#!/opt/python/3.6.2/bin/python3

import piera
import yaml
import re
import os
from pathlib import Path
import json

#dataPath = "C:\WS_EAODEPLOY3\Sandbox\data"
dataPath = "/Users/gr0005/git/Python/sandbox/data"
heiraFile1="sample.yaml"
jsonFile2="data2.json"

heiraFull1=dataPath + "//" + heiraFile1 
jsonFile1Full2=dataPath + "//" + jsonFile2

h = piera.Hiera(heiraFull1)

#x=h.get("George_Key", application='test01')
#print (str(x))
x=h.get("George_Key", application='test01', environment='env03')
print (str(x))
xx=h.get("apps_to_access", application='test01', environment='env01')
print("***************")
print (str(xx))
print("***************")
xx=h.get("MyTest", application='test01', environment='env01')
print("***************")
print (str(xx))
print("***************")
xx=h.get("integer1", application='test01', environment='env01')
print("***************")
print (str(xx))
print("***************")


def loadJSONData(data):
    json_data = json.loads(open(data).read())  
    return (json_data)

def merge_map(a, b):
    print ("GGGGG:")
    print(a)
    print (b)
    while isinstance(a, dict) or isinstance(b, dict):
        print ("*************IN MERGEMAP*****")
        print (a)
        print (b)
        # if either argument is not a dictionary than just return the second argument -- basically overriding the value of the first value 
        #if not isinstance(a, dict) or not isinstance(b, dict):
        #    return b

    # for each key in the override 
        for key in b.keys():
            print("Printing key:"+key)
            print (key)
#      a[key] = merge_map(a[key], b[key]) if key in a else b[key]
#      a[key] = merge_map(a[key], b[key]) 
            if key in a:
                a=a[key]
                #b=b[key]
                print ("%%%%%%%%")
                print (a)
                print(b)
            else:
                a=b[key]
    return a

def merge_map_original(a, b):
    print ("*************IN MERGEMAP*****")
    print (a)
    print (b)
    # if either argument is not a dictionary than just return the second argument -- basically overriding the value of the first value 
    if not isinstance(a, dict) or not isinstance(b, dict):
        return b

    # for each key in the override 
    for key in b.keys():
#      a[key] = merge_map(a[key], b[key]) if key in a else b[key]
#      a[key] = merge_map(a[key], b[key]) 
        if key in a:
            a[key]=merge_map(a[key], b[key])
        else:
            a[key]=b[key]
    return a

def readYaml():
    with open(heiraFull1) as f:
        yaml_data = yaml.load(f)
        print (yaml_data)
    paths =     yaml_data[":hierarchy"]
    json_data_dir =     yaml_data[":json"]
    json_root = json_data_dir[":datadir"]
    print("^^^^^^^^^")
    print (json_root) 
    print("^^^^^^^^^")
    print (paths)
    
    interpolate = re.compile(r'''%\{(?:::|)([^\}]*)\}''')

    rformat = re.compile(r'''%{(?:::|)([a-zA-Z_-|\d]+)}''')
    
    json_paths = []
    for path in paths[::-1]:
        print ("-->"+path)
        newpath = path.format(environment="env02", application="atg", clientcert="", datacenter="")
        #newpath= rformat.sub("ITWORKS!!!", path)
        newpath = json_root+newpath
        print("$$$$$$$$$$$$$$$")
        print ("*****"+newpath)
        #if os.path.isdir(newpath):
        if os.path.exists(newpath):
            for pth in Path(newpath).iterdir():
                if pth.suffix == '.json':
                    json_paths.append(pth) 
    print ("*******   ALL THE JSON PATHS")   
    print(json_paths)
    print("")
    print("")
    mergedJSON=""
    mergedJSON2=""
    for file in json_paths:
        print ("############## STARTING MERGE #################")
        print(file)
        myJSON = loadJSONData(file)
        print (myJSON)
        if mergedJSON == "":
            mergedJSON = myJSON
            mergedJSON2 = myJSON.copy()
        mergedJSON.update(myJSON)
        print ("BEFORREE")
        print (mergedJSON2)
        print ("-------")
        print (myJSON)
        mergedJSON2= merge_map(mergedJSON2, myJSON)
        print ("$$$$$$$$$$$$$$  SO FAR #################")
        print(mergedJSON)
        print("------------------------------------------")
        print(mergedJSON2)
        print ("##############  SO FAR #################")
    print ("===================================================")    
    print ("===================================================")  
    print (json.dumps(mergedJSON, indent=4, sort_keys=True))  
    print("------------------------------------------")
    print (json.dumps(mergedJSON2, indent=4, sort_keys=True))  
    
readYaml()