from HTMLParser import HTMLParser
from collections import defaultdict
import re
import os
import sys
import pymongo
from pymongo import MongoClient

#Code from python documentation
class MyHTMLParser(HTMLParser):
    content = True
    doc_id = ""
    
    my_dict_tf = defaultdict(int)
    def handle_starttag(self, tag, attrs):        
        if(tag == "style" or tag == "script"):            
            self.content = False
            

    def handle_endtag(self, tag):        
        if(tag == "style" or tag == "script"):            
            self.content = True

    def handle_data(self, data):
        stripped_data = data.strip().lower()        
        if self.content and stripped_data != '':
            wordList = re.findall('([a-z0-9]+)', stripped_data)
            for word in wordList: 
                self.my_dict_tf[word] += 1
                
            
            



rootdir = "C:\\Users\\shubh\\Dropbox\\CS 121\\Assignment 3\\WEBPAGES\\WEBPAGES_RAW"

#Connect to the local MongoDB database
client = MongoClient('localhost', 27017)
db = client.Information_Retrieval
collection = db.td_idf

#keep track of all the tokens we encounter
list_of_terms = set()

for subdir, dirs, files in os.walk(rootdir):    
    doc_id = defaultdict(set)
    for this_file in files:
        parser = MyHTMLParser()
        #is statement makes sure that the file is not the bookkeping file
        if not (this_file.endswith("json") or this_file.endswith("tsv")):    
            #current_file is the opened file 
            #file_name is the doc_id (format is folder_number\file_number)
            current_file = open(str(subdir) + "\\" + str(this_file), "r")
            file_name = subdir[subdir.rfind("\\") + 1:] + "\\" + this_file            
            print(file_name)
            
            #updating the parser with the doc_id and reseting the dictionary
            parser.doc_id = file_name
            parser.my_dict_tf = defaultdict(int)

            #by default the parser should start by reading content
            parser.content = True
            parser.feed(current_file.read().decode("utf-8"))

            #update our database based on the tokens we recieved from the
            #webpage
            for k,v in parser.my_dict_tf.items():
                append_to_db = dict()
                #if the term k is not in our database, add a new row to the database
                if k not in list_of_terms:
                    list_of_terms.add(k)
                    #set id equal to the term
                    #the term frequency dict has doc_id for the key and
                    #the tern frequency for value
                    append_to_db["_id"] = k
                    append_to_db["term_frequency_dict"] = dict({file_name : v})
                    append_to_db["number_of_docs"] = 1
                    collection.save(append_to_db)
                #if k is in the database we find it in the collection and modify
                #the values
                else:
                    cursor = collection.find({"_id": k})
                    dict_in_db = cursor.next()
                    dict_in_db["term_frequency_dict"].update(dict({file_name : v}))
                    dict_in_db["number_of_docs"] += 1
                    collection.save(dict_in_db)
                    
            
            
    
            
    

