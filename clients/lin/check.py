#!/usr/bin/env python

import os
import re

# Check the status of storage devices, and return a detailed report
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
    mounts = os.popen('df -h')
    line_num = 0
    for line in mounts.readlines():
        # Get rid of header line
        line_num += 1
        if (line_num == 1):
            continue
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

def check_user_status():
    print "check user status goes here"
    print "User status evaluation:"

def post_report():
    print "post report to google server and to local logs here"
    print "Report results:"

def main():
    check_fixed_drive_status();
    check_user_status();
    post_report();

if __name__ == '__main__':
    main()
