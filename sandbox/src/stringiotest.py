#!/opt/python/3.6.2/bin/python3
import configparser
from configparser import ConfigParser
#from ConfigParser import ConfigParser
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

ini_path="dhfhgfhf"

ini_str = '[root]\n' + open(ini_path, 'r').read()
ini_fp = StringIO.StringIO(ini_str)
config = ConfigParser.RawConfigParser()
config.readfp(ini_fp)