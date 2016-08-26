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
        
        appinit_dlls = ["Microsoft\\Windows NT\\CurrentVersion\\Windows",
                        "Wow6432Node\\Microsoft\\Windows NT\\CurrentVersion\\Windows"]
        
        appinit_dll_list = []
        
        for hive in self.hives:
            try:
                for k in appinit_dlls:
                    last_write = Registry.Registry(hive).open(k).timestamp()
                    on_or_off = Registry.Registry(hive).open(k).value("AppInit_DLLs").value()
                    try:
                        appinitdll = Registry.Registry(hive).open(k).value("LoadAppInit_DLLs").value()
                    except Registry.RegistryValueNotFoundException:
                        appinitdll = "None"
                        continue

                    appinit_dll_list.append((last_write, k, appinitdll, on_or_off))
        
            except Registry.RegistryKeyNotFoundException:
                continue

        for entry in appinit_dll_list:            
            last_write = entry[0]
            key = entry[1]
            loadapp_data = entry[2]
            appinit_data = entry[3].lstrip()

            if self.format_file is not None:                
                with open(self.format_file[0], "rb") as f:
                    template = env.from_string(f.read())
                    sys.stdout.write(template.render(last_write=last_write, \
                                                     key=key, \
                                                     loadapp_data=loadapp_data, \
                                                     appinit_data=appinit_data) + "\n")
            elif self.format is not None:           
                template = Environment().from_string(self.format[0])
                sys.stdout.write(template.render(last_write=last_write, \
                                                 key=key, \
                                                 loadapp_data=loadapp_data, \
                                                 appinit_data=appinit_data) + "\n")