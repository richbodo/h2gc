#!/usr/bin/env python

# StatusCheck.py - main system status check daemon for h2gc-linux 
# Status: basically works but super primitive and not useful yet
#
# A lot of checks need to run as superuser.
# Consider adding passwordless sudo user for this script.
# For now running as an hourly cron job under linux.
#

from __future__ import with_statement
import pdb
import os
import stat
import sys
import traceback
import subprocess
import re
import StringIO
import json
import urllib2
import ConfigParser  

class Status:
    def __init__(self):
        self.overall = 0
        self.collective_sad_string = 'Everything looks o.k!'
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
            status.collective_sad_string += 'Reason: ', e.reason
            status.overall += 2
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            status.collective_sad_string += 'Error code: ', e.code
            status.overall += 1 
    else:
        print "Successfully posted data."
        response = f.read()
        print "Server says: " + response
        f.close()


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

# Logging method for Status Check runs
# drop in replacement for print with timestamp
#
def sclog(logstring):
    # open logfile
    # date = 
    # logfile.write date + logstring
    # close logfile
    return 0

# Run a single check script
# TODO exception handling
#
def run_check(full_executable_path):
    print "Running: " + str(full_executable_path)
    my_environment = os.environ.copy()
    p1 = subprocess.Popen([full_executable_path], env=my_environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = p1.communicate()
    returncode = p1.returncode
    print "stdout: ", out
    print "stderr: ", err
    print "returncode: ", returncode
    return returncode

# Get sad string for a given check in the scripts directory
#
def get_sad_string(check_file_name):
    # The with statement automatically closes the file, I think
    # Only works in python 2.5 and up
    with open(check_file_name, 'r') as cf_sad_handle:
        print ("opened: " + check_file_name)
        check_file_string = cf_sad_handle.readline()
        print ("read in: " + check_file_string)

    return check_file_string

# Run All Checkscripts
# gather up overall status number and one line problem descriptions
#
def run_all_checks(scripts_dir, status):

    executable = stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH
    collective_status = 0
    collective_sadness = ''

    for dirpath, dirnames, filenames in os.walk(scripts_dir):
        for currentfile in filenames:
            fileBaseName, fileExtension = os.path.splitext(currentfile)
            path_plus_checkname = os.path.join(dirpath,currentfile)
            if (fileExtension == ".check"): 
                file_stat = os.stat(path_plus_checkname).st_mode
                if (file_stat & executable):
                    print "File: " + currentfile + " is executable - mode: " + oct(file_stat)
                    return_code = run_check(path_plus_checkname)

                    # If check found a problem, add it's return code and sad file contents to status                    
                    if (return_code > 0):
                        sad_name = fileBaseName + ".sad"
                        path_plus_sadname = os.path.join(dirpath,sad_name) 
                        
                        collective_status += return_code
                        collective_sadness += get_sad_string(sad_file_name)

                else:
                    print "Check script: " + path_plus_checkname + " is not executable, adding 1 and calling it a day."
                    collective_status += 1
            else:
                print "Skipping non check file " + path_plus_checkname

    status.collective_sad_string += collective_sadness
    status.overall += collective_status

#################################
#
def main():
    status=Status()
    config_dir = os.path.expanduser("~") + "/.h2gc/"
    scripts_dir = config_dir + "scripts/"
    config_file = "main_config"
    overall_file = "status"
    sad_file = "sad"
    full_config = config_dir + config_file
    full_overall = config_dir + overall_file
    full_sad = config_dir + sad_file

    if (os.path.isdir(config_dir) != True):
        print "Config directory does not exist.  First run assumed.  Creating.  Initializing file."
        os.makedirs(config_dir, mode=0700)
    
    # Open, read entire config file in, close
    #    
    config_handle = open(full_config, 'r') 
    print "opened full_config"
    config_p = get_config(config_handle, full_config)
    print "completed get_config"
    config_handle.close()

    if config_p == 1:
        print "Config file cannot be initialized.  We need a running mode for this situation.  Exiting."
        sys.exit(1)

    # Check system health - log locally - gather overall status info
    #
    run_all_checks(scripts_dir, status)
    
    # Open, write entire config file out, close
    # 
    config_handle = open(full_config, 'w+')
    config_p.write(config_handle)
    config_handle.close()
 
    # Post overall status to server, if available
    # TODO: Use system primary interface mac as key to a unique, meaningless id instead of this hardcoded test string
    #
    post_report("grandma@example.com", status)

    print "Overall status: " + str(status.overall)

    # Write overall status to overall status file
    #
    # --- Nothing should be affecting overall status after this point ---
    #
    overall_handle = open(full_overall, 'w+')    
    overall_handle.write(str(status.overall))
    overall_handle.close()

    # Collect status one-liners from scripts directory and write out to collective status file
    #
    status_handle = open(full_sad, 'w+')    
    status_handle.write(status.collective_sad_string)
    status_handle.close()

    print "Done.\n"

if __name__ == '__main__':
    main()
