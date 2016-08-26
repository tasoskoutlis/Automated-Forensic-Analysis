import sys
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

        for hive in self.hives:
            try:
                runmru = Registry.Registry(hive).open("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU")
            except Registry.RegistryKeyNotFoundException as e:
                pass
            key = runmru.name()
            last_write = runmru.timestamp()
            try:
                mruorder = runmru.value("MRUList").value()
            except Registry.RegistryParse.RegistryStructureDoesNotExist as error:
                print "There are no MRUList values. Exiting."
                exit(0)
            for entry in list(mruorder):
                for vals in runmru.values():
                    if entry == vals.name():
                        value = vals.name()
                        data = vals.value()
                    else:
                        continue
                    
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