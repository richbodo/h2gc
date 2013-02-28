h2gc
====

This is all very theoretical as not much works, yet.  But since you have opened this README I assume you are wondering what this is.

The HitchHikers Guide to your Computer (H2GC) is a client monitoring program that gives end users a fighting chance to learn and solve their own computer problems.  To learn why, see the_meaning_of_h2gc.

Any user of the H2GC can use the uber-simple client interface to learn about their computer, collaborate with others, and contact knowledgable people.

A server component is also available.  The server is simple and lightweight, and allows power users to ferry client data to other services, such as monitoring systems (nagios, observium, collectd) or helpdesk systems (google apps, salesforce, etc.).

The goal is to make it extremely easy to enhance the client app to check more system issues.  In most cases it is as easy as writing a shell script and dropping it in a directory.  On some systems, we will have to build tools to make it easy for users to write system checks.  Each supported client OS will have a different method of doing this.

Related stuff: The other things people need to empower themselves to fix problems are all interesting and may need integration wth H2GC at some point - debugging and rescue tools are high on the list.  Packages of H2GC and various other things may need to be spit out for update systems to grab and deliver.

LICENSE
=======

All files copyright 2013 Rich Bodo, unless otherwise noted at the top of the file.  All rights reserved.

This software is licensed for use under the GPLV2+.  See this URL for detailed license info: http://www.gnu.org/licenses/gpl-2.0.html 

That basically means you can pretty much use this for anything except distributing as closed source.  Any questions just ask.
 