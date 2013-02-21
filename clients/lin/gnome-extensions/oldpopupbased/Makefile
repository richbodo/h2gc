destdir=$(HOME)/.local/share/gnome-shell/extensions/demopopupmenu@fpmurphy.com
filestoinstall=extension.js metadata.json stylesheet.css 
icondestdir=$(HOME)/.local/share/gnome-shell/extensions/demopopupmenu@fpmurphy.com/icons
iconstoinstall=./icons/happyface.png ./icons/sadface.png

all:
	@echo "all"
	@echo "make options:"
	@echo "      install"
	@echo "      uninstall"
	@echo "      dist-zip"
	@echo "      clean"
	@echo "	     debug"

install:
	@echo "install"
	install -Cdv "$(destdir)"
	install -Cdv "$(icondestdir)"
	install -Cv -m 644 $(filestoinstall) "$(destdir)"
	install -Cv -m 644 $(iconstoinstall) "$(icondestdir)"

uninstall:
	@echo "uninstall"
	rm -rfv "$(destdir)"

dist-zip:
	@echo "dist-zip"
	zip -jv demopopupmenu $(files) Makefile

clean:
	@echo "clean"
	rm -fv demopopupmenu.zip

debug:
	@echo "debug"
	tail -F ~/.cache/gdm/session.log

listinstalled:
	@echo "list"
	find /home/richbodo/.local/share/gnome-shell/extensions/demopopupmenu@fpmurphy.com/.
