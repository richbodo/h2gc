h2gc
====

This is all very theoretical as not much works, yet.  But since you have opened this README I assume you are wondering what this is.

The HitchHikers Guide to your Computer (H2GC) is a client monitoring program that gives end users a fighting chance to learn and solve their own computer problems.

Any user of the H2GC can use the uber-simple client interface to learn about their computer, collaborate with others, and contact knowledgable people.

The server interface is simple and lightweight, and allows power users to identify problems with other systems quickly.

After installing on any supported client system, an icon will appear on the operatings system tray (or equivalent), informing users of the state of their system.  In the alpha relase, the two initial system issues checked will be fixed storage device health, and basic security issues.

It is extremely easy to enhance the system to check more system issues.  Just write a shell script that checks something, logs detailed information to a log file, and returns a number from 0 to 100, denoting the severity of the issue.  The h2gc daemon will pick it up and run with it.

LICENSE
=======

All files copyright 2013 Rich Bodo, unless otherwise noted at the top of the file.  All rights reserved.

This software is licensed for use under the GPLV2+.  See this URL for detailed license info: http://www.gnu.org/licenses/gpl-2.0.html 

That basically means you can pretty much use this for anything except distributing as closed source.  Any questions just ask.
 