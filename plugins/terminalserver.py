import sys
from Registry import Registry
from PluginManager import HelperFunctions
from jinja2 import Template, Environment, PackageLoader

class PluginClass(object):

    def __init__(self, hives=None, search=None, format=None, format_file=None):
        self.hives = hives
        self.search = search
        self.format = format
        self.format_file = format_file

    def ProcessPlugin(self):

        env = Environment(keep_trailing_newline=True, loader=PackageLoader('regparse', 'templates'))
        
        terminal_server_list = []

        for hive in self.hives:
            current = HelperFunctions(hive).CurrentControlSet()
            key = Registry.Registry(hive).open('%s\\Control\\Terminal Server' % (current))

            try:
                terminal_server_list.append((key.subkey("WinStations").subkey("RDP-Tcp").timestamp(), \
                                             key.subkey("WinStations").subkey("RDP-Tcp").value("UserAuthentication").name(), \
                                             key.subkey("WinStations").subkey("RDP-Tcp").value("UserAuthentication").value()))                
            except Registry.RegistryValueNotFoundException:
                continue            
            
            try:
                terminal_server_list.append((key.subkey("Wds").subkey("rdpwd").timestamp(), \
                                             key.subkey("Wds").subkey("rdpwd").value("StartupPrograms").name(), \
                                             key.subkey("Wds").subkey("rdpwd").value("StartupPrograms").value()))
            except Registry.RegistryValueNotFoundException:
                continue
            
            try:
                last_write = key.timestamp()
                terminal_server_list.append((last_write, \
                                             key.value("fDenyTSConnections").name(), key.value("fDenyTSConnections").value()))
                terminal_server_list.append((last_write, \
                                             key.value("DeleteTempDirsOnExit").name(), key.value("DeleteTempDirsOnExit").value()))
                terminal_server_list.append((last_write, \
                                             key.value("fSingleSessionPerUser").name(), key.value("fSingleSessionPerUser").value()))
            except Registry.RegistryValueNotFoundException:
                continue 
            
        for entry in terminal_server_list:
            key_name = key.name()
            last_write = entry[0]
            value = entry[1]
            data = entry[2]
            
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