#!/opt/python/3.6.2/bin/python3
import os
import yaml
import json
from pathlib import Path

class GlobalConfig(object):
    def __init__(self, heira_file, context={}, **kwargs):
        self.heira_file = heira_file
        self.context = context
        self.context.update(kwargs)
        self.rootDataDir=""
        
        self.paths = []

        self.jsonMerged={}
        
    def loadHeirarchy(self, context={}, **kwargs):
        # if context is provided when loading heirarchy vs at object instantiation merge with override the new values
        # this also allows ability to reset/change the context without having to instantiate a new object. 
        self.context.update(context)
        self.context.update(kwargs)
        
        with open(self.heira_file) as f:
            yaml_data = yaml.load(f)
        paths =     yaml_data[":hierarchy"]
        data_dir_key =     yaml_data[":rootPath"]
        root_dir = data_dir_key[":datadir"]
        self.rootDataDir=root_dir
        
        for path in paths[::-1]:
            try: 
                fullPath = path.format(**self.context)
                # if not all the context is provided skip those paths
            except Exception as e:
                print ("Warning: Skipping paths for missing context:"+str(e))
                continue
            fullPath = root_dir+fullPath
            if os.path.exists(fullPath):
                for pth in Path(fullPath).iterdir():
                    if pth.suffix == '.json':
                        self.paths.append(pth)
    
    def mergeJSON(self, baseDict, overrideDict):
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
    
    def buildConsolidatedJSON(self):
        for file in self.paths:
            # load all the json files in hierarchical sequence merging each subsequent one as an override to previously existing keys
            jsonOverride = json.loads(open(file).read())
            self.jsonMerged= self.mergeJSON(self.jsonMerged, jsonOverride)
        
    def mergeJSONRecursive(self,a, b):          
        # if either argument is not a dictionary than just return the second argument -- basically overriding the value of the first value 
        if not isinstance(a, dict) or not isinstance(b, dict):
            return b

        # for each key in the override 
        for key in b.keys():
#      a[key] = merge_map(a[key], b[key]) if key in a else b[key]
            if key in a:
                a[key]=self.mergeJSONRecursive(a[key], b[key])
            else:   
                a[key]=b[key]
        return a

    def buildConsolidatedJSONRecursive(self):
        for file in self.paths:
            # load all the json files in hierarchical sequence merging each subsequent one as an override to previously existing keys
            jsonOverride = json.loads(open(file).read())
            self.jsonMerged= self.mergeJSONRecursive(self.jsonMerged, jsonOverride)
        

    def printOrderedJSON(self):
        print (json.dumps(self.jsonMerged, indent=4, sort_keys=True))
          

    def writeOrderedJSON(self):
        with open(self.rootDataDir+"/globalConfigFull.json", 'w') as fp:
            json.dump(self.jsonMerged, fp,indent=4)
