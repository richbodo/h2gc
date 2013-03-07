destdir=$(HOME)/.h2gc/integrations

all:

install:
	@echo "install"
	cp integrations/* "$(destdir)"
drop:
	mongo logdb --eval "db.dropDatabase()"
