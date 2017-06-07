import yaml # PyYAML library: http://pyyaml.org

def readSettings():
	file = open('config.yaml', encoding='utf-8')
	content = file.read()
	return content

def getSettings():
	data = readSettings()
	contents = yaml.load(data)
	return contents