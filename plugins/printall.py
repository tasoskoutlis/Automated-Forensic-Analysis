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
            reg = Registry.Registry(hive).root()
            
            #https://github.com/williballenthin/python-registry/blob/master/samples/printall.py
            def rec(reg, depth=None):
                key_path = "\t" * depth + reg.path()
                if self.format is not None:
                    template = Environment().from_string(self.format[0])
                    sys.stdout.write(template.render(key_path=key_path) + "\n")
            
                elif self.format_file is not None:
                    with open(self.format_file[0], "rb") as f:
                        template = env.from_string(f.read())            
                        sys.stdout.write(template.render(key_path=key_path) + "\n")

                for subkey in reg.subkeys():
                    rec(subkey, depth + 1)

            rec(reg, depth=0)