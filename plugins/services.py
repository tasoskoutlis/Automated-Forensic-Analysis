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
        
        dict = {}
        
        for hive in self.hives:
            dict.update(self.processServices(hive))
         
        for key, val in dict.iteritems():
            last_write = val[0]
            key_name = key
            image_path = val[1]
            type_name = val[2]
            display_name = val[3]
            start_type = val[4]
            service_dll = val[5]
            

            if self.format_file is not None:
                with open(self.format_file[0], "rb") as f:
                    template = env.from_string(f.read())
                    sys.stdout.write(template.render(last_write=last_write, key_name=key_name, \
                                                     image_path=image_path, type_name=type_name, \
                                                     display_name=display_name, start_type=start_type, \
                                                     service_dll=service_dll) + "\n")
                    
            elif self.format is not None:
                template = Environment().from_string(self.format[0])
                sys.stdout.write(template.render(last_write=last_write, key_name=key_name, \
                                                 image_path=image_path, type_name=type_name, \
                                                 display_name=display_name, start_type=start_type, \
                                                 service_dll=service_dll) + "\n")
    
    def processServices(self, hive):
        
            current = HelperFunctions(hive).CurrentControlSet()
            services = Registry.Registry(hive).open('%s\\Services' % (current))
            
            service_list = []
            objects_list = []     
            
            for service in services.subkeys():
                service_list.append(service.name().lower())
    
            for service_name in service_list:
                k = Registry.Registry(hive).open('ControlSet001\\Services\\' + service_name)
                key_name = k.name()                
                last_write = str(k.timestamp())
                
                try:
                    type_name = k.value("Type").value()
                except:
                    type_name = "None"
                try:
                    image_path = k.value("ImagePath").value().lower()
                except:
                    image_path = "None"
                try:
                    display_name = k.value("DisplayName").value()
                except:
                    display_name = "None"
                try:
                    start_type = k.value("Start").value()
                except:
                    start_type = "None"
                try:
                    service_dll = k.subkey("Parameters").value("ServiceDll").value()
                except:
                    service_dll = "None"
                
                objects_list.append([last_write, key_name, image_path, type_name, display_name, start_type, service_dll])
                
            dict = {}
            for entry in objects_list:
                dict[entry[1]] = entry[0], entry[2], entry[3], entry[4], entry[5], entry[6]
                
            return(dict)