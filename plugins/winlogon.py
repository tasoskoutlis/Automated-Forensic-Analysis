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

        winlogon_list = []
        
        for hive in self.hives:
            key = Registry.Registry(hive).open("Microsoft\\Windows NT\\CurrentVersion\\Winlogon")
            last_write = key.timestamp()
            
            try:
                winlogon_list.append((key.value("Shell").name(), key.value("Shell").value()))
                winlogon_list.append((key.value("Userinit").name(), key.value("Userinit").value()))
                winlogon_list.append((key.value("Taskman").name(), key.value("Taskman").value()))
                
            except Registry.RegistryValueNotFoundException:
                continue
            
        for entry in winlogon_list:
            last_write
            key_name = key.name()
            value = entry[0]
            data = entry[1]
            
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