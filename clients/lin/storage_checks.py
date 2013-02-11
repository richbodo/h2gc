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
# Precondition: gnu mount v2.20.1 output format
# Modifies: list of StorageDevice objects that are mounted and their %usage
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
        m = re.search('/dev/.+\d+',device)
        if (m != None):
            deviceobject=StorageDevice()
            deviceobject.devname = re.search('(/dev/.+)\d+',device).group(1)
            deviceobject.mounted = 1
            deviceobject.mountpoint = mounted_on
            deviceobject.percentused = use_percent
            mounted_list.append(deviceobject)
            print "Found " + deviceobject.devname + " mounted on " + deviceobject.mountpoint + " with Use% " + deviceobject.percentused
    return 0

# get mounted, "fixed" storage device data
#
# Precondition: output format of gnu df 8.1.3 
# Arguments: pass a list of StorageDevice objects 
# Modifies: subset of passed list - devices both mounted and non-removable
#
def get_mounted_fixed_storage_device_data(mounted_list, mounted_fixed_list):
    # Make a list of the non-removable devices
    print "Starting to look at fixed."
    blockdevroot="/sys/block"
    for device in os.listdir(blockdevroot):
        devicepath=os.path.join(blockdevroot, device)        
        if os.path.isdir(devicepath):
            current_device_removable = os.path.join(blockdevroot, device, "removable")
            f= open(current_device_removable, 'r')
            isremovable=f.read(1)
            f.close()
            if (isremovable == "0") : 
                # if devicepath matches an object in mounted_list (devname) then it is fixed
                #      copy that object to mounted_fixed_list
                for mounted_device in mounted_list:
                    print "About to compare: " + devicepath + " With: " + mounted_device.devname
                    # REFACTOR - handle match not found for both of these
                    fd = re.search('/sys/block/(.+)',devicepath).group(1) 
                    md = re.search('/dev/(.+)',mounted_device.devname).group(1)
                    if  fd == md:
                        mounted_device.removable = 0
                        mounted_fixed_list.append(mounted_device)
                    else:
                        print "no match because: " + fd + " is not " + md
    return 0

# Add device smart health
#
# Precondition: output of smartctl v5.4.3
# Arguments: pass list of StorageDevice objects
# Modifies: list of StorageDevice objects annotated with smart health 
# 
def add_device_smart_health(mounted_fixed_list, completed_drive_status_list):
    # for all mounted, non-removable devices, check SMART health
    for device in mounted_fixed_list:
        result = "UNKNOWN"
        device.smartreport = ""
        device_name = device.devname

        print "about to get data for : " + device_name
        out = subprocess.check_output(["sudo", "smartctl", "-H", device_name])
        print "Smart data for: " + device_name + " is: " 
        outlines = iter(out.splitlines())
        pattern =  re.compile('SMART overall-health self-assessment test result: (.+)')
        for line in outlines:
            print line       
            device.smartreport += line
            if pattern.search(line) == None:
                continue
            else:
                result = pattern.search(line).group(1)
        device.smartstatus = result
        return 0

