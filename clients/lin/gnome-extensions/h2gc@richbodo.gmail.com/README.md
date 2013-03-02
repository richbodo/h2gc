

**H2GC** is a client monitoring extension.

This version is based on gnome-shell-extension-cpu-temperature, 
which is an extension for displaying system temperature data in
the top panel when running GNOME Shell

Originally based on the weather gnome extension - looking to use a symbolic
icon (happy face when checks are o.k., frowny when checks are bad)
instead of text in the notification menu.  The icon caused flickering
that was hard to debug so no icon option for now.

Installation
------------

make install
Alt-F2, r

Configuration
---------------------

this is part of a larger application, 
take a look at the README for the H2GC project on github.

Features
---------

Display status issues on panel

Menu:

* TBD - Displays DON'T PANIC if there is a problem.
* Displays local issue information if there is a problem.
* TBD - Collaborate link (Chatroom, IRC, etc.)
* Get Help link ( Your sysadmin, whoever)
* Read About it link (Help System, Searches of various kinds)
* Display/Edit config
* TBD Re-run-checks now (+last check run time) - if this fails, then status is set to H2GC is down

License
--------

Like all gnome extensions, GPLV2+

Authors 
---------
[H2GC]: just rich, for now.
[CPU Temp extension]: https://github.com/xtranophilist/gnome-shell-extension-cpu-temperature/graphs/contributors


