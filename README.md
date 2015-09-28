h2gc
====

NOTE: This is not currently maintained, but I do maintain that the idea of a full-featured, cross platform, peer-peer monitoring client is important.  I developed this for the Hacker Dojo reverse job fair.

The HitchHikers Guide to your Computer (H2GC) is a program that aims to give ordinary people a fighting chance to learn about and solve their own computer problems.

Any user of the H2GC can use a super-simple interface to learn about their computer, collaborate with others, and contact knowledgable people.  

What does it look like?  

A client app is installed on the device to be monitored.  It has a graphical part (GUI) and a background process part. 

The graphical part is a single icon or text button, prominently displayed only when needed, notifying the user of any problems with their computer.  

If there is a problem, the icon can be clicked on, and a one-sentence plain english summary of the problem will appear.  

Along with the explanation, the user can select any of the following actions from a menu:

* Search - Read about the specific problem that has occurred via search engines
* Learn - Learn about the problem from the resources that the person who wrote the test recommends
* Collaborate - Pop into a chatroom with people who are working on similar issues
* Get Help - Send an email with diagnostic information to your preferred expert person
* Share - Create a page online with information about your awesome setup, and compose a message about it to share on social nets.
* Change Stuff - Configure H2GC, learn to write tests yourself to know when things change online or on your computer.

What H2GC is NOT:

* Clippy (that annoying paperclip in some old versions of ms windows)
  H2GC exposes only what information you want exposed, in a secure manner, to you and to your IT person(s).
* A helpdesk system, central monitoring system, software update system, or virus checker.  
  H2GC is more powerful when used with those systems, but does not rely on or replace them.

As mentioned, the client app also comes with a background process to perform a bunch of system checks, which update the client GUI.  That background process is called the "client daemon".

One important goal of H2GC is to make it extremely easy to enhance the client app so that it can check more system issues.  

On most systems it should be possible to write a small script that checks something new, and to drop that into a directory for the H2GC client daemon to pick up.  

On other systems (ios, android), one is required to build graphical tools to make it easy for users to write system checks.  Each supported client OS will have a different method of doing this.  Ultimately we want people who can't script to either learn how, or use a graphical tool to build system checks.

Future Stuff: 
-------------

Experimentally, a server component of H2GC is also available.  We'll call it the H2GC server.  It is meant to be run online by an expert sysadmin.  Here's where I reveal my true nerd self and drop into technical jargon.  DON'T PANIC. 

The current H2GC server is simple and lightweight - it ferries non-sensitive data sent from the client to other services, such as monitoring systems (nagios, observium, zenoss) or helpdesk systems (hosted by your IT guy/gal or in google apps, salesforce, zendesk, etc.).

As we are going with the standalone server idea for now: Packages of H2GC, and possibly other tools, may need to be spit out by the H2GC server as resources for update systems (puppet, chef, OS updaters, etc.).  The design isn't fully baked yet, but the idea of the server is to insulate clients from having to integrate with various cloud services and internal network systems - so those integrations are all fun little projects that can be done as well.  

A better idea than the H2GC server is probably to make H2GC, at least partially, a peer-peer system.  Here I'll have to wave my hands a bit.  H2GC clients could connect to one another through broadcast messages or an H2GC website, or a pool of available bittorrent systems.  Trusted peer groups could be formed, a trivial exercise left for the implementor ;).  If you had a system like that, you could make each client a monitoring node in a larger group, and everyone could get central reporting of what the network appears to be like.  You would want to choose an internet scale method for this, if you could.

Many other things that people require to empower themselves to fix computing problems could be integrated wth the H2GC client - debugging and rescue tools are high on the list of possible integrations.  People have their own, very specific sets of cloud apps that they use, which are also error prone and should be monitored.  End users should be able to create tests for the online services they use themselves and share them almost as if they have a social network for fixing and monitoring computer stuff.  It is possible!  Obviously, people can become relative "domain experts" and help each other as such - H2GC should be able to notify them when the opportunity to help a friend arises.  

LICENSE
=======

All files copyright 2013 Rich Bodo, unless otherwise noted at the top of the file, or in a LICENSE file in the directory they are checked into.  All rights reserved.  No warranty.  I mean, really.  The only thing I can gaurantee right now are unexpected results, potentially followed by total destruction of the planet earth to make way for a hyperspace bypass.

This software is further licensed for use under the GPLV2+.  See this URL for license info: http://www.gnu.org/licenses/gpl-2.0.html 

Any questions just ask. richbodo@gmail.com

WANT TO WORK ON THIS?
=====================

"I would probably *love* to work with you.  Just clone the repo and contact me.  We'll get rolling.  Don't forget your towel. 
