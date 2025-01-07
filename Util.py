def copy_flat_dict(dict):
	new_dict = {}
	for key in dict.keys():
		new_dict[key] = dict[key]
	return new_dict