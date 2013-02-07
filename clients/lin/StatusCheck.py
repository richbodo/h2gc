#!/usr/bin/env python

import os
import subprocess
import re
import StringIO
import json
import urllib2

# Check the status of storage devices
#
def check_drive_status():
    # Make a list of the removable devices
    root="/sys/block"
    for item in os.listdir(root):
        # for each directory
        current_device=os.path.join(root, item)
        if os.path.isdir(current_device):
            # look for removable = 0
            current_device_removable = os.path.join(root, item, "removable")
            f= open(current_device_removable, 'r')
            isremovable=f.read(1)
            if (isremovable == "1") : 
                print ("found device " + current_device + " which has removable status " + isremovable)
            
    # Make a list of the mounted devices and their usage
    # REFACTOR - this string manip works, but can't possibly be the right way to do it
    out = '\n'.join(subprocess.check_output(["df", "-h"]).splitlines())
    mounts = StringIO.StringIO(out)

    line_num = 0
    for line in mounts.readlines():
        # Get rid of header line
        line_num += 1
        if (line_num == 1):
            continue
        # 
        parts = line.split()
        device, size, used, avail, use_percent, mounted_on = parts
        # if device starts with /dev/, then note mount point and usage
        m = re.search('/dev/.+', device)
        if (m != None):
            print "Found " + device + " mounted on " + mounted_on + " with Use% " + use_percent

    # Get SMART data from mounted devices, if possible
    print "SMART data check goes here"
    # Evaluate data
    print "Fixed drive status evaluation:"
    return 0

# Check to see if any user accounts have changed
#
def check_user_status():
    # would probably be nice to require auditd, but for now just see if shadow has changed:
    # REFACTOR 
    out = '\n'.join(subprocess.check_output(["sudo", "md5sum", "/etc/shadow"]).splitlines())
    md5sum_shadow = StringIO.StringIO(out).readline()
    print "Shadow md5: " + md5sum_shadow
    return 0

def post_report(computer, status):
    # REFACTOR - report errors 
    print "Report results: computer: " + str(computer) + " status:" + str(status)
    url = "http://localhost:3000/logs"
    data = json.dumps({"computer": str(computer), "status": str(status)})
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()

def main():
    status=0
    status += check_drive_status();
    status += check_user_status();
    post_report("grandma@example.com", status)

if __name__ == '__main__':
    main()
