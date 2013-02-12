#!/usr/bin/env python
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

# POST log entry to server
#
# NOTE: every time we fail to reach a serve we should add one to the overall status
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
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
    else:
        print "Successfully posted data."
        response = f.read()
        print "Server says: " + response
        f.close()

# Check the status of storage devices
#
# returns: 0 if all drives are o.k., 1 or more if any drive is problematic
#
def check_storage_status(storage_list):
    drive_status=0
    mounted_fixed_list=[]
    completed_drive_status_list=[]

    storage_checks.get_mounted_storage_device_info(storage_list)
    storage_checks.get_mounted_fixed_storage_device_data(storage_list, mounted_fixed_list)
    storage_checks.add_device_smart_health(mounted_fixed_list, completed_drive_status_list)

    return drive_status

# Check the status of local system security
#
# returns: 0 if no prob found, 1 or more if any issue is found
#
def check_security_status(security_list, config_file_parser):
    security_status = 0

    print "checking security status."
    current_md5 = security_checks.check_shadow_status()
    stored_md5 = config_file_parser.get('Security', 'shadowmd5', 0)
    if current_md5.strip() != stored_md5.strip():
        security_status += 50
        print "Security status is 50 because: " + current_md5 + " is NOT the same as: " + stored_md5
    else:
        print "Security status is still zero because: " + current_md5 + " is the same as: " + stored_md5
    return security_status

# Log the analysis of drives to local log file
#
def log_storage_data(sd_ob_list):
    result = 0

    for i in sd_ob_list:
        print i
        if i.percentused >= 90:
            result += 5
        if i.smartstatus != "PASSED":
            result += 100
    
    return result

# Log analysis of security data to local log file
#
def log_security_data(sec_ob_list):
    result = 0

    # for i in sec_ob_list:
    #     print i
    #     if i.percentused >= 90:
    #         result += 5
    #     if i.smartstatus != "PASSED":
    #         result += 100
    
    return result

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
#
def get_config():
    parser = ConfigParser.SafeConfigParser()
    config_dir = os.path.expanduser("~") + "/.h2gc/"
    config_file = "main_config"
    full_config = config_dir + config_file
    print "full_config: " + full_config

    if not os.path.isdir(config_dir):
        print "Config directory does not exist.  First run assumed.  Creating.  Initializing"
        os.makedirs(config_dir, mode=0700)
        config_handle = open(full_config, 'w+')
        init_config_file(parser, config_handle)

    try:
        parser.read(full_config)
    except ConfigParser.ParsingError, err:
        print "Can't read config file, got error: ", err
        
    try: 
        md5out = parser.get('Security', 'shadowmd5', 0) 
    except:
        print "Didn't find the security/shadomd5 option or something like that."     

    print "If anything was read, it was: " + md5out

    return parser

################################
#
#
def main():
    status=0
    storage_list=[]
    security_list=[]

    config_p=get_config()

    if config_p == 1:
        print "Config file cannot be opened or initialized."
        sys.exit(1)

    # Call functions to check system health and log to logfile
    #
    status += check_storage_status(storage_list)
    log_storage_data(storage_list) 
    status += check_security_status(security_list, config_p)
    log_security_data(security_list)

    # Post status to server if available
    #
    post_report("grandma@example.com", status)
    print "Overall status: " + str(status)
    print "Done."

if __name__ == '__main__':
    main()
