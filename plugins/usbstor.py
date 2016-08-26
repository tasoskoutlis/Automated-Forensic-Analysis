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
        
        usbstor_dict = dict()
        
        usb_keys = ["USBSTOR", "USB"]
        
        for hive in self.hives:
            current = HelperFunctions(hive).CurrentControlSet()
            for k in usb_keys:
                try:
                    key = Registry.Registry(hive).open('%s\\Enum\\%s' % (current, k))
                    for sks in key.subkeys():
                        key_lastwrite = sks.timestamp()
                        #SYSTEM\ControlSet001\Enum\USBSTOR\Disk&Ven_&Prod_USB_DISK_20X&Rev_PMAP
                        device_class_id = sks.name()
                        for uniqueSN in key.subkey(device_class_id).subkeys():
                            unique_sn_lastwrite = uniqueSN.timestamp()
                            try:
                                #Enum\USBSTOR\Disk&Ven_GoPro&Prod_Storage&Rev_1.0\123456789ABC&0\FriendlyName
                                friendly_name = uniqueSN.value("FriendlyName").value()
                            except Registry.RegistryValueNotFoundException:
                                friendly_name = "None"                       
                            usbstor_dict.setdefault(device_class_id, []).append((key_lastwrite, \
                                                                                 unique_sn_lastwrite, \
                                                                                 uniqueSN.name(), \
                                                                                 friendly_name))
                            
                except Registry.RegistryKeyNotFoundException as e:
                    continue
                    
            for key, val in usbstor_dict.iteritems():
                for vals in val:
                    key_lastwrite = vals[0]
                    unique_sn_lastwrite = vals[1]
                    unique_sn = vals[2]
                    friendly_name = vals[3]
                    
                    if self.format is not None:
                        template = Environment().from_string(self.format[0])
                        sys.stdout.write(template.render(key_lastwrite=key_lastwrite, \
                                                         key=key, \
                                                         friendly_name=friendly_name, \
                                                         unique_sn_lastwrite=unique_sn_lastwrite, \
                                                         unique_sn=unique_sn) + "\n")
                
                    elif self.format_file is not None:
                        with open(self.format_file[0], "rb") as f:
                            template = env.from_string(f.read())            
                            sys.stdout.write(template.render(key_lastwrite=key_lastwrite, \
                                                             key=key, \
                                                             friendly_name=friendly_name, \
                                                             unique_sn_lastwrite=unique_sn_lastwrite, \
                                                             unique_sn=unique_sn) + "\n")