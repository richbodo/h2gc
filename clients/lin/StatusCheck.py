#!/usr/bin/env python
import os
import subprocess
import re
import StringIO
import json
import urllib2
import storage_checks
import security_checks

# POST log entry to server
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
        print "Server says" + response
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
def check_security_status(security_list):
    security_status = 0

    print "checking security status."
    security_status += security_checks.check_shadow_status()
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

# Log security data to local log file
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

def main():
    status=0
    storage_list=[]
    security_list=[]

    status += check_storage_status(storage_list);
    log_storage_data(storage_list) 
    status += check_security_status(security_list);
    log_security_data(security_list)

    post_report("grandma@example.com", status)
    print "Overall status: " + str(status)
    print "Done."

if __name__ == '__main__':
    main()
