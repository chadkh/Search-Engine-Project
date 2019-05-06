import re
import os
import sys
import pymongo
from pymongo import MongoClient
import json

word = raw_input("Enter a query: ").lower()

client = MongoClient('localhost', 27017)

db = client.Information_Retrieval
collection = db.td_idf

try:
    cursor = collection.find({"_id": word})
    queries = cursor.next()['sorted_tf_idf']
    max_prints = 10
    if(len(queries) < 10):
        max_prints = len(queries)
    json_file = open("C:\\Users\\shubh\\Dropbox\\CS 121\\Assignment 3\\WEBPAGES\\WEBPAGES_RAW\\bookkeeping.json", "r")
    json_data = json.load(json_file)
    for i in range(0, max_prints):
        doc_id = queries[i][0].encode('ascii','ignore')
        doc_id = doc_id.replace("\\", "/")
        url = json_data[doc_id]
        print(str(i + 1) + ") " + url)
        #print(queries[i][0])
    


except StopIteration:
    print("No results found for query " + word)

except:
    print("FATAL ERROR")
