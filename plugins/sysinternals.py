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
            for entry in self.processSysinternals(hive):
                last_write = entry[0]
                key_name = entry[1]
                
                if self.format is not None:
                    template = Environment().from_string(self.format[0])
                    sys.stdout.write(template.render(last_write=last_write, \
                                                     key_name=key_name) + "\n")
                elif self.format_file is not None:
                    with open(self.format_file[0], "rb") as f:
                        template = env.from_string(f.read())            
                        sys.stdout.write(template.render(last_write=last_write, \
                                                         key_name=key_name) + "\n")
                
    def processSysinternals(self, hive):
        
        sysinternals_list = []
        
        try:
            for sks in Registry.Registry(hive).open("Software\\Sysinternals").subkeys():
                for v in sks.values():
                    if "EulaAccepted" in v.name():
                        if v.value() == 1:
                            last_write = sks.timestamp()
                            key_name = sks.name()
                            
                            sysinternals_list.append([last_write, key_name])
                                 
        except Registry.RegistryKeyNotFoundException as e:
            pass
        
        return(sysinternals_list)