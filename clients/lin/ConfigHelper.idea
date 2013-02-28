
# Thinking about what to do when all else fails.
#
# ConfigHelper would allow the user to bootstrap his system into debuggable order.
#
# Used when his system cannot self-repair our primary debugging tools, 
# and/or the user can't get the packages he needs (may not be on net).
#
# This script can restart the config of these packages, and attempt
# to fix any config issues that the user has run into.
#
# * update-manager - puppet or chef
# * monitoring - h2gc or whatever
# * logging - log.io or syslog-ng
# * vpn - openvpn 
# * screen sharing, and/or other remote management tools
#
# H2GC should diagnose network issues and help him figure those out,
# so if that can be installed, we can bring the rest of the tools up.
#
# Another thing to do with this is to create a custom knoppix bootable
# USB stick with these pre-installed, and teach ConfigHelper how to 
# fix a system that has booted from USB.
#
