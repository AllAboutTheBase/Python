#!/opt/python/3.6.2/bin/python3

import piera
import yaml
import re
import os
from pathlib import Path
import json

mystring ="1  2  3 4     5 6 7 8 9"
mystring = re.sub(' +', ' ',mystring)
listOfValues = mystring.split(' ')
print ('----START-----')
for oneValue in listOfValues:
    print(oneValue)
print ('----END-----')
