import os
import sys

rootdir = "C:\\Users\\shubh\\Dropbox\\CS 121\\Assignment 3\\WEBPAGES\\WEBPAGES_RAW"
number_of_files = 0;
for subdir, dirs, files in os.walk(rootdir):
    for this_file in files:
        if not (this_file.endswith("json") or this_file.endswith("tsv")):
            number_of_files += 1

print(number_of_files)
