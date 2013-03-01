h2gc
====

This is all very theoretical as not much works, yet.  But since you have opened this README I assume you are wondering what this is.

The HitchHikers Guide to your Computer (H2GC) is a client monitoring program that aims to give end users a fighting chance to learn about and solve their own computer problems.  

Any user of the H2GC can use the uber-simple client interface to learn about their computer, collaborate with others, and contact knowledgable people. 

If successful, this will encourage many users to take more responsiblity and learn more about their computing systems.  To understand why that might be useful, see the_meaning_of_h2gc.

The manifestation of the client GUI is a single icon or text button, prominently displayed, notifying the user of any dysfunctional operation of their computing system.  The icon can be clicked (moused over, selected, touched, whatever) and a menu of options will allow the user to diagnose the problem, learn about the problem in plain english, and get help.  

The client uses a local background process to perform system checks, which updates the GUI.

A server component of H2GC is also available.  The server is simple and lightweight, and ferry non-sensitive data sent from the client to other services, such as monitoring systems (nagios, observium, zenoss) or helpdesk systems (self-hosted, google apps, salesforce, etc.).

One important goal is to make it extremely easy to enhance the client app to check more system issues.  On most systems it should be possible to write a shell script and drop it into a directory for the H2GC client daemon to pick up.  On other systems (ios, android), one is forced to build tools to make it easy for users to write system checks.  Each supported client OS will have a different method of doing this.  Ultimately we want people who can't script to either learn how, or use a graphical tool to build system checks.

Future: Many other things that people require to empower themselves to fix problems could be integrated wth the H2GC client - debugging and rescue tools are high on the list of possible integrations.  People have their own, very specific sets of cloud apps, which are also error prone and should be monitored - the checks created by the people who use them.  It is possible!  People can clearly become relative "domain experts" and help each other as such - H2GC should be able to notify them when the opportunity to help a friend arises.  Packages of H2GC, and possibly other tools, may need to be spit out by the H2GC server as resources for update systems (puppet, chef, OS updaters, etc.) - so that needs to be done too.  There is so much that can be done here.  

LICENSE
=======

All files copyright 2013 Rich Bodo, unless otherwise noted at the top of the file, or in a LICENSE file in the directory they are checked into.  All rights reserved.  No warranty.  I mean, really.  The only thing I can gaurantee right now are unexpected results, potentially followed by total destruction of the planet earth to make way for a hyperspace bypass.

This software is further licensed for use under the GPLV2+.  See this URL for detailed license info: http://www.gnu.org/licenses/gpl-2.0.html 

Any questions just ask. richbodo@gmail.com

WANT TO WORK ON THIS?
=====================

I would love to work with you.  Just clone the repo and contact me.  We'll get rolling.