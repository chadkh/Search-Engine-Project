from HTMLParser import HTMLParser
from collections import defaultdict
import re
import os
import sys
import pymongo
from pymongo import MongoClient

import math

client = MongoClient('localhost', 27017)

db = client.Information_Retrieval
collection = db.td_idf
counter = 0
cursor = collection.find({})
for term in cursor:
    counter += 1
    tf_dict = term['term_frequency_dict']
    tf_idf_dict = defaultdict(float)
    for k,v in tf_dict.items():        
        tf_idf = term['idf'] * v
        tf_idf_dict[k] = tf_idf
    term['tf_idf'] = tf_idf_dict
    collection.save(term)
    if counter % 1000 == 0:
        print(counter)
            
        
