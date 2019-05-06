from collections import OrderedDict
from pymongo import MongoClient
import json

client = MongoClient('localhost', 27017)

client.admin.command('copydb', fromdb='Information_Retrieval', todb='BackupV5')
