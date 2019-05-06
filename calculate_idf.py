from HTMLParser import HTMLParser
from collections import defaultdict
import re
import os
import sys
import pymongo
from pymongo import MongoClient

import math

#Connect to the local database
client = MongoClient('localhost', 27017)
db = client.Information_Retrieval
collection = db.td_idf

#counter variable for debugging purposes
counter = 0
cursor = collection.find({})            
for term in cursor:
    counter += 1
    number_of_docs = term['number_of_docs']
    idf = math.log10(37500.0 / number_of_docs)
    term['idf'] = idf
    #if statement used for debugging purposes
    if (counter % 1000 == 0):
        print(counter)
    collection.save(term)
