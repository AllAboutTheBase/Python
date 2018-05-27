#!/opt/python/3.6.2/bin/python3

import json

class ConfigParser(object):
    def __init__(self, criteria=[]):
        self.criteria=criteria
        self.jsonData={}
        self.jsonFiltered={}
        
    def loadJSONFile(self, jsonFile):
        self.jsonData = json.loads(open(jsonFile).read())
            
    def loadJSONDict(self, jsonDict):
        self.jsonData = jsonDict
        
    def isKeyEligible(self, listCriteria1, listAttributes):
        for criteria in listCriteria1:
            if criteria in listAttributes:
                return True
        return False
    
    def filterJSON(self):
        for key,value in self.jsonData.items():
            if isinstance(value, dict):
                if "apps_to_access" in value:
                    if self.isKeyEligible(["GLOBAL","app1"], value["apps_to_access"]):
                        self.jsonFiltered[key] = value["value"]
                                  
    def printOrderedJSON(self):
        print ("===================================================")    
        print ("===================================================")  
        print (json.dumps(self.jsonFiltered, indent=4, sort_keys=True))

    def writeOrderedJSON(self, globalConfigPath):
        print ("===================================================")    
        print ("===================================================")  
        with open(globalConfigPath+"/globalConfig.tmpl", 'w') as fp:
            json.dump(self.jsonFiltered, fp,indent=4)
