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
            for entry in self.processURLs(hive):
                last_write = entry[0]
                url_name = entry[1]
                url = entry[2]
            
                if self.format is not None:
                    template = Environment().from_string(self.format[0])
                    sys.stdout.write(template.render(last_write=last_write, \
                                                     url_name=url_name, \
                                                     url=url) + "\n")
            
                elif self.format_file is not None:
                    with open(self.format_file[0], "rb") as f:
                        template = env.from_string(f.read())            
                        sys.stdout.write(template.render(last_write=last_write, \
                                                         url_name=url_name, \
                                                         url=url) + "\n")            
            
    def processURLs(self, hive):
        list_of_urls = []
        
        try:
            for urls in Registry.Registry(hive).open("Software\\Microsoft\\Internet Explorer\\TypedURLs").values():
                last_write = Registry.Registry(hive).open("Software\\Microsoft\\Internet Explorer\\TypedURLs").timestamp()
                url_name = urls.name()
                url = urls.value()
                
                list_of_urls.append([last_write, url_name, url])
                
        except Registry.RegistryKeyNotFoundException as e:
            pass
        
        return(list_of_urls)