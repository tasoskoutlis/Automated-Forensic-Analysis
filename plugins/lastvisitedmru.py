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

        lastvisited = ["Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\LastVisitedMRU",
                       "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\LastVisitedPidlMRU",
                       "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\LastVisitedPidlMRULegacy"
                       ]

        for hive in self.hives:
            for k in lastvisited:
                try:
                    lvmru = Registry.Registry(hive).open(k)
                    key = lvmru.name()
                    last_write = lvmru.timestamp()
                    mruorder = lvmru.value("MRUListEx").value()
                    for entry in struct.unpack("%dI" % (len(mruorder)/4), mruorder):
                        for values in lvmru.values():
                            if str(values.name()) == str(entry):
                                value = values.name()
                                data = (values.value().split('\x00\x00')[0])
                                if self.format_file is not None:                
                                    with open(self.format_file[0], "rb") as f:
                                        template = env.from_string(f.read())
                                        sys.stdout.write(template.render(last_write=last_write, \
                                                                            key=key, \
                                                                            mruorder=mruorder, \
                                                                            value=value, \
                                                                            data=data) + "\n")
                                elif self.format is not None:           
                                    template = Environment().from_string(self.format[0])
                                    sys.stdout.write(template.render(last_write=last_write, \
                                                                        key=key, \
                                                                        mruorder=mruorder, \
                                                                        value=value, \
                                                                        data=data) + "\n")  
                            
                except (Registry.RegistryKeyNotFoundException, Registry.RegistryValueNotFoundException):
                    continue



