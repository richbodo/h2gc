destdir=$(HOME)/.local/share/gnome-shell/extensions/temperature@xtranophilist
filestoinstall=convenience.js  extension.js  metadata.json  prefs.js
schemadestdir=$(HOME)/.local/share/gnome-shell/extensions/temperature@xtranophilist/schemas
schemastoinstall=./schemas/gschemas.compiled  ./schemas/org.gnome.shell.extensions.cpu-temperature.gschema.xml

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
	install -Cdv "$(schemadestdir)"
	install -Cv -m 644 $(filestoinstall) "$(destdir)"
	install -Cv -m 644 $(schemastoinstall) "$(schemadestdir)"

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
	find /home/richbodo/.local/share/gnome-shell/extensions/temperature@xtranophilist
