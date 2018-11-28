import os
import csv
import re

def createMap():
    resultMap = {}
    with open('result.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            resultMap[row[11]] = row[4]
    return resultMap

def getDir():
    directory = input("Enter location of the files")
    path = r"%s" % directory
    return path;

def readFiles(path, pattern, replace):
    for file in os.listdir(path):
        current_file = os.path.join(path, file)
        if not any(value in current_file for value in (".git", ".DS_Store", "css", "fonts","mock","assets", "script", "img", "protobuf")):
            if(os.path.isfile(current_file)):
                with open(current_file, "rb") as r:
                    lineslist = r.readlines()
                with open(current_file, "w") as w:
                    for l in lineslist:
                        l = l.decode('utf8')
                        l = re.sub(pattern, replace, l)
                        w.write(l)
            else:
                readFiles(current_file, pattern, replace)

def init():
    path = getDir();
    keyMap = createMap();
    for key in keyMap:
        readFiles(path, r'\b%s\b' %key, keyMap[key])

init()
