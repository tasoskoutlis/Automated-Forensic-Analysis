import sys
import struct
from Registry import Registry
from jinja2 import Template, Environment, PackageLoader

class PluginClass(object):

    def __init__(self, hives=None, search=None, format=None, format_file=None):
        self.hives = hives
        self.search = search
        self.format = format
        self.format_file = format_file

    def ProcessPlugin(self):

        env = Environment(keep_trailing_newline=True, loader=PackageLoader('regparse', 'templates'))
        
        recentdocs_root = []
        
        for hive in self.hives:
            
            recentdocs = Registry.Registry(hive).open("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs")

            key = recentdocs.name()
            last_write = recentdocs.timestamp()
            mruorder = recentdocs.value("MRUListEx").value()
            for entry in struct.unpack("%dI" % (len(mruorder)/4), mruorder):
                for docs in recentdocs.values():
                    if docs.name() == str(entry):
                        val = (docs.value().split('\x00\x00')[0]).decode("utf-8", errors='ignore')
                        recentdocs_root.append((recentdocs.timestamp(), key, "RootMRU", entry, val))
                    else:
                        continue
                        
            for subkeys in Registry.Registry(hive).open("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs").subkeys():
                mruorder = subkeys.value("MRUListEx").value()
                for values in subkeys.values():
                    for entry in  struct.unpack("%dI" % (len(mruorder)/4), mruorder):
                        if str(values.name()) == str(entry):
                            val = (values.value().split('\x00\x00')[0]).decode("utf-8", errors='ignore')
                            recentdocs_root.append((subkeys.timestamp(), key, subkeys.name(), values.name(), val))
                        else:
                            continue
                        
        for entry in recentdocs_root:
            last_write = entry[0]
            key_name = entry[1]
            key = entry[2]
            value = entry[3]
            data = entry[4]
                        
            if self.format_file is not None:
                with open(self.format_file[0], "rb") as f:
                    template = env.from_string(f.read())
                    sys.stdout.write(template.render(last_write=last_write, \
                                                     key_name=key_name, \
                                                     key=key, \
                                                     value=value, \
                                                     data=data) + "\n")
        
            elif self.format is not None:              
                template = Environment().from_string(self.format[0])
                sys.stdout.write(template.render(last_write=last_write, \
                                                 key_name=key_name, \
                                                 key=key, \
                                                 value=value, \
                                                 data=data) + "\n")