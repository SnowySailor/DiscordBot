import yaml  # PyYAML library: http://pyyaml.org

def readSettings(name):
    file = open(name, encoding='utf-8')
    content = file.read()
    return content


def getSettings(name):
    data = readSettings(name)
    contents = yaml.load(data)
    return contents

def parseServerSettings(settings):
    parsedSettings = dict() # {name: (val, type)}
    for name, val in settings.items():
        if isinstance(val, dict):
            parsedSettings[name] = parseServerSettings(val)
            continue
        parsedSettings[name] = (val, type(val))
    return parsedSettings
