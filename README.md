h2gc
====

This is all very theoretical as not much works, yet.  But since you have opened this README I assume you are wondering what this is.

The HitchHikers Guide to your Computer (H2GC) is a client monitoring program that aims to give end users a fighting chance to learn and solve their own computer problems.  

Any user of the H2GC can use the uber-simple client interface to learn about their computer, collaborate with others, and contact knowledgable people. 

To understand why that might be useful, see the_meaning_of_h2gc.

The manifestation of the client GUI is a single icon or text button, notifying the user of any dysfunctional operation of their computing system.  The icon can be clicked (moused over, selected, touched, whatever) and a menu of options will allow the user to diagnose the problem, learn about the problem in plain english, and get help.  

The client uses a local background process to perform system checks, which update the GUI.

A server component of H2GC is also available.  The server is simple and lightweight, and allows power users to ferry non-sensitive client data to other services, such as monitoring systems (nagios, observium, zenoss) or helpdesk systems (self-hosted, google apps, salesforce, etc.).

The goal is to make it extremely easy to enhance the client app to check more system issues.  In most cases it should be as easy as writing a shell script and dropping said script in a directory.  On some systems (ios, android), we will have to build tools to make it easy for users to write system checks.  Each supported client OS will have a different method of doing this.

Future: Many other things that people require to empower themselves to fix problems could be integrated wth the H2GC client - debugging and rescue tools are high on the list of possible integrations.  Packages of H2GC, and possibly other tools, may need to be spit out by the H2GC server as resources for update systems (puppet, chef, OS updaters, etc.).

LICENSE
=======

All files copyright 2013 Rich Bodo, unless otherwise noted at the top of the file, or in a LICENSE file in the directory they are checked into.  All rights reserved.  No warranty.  I mean, really.  The only thing we can gaurantee right now are unexpected results, potentially followed by total destruction of the planet earth to make way for a hyperspace bypass.

This software is further licensed for use under the GPLV2+.  See this URL for detailed license info: http://www.gnu.org/licenses/gpl-2.0.html 

Any questions just ask. richbodo@gmail.com
