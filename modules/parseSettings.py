import yaml  # PyYAML library: http://pyyaml.org


def readSettings(name):
    file = open(name, encoding='utf-8')
    content = file.read()
    return content


def getSettings(name):
    data = readSettings(name)
    contents = yaml.load(data)
    return contents
