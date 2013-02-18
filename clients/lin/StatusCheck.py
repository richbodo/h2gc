#!/usr/bin/env python

# StatusCheck.py - main system status check daemon for h2gc-linux 
# Status: basically works but super primitive and not useful yet
#
# Run as an hourly cron job under linux
#

import pdb
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
def check_security_status(security_list, config_p):
    md5item = security_checks.SecurityItem()
    md5item.currmd5 = security_checks.check_shadow_status()
    md5item.lastmd5 = config_p.get('Security', 'shadowmd5', 0)    
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
# modifies: status object, config file with new md5 if necesary
#
def log_security_data(sec_ob_list, status, config_p):
    
    for item in sec_ob_list:
        print item
        if item.currmd5.strip() != item.lastmd5.strip():
            status.overall += 50
            print "Security status +50 because: " + item.currmd5 + " is NOT the same as: " + item.lastmd5 + "\n"
            pdb.set_trace()
            config_p.set("Security","shadowmd5",item.currmd5)
        else:
            print "Security status adds zero because: " + item.currmd5 + " is the same as: " + item.lastmd5 + "\n"

# Create the minimum config file that will work if none exists
#
#
def init_config_file(parser, config_handle):
    try:
        parser.add_section('Security')
        shadow_md5sum = security_checks.check_shadow_status()
        parser.set('Security', 'shadowmd5', shadow_md5sum)
        #pdb.set_trace()
        parser.write(config_handle)
    except:
        print "Could not initialize parser."
        return 1

    return parser
    

# Get the config file data into a configparser object
# returns: a configparser object handle or 1 on error
#
def get_config(config_handle, full_config):
    parser = ConfigParser.SafeConfigParser()
    
    try:
        parser.read(full_config)
    except ConfigParser.ParsingError, err:
        print "Can't read from config file at all."
        return 1

    try: 
        md5out = parser.get('Security', 'shadowmd5', 0) 
    except:
        print "Didn't find the security/shadowmd5 option or something like that.  Creating new sections."     
        return init_config_file(parser, config_handle)
        
    return parser

################################
#
#
def main():
    status=Status()
    storage_list=[]
    security_list=[]

    # Open/Parse config file
    #
    config_dir = os.path.expanduser("~") + "/.h2gc/"
    config_file = "main_config"
    full_config = config_dir + config_file

    if (os.path.isdir(config_dir) != True):
        print "Config directory does not exist.  First run assumed.  Creating.  Initializing file."
        os.makedirs(config_dir, mode=0700)
    
    # pdb.set_trace()
    # Open, read entire init file in, close
    #    
    config_handle = open(full_config, 'w+')    
    config_p = get_config(config_handle, full_config)
    config_handle.close()

    if config_p == 1:
        print "Config file cannot be initialized.  We need a running mode for this situation.  Exiting."
        sys.exit(1)

    # Check system health - log locally
    #
    check_storage_status(storage_list)
    log_storage_data(storage_list, status) 

    check_security_status(security_list, config_p)
    log_security_data(security_list, status, config_p)

    # Open, write entire init file out, close
    # 
    config_handle = open(full_config, 'w+')
    config_p.write(config_handle)
    config_handle.close()

    # Post overall status to server, if available
    #
    post_report("grandma@example.com", status)

    print "Overall status: " + str(status.overall)
    print "Done.\n"

if __name__ == '__main__':
    main()
