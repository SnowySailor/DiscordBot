import copy

# Copies any values from `default` into `data`
def mergeDicts(default, data):
	changed = 0
	default = copy.deepcopy(default)
	for k, v in default.items():
		if k in data:
			if type(v) is dict:
				mergeDicts(v, data[k])
			pass
		else:
			data[k] = v
			changed = changed+1
	return changed
