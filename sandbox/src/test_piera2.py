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

x=h.get("George_Key", application='test01', environment='env03')
print (str(x))


def loadJSONData(data):
    json_data = json.loads(open(data).read())  
    return (json_data)

def merge_map(a,b):
    for key,value in b.items():
        if isinstance(value, dict):
           print(a[key]) 
           print(b[key])
           a[key].update(b[key])  
           print (a[key])
        else:
            if key in a: 
                print (a[key]) 
                print (b[key])
                a[key]=b[key]
            else:
                print (a)
                print(b[key])
                print(key)
                a[key]=value         
    return a                 

def merge_map2(a, b):
    print ("GGGGG:")
    print(a)
    print (b)
    while isinstance(a, dict) or isinstance(b, dict):
        print ("*************IN MERGEMAP*****")
        print ("Now List a::"+str(a))
        print ("Now List b::"+str(b))
        # if either argument is not a dictionary than just return the second argument -- basically overriding the value of the first value 
        #if not isinstance(a, dict) or not isinstance(b, dict):
        #    return b

    # for each key in the override
        Level1B=b.copy()
        Level1A=a.copy() 
        for key in Level1B.keys():
            print("Working This Key:"+key)
            if key in Level1A:
                print ("This Key::"+key+" is in the list::"+str(Level1A))
                print ("a before::"+str(Level1A) +" [] a after::"+str(Level1A[key]))                
                print ("b before::"+str(Level1B) +" [] b after::"+str(Level1B[key]))  
                if isinstance(Level1A, dict) or isinstance(Level1B, dict):
                    Level2B=Level1B.copy()
                    Level2A=Level1A.copy() 
                    for key in Level2B.keys():
                        print("Working This Key:"+key)
                        if key in Level2A:
                            print ("")                    
#                for key in newB.keys():
#                    if key in newA:        
#                        print ("This Key::"+key+" is in the list::"+str(newA))
#                        print ("a before::"+str(newA) +" [] a after::"+str(newA[key]))                
#                        print ("b before::"+str(newB) +" [] b after::"+str(newB[key]))                
 #               print ("Now a is::"+str(a) + " [] Now b is::"+str(b))
            else:
                print ("a before::"+str(a) +" [] a after::"+str(b[key]))
#                a=newB[key]
        
        print ("Leaving For Loop Key:  No More keys")        
        
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
            a[key]=merge_map_original(a[key], b[key])
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
        newpath = path.format(environment="env03", application="test0222", clientcert="", datacenter="")
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
#        mergedJSON2= merge_map_original(mergedJSON2, myJSON)        
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