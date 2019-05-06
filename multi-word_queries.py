import sys
import pymongo
from pymongo import MongoClient

import math
import time
import numpy
import json

#Connect to the database
client = MongoClient('localhost', 27017)
db = client.Information_Retrieval
collection = db.td_idf

#get the data from the bookeeping json file
json_file = open("C:\\Users\\shubh\\Dropbox\\CS 121\\Assignment 3\\WEBPAGES\\WEBPAGES_RAW\\bookkeeping.json", "r")
json_data = json.load(json_file)
json_file.close()

#find the intersection of the top 500 documents (based on tf-idf value)
#for each word in the query
def get500Docs(query):
    new_dict = dict(collection.find({"_id": query[0]}).next()["sorted_tf_idf"][:500])
    docs = set(new_dict.keys())
    for index in range(1, len(query)):
        new_dict = dict(collection.find({"_id": query[index]}).next()["sorted_tf_idf"][:500])
        docs = docs.intersection(new_dict.keys())
    return docs

#returns the sum of the tf-idf for each term in the query
def getSum(query, doc_id):
    total = 0
    for word in query:
        total += collection.find({"_id": word}).next()["log_tf_idf"][doc_id]
    return total

#returns the sums of the tf-idf value for each document in
#the top 500 intersection
def labelSums(query, set_of_docs):
    list_of_sums = list()    
    for doc in set_of_docs:  
        tf_idf_sum = getSum(query, doc)
        doc = doc.encode('ascii','ignore').replace("\\", "/")
        list_of_sums.append((doc, tf_idf_sum))    
    return list_of_sums

#converts doc_id to a url
def getUrl(key):
    doc_id = key.encode('ascii','ignore')
    doc_id = doc_id.replace("\\", "/")
    url = json_data[doc_id]    
    return url

#prompt user until the query contains a word
def prompt_user():
    list_of_words = []
    while(len(list_of_words) == 0):
        list_of_words = raw_input("Enter a query: ").split()
    return list_of_words

def find_results(list_of_words):
    start = time.time()
    #if the length of the query is one, lookup the the term in the presorted
    #tf-df column
    if(len(list_of_words) == 1):
        try:
            #find the term in the collection
            cursor = collection.find({"_id": list_of_words[0]})
            #get the list of sorted arrays (0th index is doc_id while 1st index
            #is the tf-idf value)
            queries = cursor.next()['sorted_tf_idf']

            #determine the number of queries to display (at most 15)
            max_prints = 15
            if(len(queries) < 15):
                max_prints = len(queries)
            #prints the top urls for the single word query
            for i in range(0, max_prints):
                doc_id = queries[i][0].encode('ascii','ignore')
                doc_id = doc_id.replace("\\", "/")
                url = json_data[doc_id]
                print(str(i + 1) + ") " + url + "\n")
        except:
            #occurs if there the term does not appear in our database
            print("No results found")
    else:    
        
        try:
            #recieves the intersection of the top 500 documents of each
            #query term (ranking determined by tf-idf value of that document
            #for the term)
            set_of_docs = get500Docs(list_of_words)
            #labelSums returns list of tuples
            #each tuple consists of doc_ids and the tf-idf sum
            #we convert this list into a dictionary for sorting purposes
            doc_dictionary = dict(labelSums(list_of_words, set_of_docs))
            if not doc_dictionary:
                #if doc_dictionary is empty
                print("No results found")
            else:
                i = 1
                #print at most 15 urls
                for key, value in sorted(doc_dictionary.items(), key = lambda x: x[1])[:15]:
                    print(str(i) + ") " + str(getUrl(key)) + "\n")                    
                    i += 1
        except:
            #if any term is not in our database
            print("No results found")
    print("Time Taken: " + str(time.time() - start) + " seconds\n")

if __name__ == '__main__':
    print("Press ctrl+c to quit")
    while (True):
        try:
            list_of_words = prompt_user()        
            find_results(list_of_words)
        except KeyboardInterrupt:
            #user pressed control-c
            sys.exit()
        
        
