#!/opt/python/3.6.2/bin/python3

import piera

#dataPath = "C:\WS_EAODEPLOY3\Sandbox\data"
dataPath = "/Users/gr0005/git/Python/sandbox/data"
heiraFile1="sample.yaml"
jsonFile2="data2.json"

heiraFull1=dataPath + "//" + heiraFile1 
jsonFile1Full2=dataPath + "//" + jsonFile2

h = piera.Hiera(heiraFull1)

#x=h.get("George_Key", application='test01')
#print (str(x))
#x=h.get("George_Key", application='test01', environment='env1')
#print (str(x))
xx=h.get("apps_to_access", application='test01', environment='env1')
print("***************")
print (str(xx))
print("***************")