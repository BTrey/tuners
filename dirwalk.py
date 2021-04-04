#!/usr/bin/python

import os
import sys

try:
    rootDir = sys.argv[1] or '.'
except IndexError:
    rootDir = '.'


for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: %s' % dirName)
    for fname in fileList:
        print('\t%s' % fname)
