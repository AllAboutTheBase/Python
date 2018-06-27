#!/opt/python/3.6.2/bin/python3
import os
import yaml
import json
from pathlib import Path
from datetime import date
import datetime

class ConvertOld2New(object):
    def __init__(self):
        
        self.paths = []

        self.jsonMerged={}  
        self.jsonNEW={}
    def MakeDict(self, key, value):
        newDict={}
        newDict["value"]=value
        newDict["apps_to_access"]=list({"global","atg"})
        newDict["type"]="string"
        newDict["description"]= "tbd"
        newDict["encryption"]=0
        newDict["primary application"]= "??"
        newDict["author"]= "george"
        newDict["created_date"]= str(datetime.datetime.now())
        newDict["last_modified"]= str(datetime.datetime.now())

        return newDict
            
    def ConvertJSON(self, myDict):       
        # loop thru each key on level of override dictionary
        for key1,value1 in myDict.items():
            if isinstance(value1, dict):
                for key2,value2 in value1.items():
                    if isinstance(value2, dict):
                        for key3,value3 in value2.items():
                            if isinstance(value3, str):
                                self.jsonNEW[key1+"."+key2+"."+key3]=self.MakeDict(key1+"."+key2+"."+key3,value3)
                            else:
                                print("COULD NOT EVALUATE: key:"+key1 +"key2:"+key2+"key3:"+key3 )
                    else:
                        if isinstance(value2, str):
                            self.jsonNEW[key1+"."+key2]=self.MakeDict(key1+"."+key2,value2)
                        else:
                            print("COULD NOT EVALUATE: key:"+key1 +"key2:"+key2)
            else:
                if isinstance(value1, str):
                    self.jsonNEW[key1]=self.MakeDict(key1,value1)
                    #self.jsonNEW[key1]=value1
                else:
                    print("COULD NOT EVALUATE: key:"+key1 )                        

        return myDict       
    
    def ConvertAllJSON(self):
            file = "/Users/gr0005/git/Python/sandbox/data/environment/production/atg.json"
            myJSON = json.loads(open(file).read())
            self.ConvertJSON(myJSON)   
            self.printOrderedJSON()     

    def printOrderedJSON(self):
        print (json.dumps(self.jsonNEW, indent=4, sort_keys=True))
          

    def writeOrderedJSON(self):
        with open(self.rootDataDir+"/globalConfigFull.json", 'w') as fp:
            json.dump(self.jsonMerged, fp,indent=4)
