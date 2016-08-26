import sys
import time
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
        
        dict = {}
        
        for hive in self.hives:
            
            try:
                control = HelperFunctions(hive).CurrentControlSet()
                dict.update(self.getSystemInfo(Registry.Registry(hive).open('%s\\Control' % (control))))
            except Registry.RegistryKeyNotFoundException:
                pass
        
            try:
                dict.update(self.getSoftwareInfo(Registry.Registry(hive).open("Microsoft\\Windows NT\\CurrentVersion")))
            except Registry.RegistryKeyNotFoundException:
                pass
        
        os_info = dict['OSInfo']
        installed_date = dict['InstallDate']
        registered_owner = dict['Owner']
        computer_name = dict['ComputerName']
        time_zone = dict['TimeZone']
        
        if self.format_file is not None:
            with open(self.format_file[0], "rb") as f:
                template = env.from_string(f.read())
                sys.stdout.write(template.render(os_info=os_info, \
                                                 installed_date=installed_date, \
                                                 registered_owner=registered_owner, \
                                                 computer_name=computer_name, \
                                                 time_zone=time_zone) + "\n")
    
        elif self.format is not None:              
            template = Environment().from_string(self.format[0])
            sys.stdout.write(template.render(os_info=os_info, \
                                                 installed_date=installed_date, \
                                                 registered_owner=registered_owner, \
                                                 computer_name=computer_name, \
                                                 time_zone=time_zone) + "\n")        
      
    def getSystemInfo(self, hive):       
        if "@tzres.dll" in hive.subkey("TimeZoneInformation").value("StandardName").value():
            time_zone = hive.subkey("TimeZoneInformation").value("TimeZoneKeyname").value()
        else:
            time_zone = hive.subkey("TimeZoneInformation").value("StandardName").value()

        computer_name = hive.subkey("ComputerName").subkey("ComputerName").value("ComputerName").value()
        dict = {'ComputerName': computer_name, 'TimeZone': time_zone}
        return(dict)
        
    def getSoftwareInfo(self, hive):
        master = hive
        try:
            product_name = master.value("ProductName").value()
        except Registry.RegistryValueNotFoundException as e:
            product_name = "None Listed"
        try:
            csd_version = master.value("CSDVersion").value()
        except Registry.RegistryValueNotFoundException as e:
            csd_version = "None Listed"
        try:
            current_version = master.value("CurrentVersion").value()    
        except Registry.RegistryValueNotFoundException as e:
            current_version = "None Listed"
        try:
            current_build_number = master.value("CurrentBuildNumber").value()
        except Registry.RegistryValueNotFoundException as e:
            current_build_number = "None Listed"   
        try:
            registered_owner = master.value("RegisteredOwner").value()
        except Registry.RegistryValueNotFoundException as e:
            registered_owner = "None Listed"
        #2013-10-25T02:53:08Z
        try:
            installed_date = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(master.value("InstallDate").value()))
        except Registry.RegistryValueNotFoundException as e:
            installed_date = "None Listed"

        os_info = product_name +" "+ current_version +" "+ current_build_number +" "+ csd_version
        dict = {'OSInfo': os_info, 'Owner': registered_owner, 'InstallDate': installed_date}
        return(dict)