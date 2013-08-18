#!/usr/bin/env python

import os
import subprocess

def run_check(full_executable_path):
    print "Running: " + str(full_executable_path)
    my_environment = os.environ.copy()
    p1 = subprocess.Popen(full_executable_path.split(), env=my_environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = p1.communicate()
    returncode = p1.returncode
    print "stdout: ", out
    print "stderr: ", err
    print "returncode: ", returncode
    return returncode

#################################
#
def main():
    print "lets run something"
    path="/bin/ls /home/richbodo"
    run_check(path)

if __name__ == '__main__':
    main()
