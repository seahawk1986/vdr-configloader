#!/usr/bin/python3

import configparser
from collections import OrderedDict

class Config:
    def __init__(self, config='vdr-settings.conf'):
        self.parser = configparser.SafeConfigParser(interpolation=configparser.ExtendedInterpolation(), allow_no_value=True, delimiters=(" ",":","="))
        #self.parser.optionxform = unicode
        with open(config, 'r', encoding='utf-8') as f:
            self.parser.readfp(f)
    def get_plugins(self):
        self.plugins = []
        if self.parser.has_section("Plugins"):
            for plugin, args in self.parser.items('Plugins'):
                if len(args) == 0:
                    self.plugins.append('-P %s' % plugin)
                else:
                    self.plugins.append(('-P "%s %s"' % (plugin, args)))
        return " ".join(self.plugins)


    def get_vdroptions(self):
        self.options = []
        if self.parser.has_section("Options"):
            for option, args in self.parser.items("Options"):
                if len(args) == 0:
                    self.options.append('%s' % option)
                else:
                    sep = lambda option: "=" if option.startswith("--") else " "
                    self.options.append(('%s%s%s' % (option, sep(option), args)))
            return " ".join(self.options)
        else:
            return ""


if __name__ == '__main__':

    config = Config()
    with open("vdr.conf", 'w', encoding='utf-8') as f:
        f.write("plugins=%s\n" % config.get_plugins())
        f.write("options=%s\n" % config.get_vdroptions())
    print(config.get_vdroptions() + " " + config.get_plugins())

