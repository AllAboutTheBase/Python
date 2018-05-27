#!/opt/python/3.6.2/bin/python3
from globalConfig import GlobalConfig
from configParser import ConfigParser

dataPath = "/Users/gr0005/git/Python/sandbox/data"
heiraFile1="sample.yaml"
heiraFull1=dataPath + "//" + heiraFile1 

gc=GlobalConfig(heiraFull1,application='test01', environment='env022', datacenter='me')
gc.loadHeirarchy(application='atg', datacenter='me')
print(gc.paths)
print ("***************** CONSOLIDATED JSON ITERATIVE ***********************")
gc.buildConsolidatedJSON()
gc.printOrderedJSON()
print ("***************** CONSOLIDATED JSON RECURSIVE ***********************")
gc.buildConsolidatedJSONRecursive()
gc.printOrderedJSON()
gc.writeOrderedJSON()

print ("***************** CONFIG PARSER FILTER JSON ***********************")
cp=ConfigParser()
cp.loadJSONDict(gc.jsonMerged)
cp.loadJSONFile(dataPath+"/globalConfigFull.json")
cp.filterJSON()
cp.printOrderedJSON()
cp.writeOrderedJSON(dataPath)

print ("***************** INTERPOLATE KEYS  ***********************")
print ("tbd")