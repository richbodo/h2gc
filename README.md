h2gc
====

This is all very theoretical as not much works, yet.  But since you are here, I assume you are wondering what this is...

The HitchHikers Guide to your Computer (H2GC) is a program that aims to give ordinary people a fighting chance to learn about and solve their own computer problems.  

Any user of the H2GC can use a super-simple interface to learn about their computer, collaborate with others, and contact knowledgable people. 

What does H2GC look like?  The part that goes on your laptop or mobile device I call the client app.  The client app has a user interface, we'll call it the "client GUI".

The manifestation of the client GUI is a single icon or text button, prominently displayed, notifying the user of problems.  The icon can be clicked (moused over, selected, touched, whatever) and a menu of options will allow the user to diagnose the problem, learn about the problem in plain english, and get help.  

The client app also comes with a background process to perform a bunch of system checks, which update the client GUI.  That background process is called the "client daemon".  I know.

A server component of H2GC is also available.  We'll call it the H2GC server.  Here's where I reveal my true nerd self and drop into technical jargon.  DON'T PANIC. 

The H2GC server is simple and lightweight - it ferries non-sensitive data sent from the client to other services, such as monitoring systems (nagios, observium, zenoss) or helpdesk systems (hosted by your IT guy/gal or in google apps, salesforce, zendesk, etc.).

One important goal of H2GC is to make it extremely easy to enhance the client app to check more system issues.  

On most systems it should be possible to write a small script that checks something new, and to drop that into a directory for the H2GC client daemon to pick up.  

On other systems (ios, android), one is required to build graphical tools to make it easy for users to write system checks.  Each supported client OS will have a different method of doing this.  Ultimately we want people who can't script to either learn how, or use a graphical tool to build system checks.

Future Stuff: 

Many other things that people require to empower themselves to fix problems could be integrated wth the H2GC client - debugging and rescue tools are high on the list of possible integrations.  People have their own, very specific sets of cloud apps that they use, which are also error prone and should be monitored.  End users should be able to create tests for the online services they use themselves.  It is possible!  People can clearly become relative "domain experts" and help each other as such - H2GC should be able to notify them when the opportunity to help a friend arises.  Packages of H2GC, and possibly other tools, may need to be spit out by the H2GC server as resources for update systems (puppet, chef, OS updaters, etc.) - so that needs to be done too.  There is so much that can be done when you are empowering people rather than herding them.

LICENSE
=======

All files copyright 2013 Rich Bodo, unless otherwise noted at the top of the file, or in a LICENSE file in the directory they are checked into.  All rights reserved.  No warranty.  I mean, really.  The only thing I can gaurantee right now are unexpected results, potentially followed by total destruction of the planet earth to make way for a hyperspace bypass.

This software is further licensed for use under the GPLV2+.  See this URL for license info: http://www.gnu.org/licenses/gpl-2.0.html 

Any questions just ask. richbodo@gmail.com

WANT TO WORK ON THIS?
=====================

I would probably *love* to work with you.  Just clone the repo and contact me.  We'll get rolling.  Don't forget your towel. 