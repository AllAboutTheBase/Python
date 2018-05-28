#!/opt/python/3.6.2/bin/python3

import json

class ConfigParser(object):
    def __init__(self, criteria=[]):
        self.criteria=criteria
        self.globalConfig={}
        self.jsonFiltered={}
        self.application=""
        
    def loadGlobalConfig(self, jsonFile):
        self.globalConfig = json.loads(open(jsonFile).read())
            
    def loadJSONDict(self, jsonDict):
        self.globalConfig = jsonDict
        
    def isKeyEligible(self, listCriteria1, listAttributes):
        for criteria in listCriteria1:
            if criteria in listAttributes:
                return True
        return False
    
    def filterJSON(self, application):
        self.application=application
        for key,value in self.globalConfig.items():
            if isinstance(value, dict):
                if "apps_to_access" in value:
                    if self.isKeyEligible(["GLOBAL",self.application], value["apps_to_access"]):
                        self.jsonFiltered[key] = value["value"]
                                  
    def printOrderedJSON(self):
            
          
        print (json.dumps(self.jsonFiltered, indent=4, sort_keys=True))

    def writeOrderedJSON(self, globalConfigPath):
            
          
        with open(globalConfigPath+"/globalConfig.tmpl", 'w') as fp:
            json.dump(self.jsonFiltered, fp,indent=4)
