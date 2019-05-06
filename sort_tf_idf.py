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
    tf_idf_dict = term['tf_idf']
    list_of_sorted_tf_idf = sorted(tf_idf_dict.items(), key = lambda x: (-x[1], x[0]))
    term['sorted_tf_idf'] = list_of_sorted_tf_idf
    collection.save(term)
    if(counter % 1000 == 0):
        print(counter)
