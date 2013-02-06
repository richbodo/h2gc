import os
import stat
from ConfigParser import SafeConfigParser
from UserDict import IterableUserDict

__all__ = ['SimpleConfig', 'UnsupportedOSError']

class UnsupportedOSError(Exception): pass

class SimpleConfig(IterableUserDict):
    """Cross-platform configuration file handler.

    This is a class to manage a configuration file, regardless of the
    operating system. Configuration is a set of (key, value) that can
    be set and retrieved by using SimpleConfig as a dictionary. Keys
    and values must all be strings. Example usage::

    >>> conf = SimpleConfig('myapp')   # Load configuration file if it exists
    >>> conf['foo'] = '3'              # Set a value
    >>> conf.save()                    # Save the configuration file on disk
    >>> conf.delete()                  # Delete file, it was just an example

    SimpleConfig builds the configuration file path using the
    operating system name and the application name:

    * Unix: $HOME/.appname
    * Mac: $HOME/Library/Application Support/appname
    * Windows: $HOMEPATH\Application Data\\appname
    
    Tested on Linux and Windows XP so far. 

    """

    section = 'main'

    def __init__(self, appname):
        """Open the configuration file and fill the dictionary.

        ``appname`` is the application identifier, it is used to build
        the configuration file path.  If the file does not exist, the
        dictionary is left empty.
        """
        IterableUserDict.__init__(self)
        self.filename = self._filename(appname)
        self.parser = SafeConfigParser()
        self.parser.read(self.filename)
        if not self.parser.has_section(self.section):
            self.parser.add_section(self.section)
        for name, value in self.parser.items(self.section):
            self.data[name] = value


    def save(self):
        """Save the configuration file on disk."""
        for name, value in self.data.items():
            self.parser.set(self.section, str(name), str(value))
        f = open(self.filename, 'w')
        self.parser.write(f)
        f.close()
        

    def delete(self):
        """Delete the configuration file."""
        os.chmod(self.filename, stat.S_IWRITE)
        os.remove(self.filename)


    def _filename(self, appname):
        # os.name is 'posix', 'nt', 'os2', 'mac', 'ce' or 'riscos'
        if os.name == 'posix':
            filename = "%s/.%s" % (os.environ["HOME"], appname)

        elif os.name == 'mac':
            filename = ("%s/Library/Application Support/%s" %
                        (os.environ["HOME"], appname))
            
        elif os.name == 'nt':
            filename = ("%s\Application Data\%s" %
                        (os.environ["HOMEPATH"], appname))
        else:
            raise UnsupportedOSError(os.name)
        
        return filename


if __name__ == "__main__":
    
    def test():
        conf = SimpleConfig("myapp")
        filename = conf.filename
        port = "3000"
        message = "Hello World!"
        conf["port"] = port
        conf["message"] = message
        conf.save()

        conf = SimpleConfig("myapp")
        assert conf["port"] == port
        assert conf["message"] == message
        conf.delete()
        assert not os.path.exists(filename)

    test()
