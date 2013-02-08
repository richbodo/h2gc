#!/usr/bin/env python
import os
import subprocess
import re
import StringIO
import json
import urllib2
import random
import math

class StorageDevice:
    def __init__(self):
        self.devname = 0
        self.removable = 0
        self.mounted = 0
        self.percentused = 0
        self.smartcapable = 0
        self.smartreport = "TBD"
        self.smartstatus = "TBD"

def putstuffinobjects():
    foo = 11
    myobjectlist=[]
    for count in xrange(1,foo):
        print "Storing in object: " + str(count)
        x = StorageDevice()
        x.devname = count
        x.smartreport = "foo" if math.ceil(random.random()) else "bar"
        x.smartstatus = "baz" if math.ceil(random.random()) else "blah"
        myobjectlist.append(x)
    return myobjectlist
     
def printstuffoutofobjects(olist):
    for sdevice in olist:
        print "Storage device name: " + str(sdevice.devname)
        print "SMART report: " + str(sdevice.smartreport)
        print "SMART status: " + str(sdevice.smartstatus)

def main():
    print "Start." + str(math.ceil(random.random()))
    printstuffoutofobjects(putstuffinobjects())
    print "Done." + str(math.ceil(random.random()))

if __name__ == '__main__':
    main()
