#!/usr/bin/env python
import os
import subprocess
import re
import StringIO
import json
import urllib2

class StorageDevice:
    def __init__(self):
        self.devname = 0
        self.removable = 0
        self.mounted = 0
        self.mountpoint = "TBD"
        self.percentused = 0
        self.smartcapable = 0
        self.smartreport = "TBD"
        self.smartstatus = "TBD"
    def __str__(self):        
        return ("Storage Device Object\n"
                "Device Name: " + str(self.devname) + "\n"
                "Removable?: " + str(self.removable) + "\n"
                "Mounted?: " + str(self.mounted) + "\n"
                "Mount Point: " + str(self.mountpoint) + "\n"
                "Percent Used: " + str(self.percentused) + "\n"
                "SMART Capable: " + str(self.smartcapable) + "\n"
                "SMART Report: " + str(self.smartreport) + "\n"
                "SMART Health Summary Status: " + str(self.smartstatus) + "\n")	


# Get mounted storage device info
#
# precondition: gnu mount v2.20.1 output format
# modifies: list of StorageDevice objects that are mounted and their %usage
#
def get_mounted_storage_device_info(mounted_list):
    # Make a list of the mounted devices and their usage
    # REFACTOR - this string manip works, but can't possibly be the right way to do it
    out = '\n'.join(subprocess.check_output(["df", "-h"]).splitlines())
    mounts = StringIO.StringIO(out)

    line_num = 0
    for line in mounts.readlines():
        line_num += 1
        # Get rid of header line
        if (line_num == 1):
            continue
        parts = line.split()
        # REFACTOR - robustness
        device, size, used, avail, use_percent, mounted_on = parts
        # if device starts with /dev/, then note mount point and usage
        m = re.search('/dev/.+', device)
        if (m != None):
            #print "Found " + device + " mounted on " + mounted_on + " with Use% " + use_percent
            deviceobject=StorageDevice()
            deviceobject.devname=device
            deviceobject.mountpoint = mounted_on
            deviceobject.percentused = use_percent
            mounted_list.append(deviceobject)
    return 0

# get mounted, "fixed" storage device data
#
# precondition: output format of gnu df 8.1.3 
# arguments: pass a list of StorageDevice objects 
# modifies: subset of passed list - devices both mounted and non-removable
#
def get_mounted_fixed_storage_device_data(mounted_list, mounted_fixed_list):
    # Make a list of the non-removable devices
    blockdevroot="/sys/block"
    for device in os.listdir(blockdevroot):
        devicepath=os.path.join(blockdevroot, device)        
        if os.path.isdir(devicepath):
            current_device_removable = os.path.join(blockdevroot, device, "removable")
            f= open(current_device_removable, 'r')
            isremovable=f.read(1)
            f.close()
            if (isremovable == "0") : 
                # print ("found device " + devicepath + " which is fixed: " + isremovable)
                # if devicepath matches an object in mounted_list (devname) then copy that object to mounted_fixed_list
                for mounted_device in mounted_list:
                    fd = re.search('/sys/block/(.+)',devicepath).group(1) 
                    md = re.search('/dev/(.+)\d+',mounted_device.devname).group(1)
                    if  fd == md:
                        print "Sys block device: " + fd + " matches device name: " + md + " within mounted partition name: " + mounted_device.devname
                        mounted_fixed_list.append(mounted_device)
                    else:
                        print "no match because: " + fd + " is not " + md
            #else:
                #print ("found device " + devicepath + " which is removable: " + isremovable)
    # Compile list of devices that are both mounted and fixed
    return 0

# Add device smart health
#
# precondition: output of smartctl v5.4.3
# arguments: pass list of StorageDevice objects
# modifies: list of StorageDevice objects annotated with smart health 
# 
def add_device_smart_health(mounted_fixed_list, completed_drive_status_list):
    # Get SMART data from mounted devices, if possible
    # NOTE might need to require smartmontools, don't know of another way to get this

    # for all mounted, non-removable devices
    #for device in mounted_fixed_list:
            # smartreport = sudo smartctl -H device
                # deviceobject.smartreport = smartreport
            # if ! grep for PASSED:
                # deviceobject.smarthealth = FAIL
            # else 
                # deviceobject.smarthealth = PASSED

    print "SMART data check goes here"
    return 0

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

# Check the status of storage devices
#
# returns: 0 if all drives are o.k., 1 if any drive is problematic
#
def check_drive_status():
    drive_status=0
    mounted_list=[]
    mounted_fixed_list=[]
    completed_drive_status_list=[]

    get_mounted_storage_device_info(mounted_list)
    get_mounted_fixed_storage_device_data(mounted_list, mounted_fixed_list)
    #add_device_smart_health(mounted_fixed_list, completed_drive_status_list)
    drive_status = log_storage_data(mounted_fixed_list) 

    return drive_status

# Check to see if any user accounts have changed
#
def check_user_status():
    # NOTE would probably be nice to require auditd
    # REFACTOR 
    out = '\n'.join(subprocess.check_output(["sudo", "md5sum", "/etc/shadow"]).splitlines())
    md5sum_shadow = StringIO.StringIO(out).readline()
    print "Shadow md5: " + md5sum_shadow
    return 0

# POST log entry to server
#
def post_report(computer, status):
    # REFACTOR - report errors - cleanup 
    print "Reporting results: computer: " + str(computer) + " status:" + str(status)
    url = "http://localhost:3000/logs"
    data = json.dumps({"computer": str(computer), "status": str(status)})
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    print "Server says" + response
    f.close()

def main():
    status=0
    status += check_drive_status();
    status += check_user_status();
    # post_report("grandma@example.com", status)
    print "Overall status: " + str(status)
    print "Done."

if __name__ == '__main__':
    main()
