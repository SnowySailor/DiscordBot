import yaml  # PyYAML library: http://pyyaml.org
from ast import literal_eval as make_tuple

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

def parse(strVal, expectedType):
	retVal = None
	if expectedType is int:
		try:
			retVal = int(strVal)
			print(retVal)
		except ValueError:
			raise ValueError
	elif expectedType is str:
		retVal = strVal
	elif expectedType is tuple:
		try:
			retVal = make_tuple(strVal)
		except ValueError:
			raise ValueError
	elif expectedType is bool:
		if strVal.lower() == "true":
			retVal = True
		elif strVal.lower() == "false":
			retVal = False
	return retVal