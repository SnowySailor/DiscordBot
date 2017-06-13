#!/usr/local/bin/python3.5

import sys
import os

def main(argv):
    if len(argv) < 3:
        sys.exit("ERROR: Not enough arguments.\n\n"+str(getUsage()))
    file = argv[1]
    if not os.path.isfile(file):
        sys.exit("{} is not a valid file.".format(file))

    try:
        length = int(argv[2])
    except ValueError:
        sys.exit("ERROR: Integer required as second argument.\n\n"+getUsage())

    count = 0
    with open(file, "r", encoding="utf-8", errors="ignore") as fileHandle:
        data = fileHandle.read()
        lines = data.split("\n")
        count = len([x for x in lines if len(x.split()) >= length])
        exactCount = len([x for x in lines if len(x.split()) == length])

    if (len(argv) > 3 and argv[3] != 'ET') or (len(argv) == 3):
        print("Lines with more than {} words in {}: {}".format(length, file, count))
    if(len(argv) == 4 and argv[3] == 'ET'):
        print("Lines with exactly {} words in {}: {}".format(length, file, exactCount))
    return

def getUsage():
    return ("Usage: getlinecount.py FILE SENTENCELENGTH [GT/ET]\n"+
           "GT finds lines with 'at least' SENTENCELENGTH words.\n"+
           "ET finds lines with exactly SENTENCELENGTH words.")

main(sys.argv)
