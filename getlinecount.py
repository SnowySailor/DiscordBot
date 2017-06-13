#!/usr/local/bin/python3.5

import sys
import os

def main(argv):
    if len(argv) < 3:
        sys.exit("Not enough arguments. \nUsage: getlinecount.py [file] [sentencelength]")
    file = argv[1]
    if not os.path.isfile(file):
        sys.exit("{} is not a valid file.".format(file))

    try:
        length = int(argv[2])
    except ValueError:
        sys.exit("Integer required as second argument. \nUsage: getlinecount.py [file] [sentencelength]")

    count = 0
    with open(file, "r", encoding="utf-8", errors="ignore") as fileHandle:
        data = fileHandle.read()
        lines = data.split("\n")
        count = len([x for x in lines if len(x.split()) >= length])

    print("Lines with more than {} words in {}: {}".format(length, file, count))
    return

main(sys.argv)