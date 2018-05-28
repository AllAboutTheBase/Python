#!/opt/python/3.6.2/bin/python3

import json
import os
import re

class Interpolate(object):
    def __init__(self, criteria=[]):
        self.criteria=criteria
        self.globalConfig={}
        self.interpolationComplete=False
        self.basePath=""
        self.templateFilename=""
        self.fullFileName=""
        self.startDelim="{{"
        self.endDelim="}}"
        self.tmpl_exten = '.tmpl'

            
    def loadGlobalConfig(self, fullJSONFile):
        self.globalConfig = json.loads(open(fullJSONFile).read())
        self.basePath, self.templateFilename = os.path.split(fullJSONFile)
        self.fullFileName=fullJSONFile
        
    def interpolateDict(self):
        regex = re.compile(r'('+ self.startDelim + '[0-9a-zA-Z_-\|]+'+self.endDelim +')')
        
        for key,value in self.globalConfig.items():
            tokenList=regex.findall(value)
            tokenList= set(tokenList)     # unique token list
            replacedValue=value
            for token in tokenList:
                tokenKey = token.replace(self.startDelim, "")
                tokenKey= tokenKey.replace(self.endDelim,"")
                replacedValue = replacedValue.replace(token, self.globalConfig[tokenKey])
            self.globalConfig[key]=replacedValue

    def interpolateTemplate(self, fullTmplFile):
        regex = re.compile(r'('+ self.startDelim + '[0-9a-zA-Z_-\|]+'+self.endDelim +')')
        newFullTmplFile = fullTmplFile.split(self.tmpl_exten)[0]
        with open(fullTmplFile,'r') as fInput:
            with open(newFullTmplFile,'w') as fOutput:
                for line in fInput:
                    line = line.rstrip('\n')
                    tokenList=regex.findall(line)
                    tokenList= set(tokenList)     # unique token list
                    newLine=line
                    for token in tokenList:
                        tokenKey = token.replace(self.startDelim, "")
                        tokenKey= tokenKey.replace(self.endDelim,"")
                        newLine = newLine.replace(token, self.globalConfig[tokenKey])
                    print(newLine, file=fOutput)              

    def interpolate(self, path):
        if os.path.isdir(path):
            for dirPath, dirNames, fileNames in os.walk(path, followlinks=False):
                for fileName in fileNames:
                    if fileName.lower().endswith(self.tmpl_exten):
                        self.interpolateTemplate(os.path.join(dirPath,fileName))
        else:
            self.interpolateTemplate(path)

    def printOrderedJSON(self):
        print (json.dumps(self.globalConfig, indent=4, sort_keys=True))
        
    def writeOrderedJSON(self, globalConfigPath):
        with open(globalConfigPath+"/globalConfig.json", 'w') as fp:
            json.dump(self.globalConfig, fp,indent=4)
