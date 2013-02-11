import os
import subprocess
import re
import StringIO
import json
import urllib2

# Check to see if any user accounts have changed
#
def check_shadow_status():
    # REFACTOR 
    out = '\n'.join(subprocess.check_output(["sudo", "md5sum", "/etc/shadow"]).splitlines())
    md5sum_shadow = StringIO.StringIO(out).readline()
    print "Shadow md5: " + md5sum_shadow
    return 0
