#!/usr/bin/env python

# StatusCheck.py - main system status check daemon for h2gc-linux
# Status: basically works.  needs to be daemonized, add rotating log file, rotating data file, tests
#
# Todo: break out all individual checks into their own scripts as below:
#
# Check script must follow rules:
#
# 1) All scripts create a subdirectory named "checkname" with an executable called "checkname" in it.
# 2) All scripts return 0 on success, or a number on fail (1 means possibly a little bad, 100 means must fix immediately).
# 3) Scripts should fill out a section of the .ini file as follows:
#
#    [checkname]
#    description = "what this check does and how it works for end users"
#    status_happy_explanation = "description of what it means for this check to be o.k. for end users"
#    status_sad_explanation = "description of what it means for this check to be o.k. for end users"    
#    url = "http://url the user can go to for help"
#
# Check script optional rules:
# 
# In the check scripts subdirectory, OPTIONALLY include:
#
# teaching.txt - teach user about the check, how it works, and the issue in general
# logfile.txt - detailed ascii log of all checks (StatusCheck.py will truncate for you)
# cron.txt - if this file is here then StatusCheck.py will not run the check, instead it will check the contents of this file for
#            a single integer between 0 and 100, and report that as a result. 
#



import os
import sys
import traceback
import subprocess
import re
import StringIO
import json
import urllib2
import ConfigParser
import storage_checks
import security_checks

class Status:
    def __init__(self):
        self.overall = 0
    def __str__(self):
        return (str(self.overall))


# POST log entry to server
# modifies: status object
#
def post_report(computer, status):
    url = "http://localhost:3000/logs"

    data = json.dumps({"computer": str(computer), "status": str(status)})
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})

    try:
        f = urllib2.urlopen(req)
    except IOError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
            status.overall += 2
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            status.overall += 1
    else:
        print "Successfully posted data."
        response = f.read()
        print "Server says: " + response
        f.close()

# Check the status of storage devices
#
# modifies: storage list
#
def check_storage_status(storage_list):
    mounted_fixed_list=[]
    completed_drive_status_list=[]

    storage_checks.get_mounted_storage_device_info(storage_list)
    storage_checks.get_mounted_fixed_storage_device_data(storage_list, mounted_fixed_list)
    storage_checks.add_device_smart_health(mounted_fixed_list, completed_drive_status_list)

# Check the status of local system security
#
# modifies: security list
#
def check_security_status(security_list, config_file_parser):
    md5item = security_checks.SecurityItem()
    md5item.currmd5 = security_checks.check_shadow_status()
    md5item.lastmd5 = config_file_parser.get('Security', 'shadowmd5', 0)    
    security_list.append(md5item)

# Log the analysis of drives to local log file
# modifies: status object
#
def log_storage_data(sd_ob_list, status):
    result = 0

    for i in sd_ob_list:
        print i
        if i.percentused >= 90:
            result += 5
        if i.smartstatus != "PASSED":
            result += 100
    
    status.overall += result

# Log analysis of security data to local log file
# modifies: status object
#
def log_security_data(sec_ob_list, status):
    
    for item in sec_ob_list:
        print item
        if item.currmd5.strip() != item.lastmd5.strip():
            status.overall += 50
            print "Security status +50 because: " + item.currmd5 + " is NOT the same as: " + item.lastmd5 + "\n"
        else:
            print "Security status adds zero because: " + item.currmd5 + " is the same as: " + item.lastmd5 + "\n"

# Create the minimum config file that will work if none exists
#
#
def init_config_file(parser, config_handle):
    parser.add_section('Security')
    shadow_md5sum = security_checks.check_shadow_status()
    parser.set('Security', 'shadowmd5', shadow_md5sum)
    parser.write(config_handle)
    return parser
    

# Get the config file data into a configparser object
# REFACTOR - more error handling and better usage of configparser
# returns: a configparser object handle or 1 on error
#
def get_config():
    parser = ConfigParser.SafeConfigParser()
    config_dir = os.path.expanduser("~") + "/.h2gc/"
    config_file = "main_config"
    full_config = config_dir + config_file
    
    if not os.path.isdir(config_dir):
        print "Config directory does not exist.  First run assumed.  Creating.  Initializing file."
        os.makedirs(config_dir, mode=0700)
        config_handle = open(full_config, 'w+')
        init_config_file(parser, config_handle)

    try:
        parser.read(full_config)
    except ConfigParser.ParsingError, err:
        print "Can't read config file, error is: ", err
        return 1

    try: 
        md5out = parser.get('Security', 'shadowmd5', 0) 
    except:
        print "Didn't find the security/shadowmd5 option or something like that."     
        return 1

    return parser

################################
#
#
def main():
    status=Status()
    storage_list=[]
    security_list=[]

    config_p=get_config()

    if config_p == 1:
        print "Config file cannot be opened or initialized.  We need a running mode for this situation.  Exiting."
        sys.exit(1)

    # Check system health - log locally
    #
    check_storage_status(storage_list)
    log_storage_data(storage_list, status) 

    check_security_status(security_list, config_p)
    log_security_data(security_list, status)

    # Post overall status to server if available
    #
    post_report("grandma@example.com", status)

    print "Overall status: " + str(status.overall)
    print "Done.\n"

if __name__ == '__main__':
    main()
