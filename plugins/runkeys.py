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
        
        dict = {}
        
        for hive in self.hives:
            dict.update(self.processKeys(hive))
            
        for key, val in dict.iteritems():
            last_write = val[0]
            value = key
            key_name = val[1]
            data = val[2]
            
            
            if self.format is not None:              
                template = Environment().from_string(self.format[0])
                sys.stdout.write(template.render(last_write=last_write, \
                                                     key_name=key_name, \
                                                     value=value, \
                                                     data=data) + "\n")
            elif self.format_file is not None:
                with open(self.format_file[0], "rb") as f:
                    template = env.from_string(f.read())
                    sys.stdout.write(template.render(last_write=last_write, \
                                                     key_name=key_name, \
                                                     value=value, \
                                                     data=data) + "\n")        
    
    def processKeys(self, hive):
        run_key_list = []
        run_entries =   ["Microsoft\\Windows\\CurrentVersion\\Run",
                         "Microsoft\\Windows\\CurrentVersion\\RunOnce",
                         "Microsoft\\Windows\\CurrentVersion\\RunOnceEx",
                         "Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\Run",
                         "Microsoft\\Windows\\CurrentVersion\\RunServicesOnce"
                         "Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Run",
                         "Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\RunOnce",
                         "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                         "Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce",
                         "Software\\Microsoft\\Windows\\CurrentVersion\\RunServices",
                         "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\Run"]
        
        for k in run_entries:
            try:
                for v in  Registry.Registry(hive).open(k).values():
                    last_write = Registry.Registry(hive).open(k).timestamp()
                    if k:
                        key_name = k
                    else:
                        key_name = "None"
                    if v.name():
                        name = v.name()
                    else:
                        name = "None"
                    if v.value():
                        value = v.value()
                    else:
                        value = "None"
                    run_key_list.append([last_write, key_name, name, value])
                    
            except Registry.RegistryKeyNotFoundException:
                continue
        
        dict = {}
        for entry in run_key_list:
            dict[entry[2]] = entry[0], entry[1], entry[3]            

        return(dict)