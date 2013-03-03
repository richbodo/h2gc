#!/usr/bin/env python

# StatusCheck.py - main system status check daemon for h2gc-linux 
#
# Status: basically works but super primitive alpha
#
# Functionality:
#
#   StatusCheck.py runs all the status checkscripts in the ~/.h2gc/scripts/ directory
#
#   It summarizes the outcome of each checkscript, and writes summary data to files.
#   (Currently writes into files in the ~/.h2gc directory.)
#
#   It also sends a status notification to the h2gc notifier application.
#   Once that is done, it stops.  It allows the client GUI to read the summary data
#   in, along with data from the /scripts directory and the web, informing the
#   end user of the system status.
#
#   Files this program writes out (all in ~/.h2gc/ at the moment):
#
#   priority - writes a single word containing the name of the check that is most concerning, if any
#   sad - collected one-liner descriptions from all the system checks of issues outstanding 
#   status - a fuzzy number from 0 to 100 representing the percent hosed the system is 
#   log - any log entries that this script itself generates
#
# TODO:
#
# A lot of checks need to run as superuser.  Disconcerting.
# Consider adding passwordless sudo user for this script.
# For now running as an hourly cron job under linux.
#
# See Roadmap for more features that need to be added
#
#

from __future__ import with_statement
import pdb
import os
import stat
import sys
import traceback
import subprocess
import re
import datetime
import time
import StringIO
import json
import urllib2
import ConfigParser  

class Status:
    def __init__(self):
        self.overall = 0
        self.collective_sad_string = ""
        self.top_priority = ""
    def __str__(self):
        return ("Overall System Status: " + str(self.overall) + "\n"
                "Current Evaluation of Issues: " + str(self.collective_sad_string) + "\n"
                "Top priority: " + str(self.top_priority))

# POST log entry to server
# modifies: status object
#
def post_report(computer, status):
    url = "http://localhost:3000/logs"
    now = datetime.datetime.now()

    data = json.dumps({"device": str(computer), "status": str(status.overall), "datetime": str(now)})
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})

    try:
        f = urllib2.urlopen(req)
    except IOError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            # TODO reset string instead of adding to string here if the current status is zero
            # that goes for both cases
            status.collective_sad_string += 'Error posting to server: ' + str(e.reason)
            status.overall += 2
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            status.collective_sad_string = 'Error posting to server: ' + str(e.code)
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
        parser.add_section('Placeholder')
        foo = "bar"
        parser.set('Placeholder', 'foo', foo)
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
        stuff = parser.get('Placeholder', 'foo', 0)
    except:
        print "Didn't find the placeholder/foo section or something like that.  Creating new sections."     
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
    # The with statement automatically closes the file, I think - only works in python 2.5 and up
    with open(check_file_name, 'r') as cf_sad_handle:
        print ("opened: " + check_file_name)
        check_file_string = cf_sad_handle.readline()
        print ("read in: " + check_file_string)

    return check_file_string

# Run All Checkscripts
# Fill out status object as we go:
#  * gather up overall status number and one line problem descriptions
#  * calculate the top_priority_check based on return value (probably not the best way to do this)
#
def run_all_checks(scripts_dir, status):

    executable = stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH
    collective_status = 0
    collective_sadness = ""
    top_priority_check = ""
    top_priority_value = 0

    for dirpath, dirnames, filenames in os.walk(scripts_dir):
        for currentfile in filenames:
            fileBaseName, fileExtension = os.path.splitext(currentfile)
            path_plus_checkname = os.path.join(dirpath,currentfile)
            if (fileExtension == ".check"): 
                file_stat = os.stat(path_plus_checkname).st_mode
                if (file_stat & executable):
                    print "File: " + currentfile + " is executable - mode: " + oct(file_stat)
                    return_code = run_check(path_plus_checkname)
                    if (return_code > top_priority_value):
                        top_priority_check = fileBaseName
                        top_priority_value = return_code
                        print "New Top Priority: " + top_priority_check + " with returncode: " + str(top_priority_value)
                    # If check found a problem, add it's return code and sad file contents to status                    
                    if (return_code > 0):
                        sad_name = fileBaseName + ".sad"
                        path_plus_sadname = os.path.join(dirpath,sad_name)                        
                        collective_status += return_code
                        collective_sadness += get_sad_string(path_plus_sadname)
                else:
                    print "Check script: " + path_plus_checkname + " is not executable, adding 1 and calling it a day."
                    collective_status += 1
            else:
                print "Skipping non check file " + path_plus_checkname

    if (collective_sadness == ""):
        collective_sadness = "DON'T Panic. Everything looks like it's running o.k."
    status.collective_sad_string += collective_sadness
    status.overall += collective_status
    status.top_priority = top_priority_check

#################################
#
def main():
    status=Status()
    config_dir = os.path.expanduser("~") + "/.h2gc/"
    scripts_dir = config_dir + "scripts/"

    config_file = "config"
    full_config = config_dir + config_file

    overall_file = "status"
    full_overall = config_dir + overall_file

    sad_file = "sad"
    full_sad = config_dir + sad_file

    priority_file = "priority"
    full_priority = config_dir + priority_file
    

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
        
    # Check system health - log locally - gather overall status info
    #
    run_all_checks(scripts_dir, status)

    # Open, write entire config file out, close
    # 
    if config_p == 1:
        print "Client daemon config file could not be initialized.  Not a big deal as I'm not using it right now"
    else:
        config_handle = open(full_config, 'w+')
        config_p.write(config_handle)
        config_handle.close()
 
    # Post overall status to server, if available
    # TODO: Use system primary interface mac as key to a unique, meaningless id instead of this hardcoded test string
    #
    post_report("grandma@example.com", status)

    # Write overall status to overall status file
    #
    # --- Nothing should be affecting overall status after this point ---
    #
    overall_handle = open(full_overall, 'w+')    
    overall_handle.write(str(status.overall))
    overall_handle.close()

    # Write the collective list of one line problem descriptions to the sad file
    #
    status_handle = open(full_sad, 'w+')    
    status_handle.write(status.collective_sad_string)
    status_handle.close()

    # Write the name of the check that is the highest priority right now to the priorty file
    #
    status_handle = open(full_priority, 'w+')    
    status_handle.write(status.top_priority)
    status_handle.close()

    print "Final status written:"
    print status

if __name__ == '__main__':
    main()
