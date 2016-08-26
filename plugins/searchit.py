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
            for needle in self.search:
                paths = {}
                value_names = {}
                values = {}
                
                def rec(key, depth, needle):
                    
                    for value in key.values():
                        if (needle.lower() in value.name().lower()) or needle in value.name():
                            value_names.setdefault("Value Names",[]).append((key.path(), value.name()))
                        try:
                            if (needle.lower() in str(value.value()).lower()) or needle in str(value.value()):
                                values.setdefault("Values",[]).append((key.path(), value.name()))
                        except UnicodeEncodeError:
                            pass

                    for subkey in key.subkeys():
                        if needle in subkey.name():
                            paths.setdefault("Path",[]).append(subkey.path())
                            
                        rec(subkey, depth + 1, needle)

                reg = Registry.Registry(hive)
            
                rec(reg.root(), 0, needle)
                
                if self.format is not None:
                    print("Try using --format_file templates/searchit.html for now.")
                    exit(0)

                elif self.format_file is not None:
                    with open(self.format_file[0], "rb") as f:
                        template = env.from_string(f.read())            
                        sys.stdout.write(template.render(paths=paths, \
                                                         value_names=value_names, \
                                                         values=values, \
                                                         hive=hive) + "\n")