#!/opt/python/3.6.2/bin/python3
from globalConfig import GlobalConfig
from configParser import ConfigParser
from interpolation import Interpolate
from convertOld2New import ConvertOld2New

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
cp.loadGlobalConfig(dataPath+"/globalConfigFull.json")
cp.filterJSON('atg')
cp.printOrderedJSON()
cp.writeOrderedJSON(dataPath)


print ("***************** INTERPOLATE KEYS  ***********************")
i=Interpolate()
i.loadGlobalConfig(dataPath+"/globalConfig.tmpl")
i.interpolateDict()
i.printOrderedJSON()
i.writeOrderedJSON(dataPath)
#i.interpolateTemplate(dataPath+"/sample.txt.tmpl")
i.interpolate(dataPath+"/multidir")
#i.interpolate(dataPath+"/multidir/sample.txt.tmpl")


print ("***************** PARTIAL KEYS  ***********************")
cp.jsonFiltered

print ("***************** CONVERT ORIGINAL JSON  ***********************")

co2n=ConvertOld2New()
co2n.ConvertAllJSON()
print ("=============================================================")
print ("=============================================================")
print ("=======================FINISHED==============================")
print ("=============================================================")
print ("=============================================================")
