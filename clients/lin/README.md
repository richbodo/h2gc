

What the StatusCheck daemon does
=================================

* Run hourly to run checks and update an overall status (checks update more descriptive problem statuses themselves)
* TBD - serve up a local copy of the GUI help system
* TBD - serve up a local copy of tutorial on coding status checks
* TBD - wizard mode to walk you through creating a status check

There should be a subdirectory for the graphical user interface, which has it's own readme.

I'm calling scripts that are used to check status of something checkscripts.

How to make a checkscript for use with H2GC
============================================

You could just write a script and throw it in the H2GC directory to have it run, but we want to do better than that.

There are loads of ways to improve this system in the future.  Today we are just getting something working.

So here are some rules that one can follow to make client monitoring checks friendly to end users.  

Mostly what needs to be done is to create a few simple files along with your system check, to give the end user some data.

Note the goals here are simplicity, ease of use for end-users, extensibility, update-system-angnostic-ness, and check-freshness.

Recommendations for Writing a CheckScript:
============================================

A) Checkscripts are the executable to be run to check something important every hour - make them executable, name them uniquely,
and put them in the /scripts subdirectory.  Give your script the extension .check

B) All checkscripts must return 0 on success (no problems detected, mission accomplished), or an integer on fail, as below: 

As a rough guide, a return code of 1 means possibly a little bad, 50 means hard drive is about to fail, and 100 is a clear 
security compromise. If the checkscript encounters an exception returncode can be any non-zero value, but the .sad file should be 
updated to reflect the fact that the checkscript is producing an internal error and failing to complete, if possible.

C) You should also put the following files in the scripts directory (all optional, but all easy to make and highly recommended):

checkname.teach - teach user about the check, how it works, and the issue in general - as non technical as possible, as long as you want it to be.

checkname.sad - short (one sentence) explanation to end user of what it means when an error is returned.  it is good but not
required that the check script update this to reflect a specific issue your script has identified.  this is your opportunity
to be specific and not fuzzy.  This is also one place for your script to tell us what problems it runs into when it can't perform
it's job.

checkname.search - a set of search terms the user can use to learn more about how to solve his problem.  this is another file that could be made more useful if you enhanced your script to add to it dynamically.

checkname.log (optional) - Ongoing log file for your checkscript (StatusCheck.py will truncate for you) - can be shown to user with 
the .sad file.  This is where we'll go to figure out the details of what is wrong with the system under test, or with your script.

checkname.cron (optional) - if this file exists, then StatusCheck.py will not try to run this check.
instead, statuscheck will check the contents of this file for a single integer between 0 and 100, and report that as a result. 
(If this file exists we assume you are running a system check under cron, or that it is run as part of another system, and you have adapted it to try to echo some data to h2gc).  Yet another note to self to think about the security implications before I encourage anyone to use this system.

checkname.conf (optional) - if you want your own config file

Open questions (updates/sharing/pushing of checkscripts): 
=========================================================

How can this be made better?  Oh, lots of ways.  Off the top of my head:

     * StatusCheck will have to have a mechanism to prevent just anyone from doing dropping a script in it's scripts dir
     * StatusCheck will have to validate scripts and possibly enforce some rules.
     * Some checks can be created without knowing how to code, given the proper gui.  Build that.

Most, if not all, of the checkscript files could be sections of a wiki page, pulled down periodically via API or wget
(with a link to the latest online version embedded), while the client app itself
could be pushed periodically via puppet or chef, or could update itself via the OS update system.

Have to take a look at what others are doing.  Tons of security issues.

I want to go to there ->  http://www.python.org/dev/peps/pep-0020/