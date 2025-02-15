def copy_flat_dict(dict):
	'''Returns a new dictionary with copied keys'''
	new_dict = {}
	for key in dict.keys():
		new_dict[key] = dict[key]
	return new_dict


def print_production_tree(production_tree, current_print_str = [], current_columns = set(), depth = 0):
	'''Prints a production tree to the console (non-functional)'''
	if depth == 0:
		current_print_str.append("Production Tree:")
		depth += 1
	
	current_columns.add(depth)

	for i in range(len(production_tree.keys())):
		recipe = list(production_tree.keys())[i]

		depth_prefix = (("  " * (depth-1)) if depth > 0 else "")
		for column_index in current_columns:
			if depth == column_index:
				continue
			depth_prefix = list(depth_prefix)
			depth_prefix[(column_index - 1) * 2] = "│"
			depth_prefix = ''.join(depth_prefix)

		if i >= len(production_tree.keys()) - 1:
			connector = "├─"
		else:
			connector = "└─"
		
		current_print_str.append(depth_prefix + connector + recipe.__class__.__name__.replace("_", " "))

		for sub_tree in production_tree[recipe]:
			print_production_tree(sub_tree, current_print_str, current_columns, depth + 1)
	
	current_columns.remove(depth)
	
	
	if depth == 1: #First call
		print("\n".join(current_print_str))


def display_box_content_to_dict(content):
	output = {}
	for arr in content:
		output[arr[0]] = arr[1]
	return output