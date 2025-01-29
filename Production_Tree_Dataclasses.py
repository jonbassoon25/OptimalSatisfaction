import numpy as np

#Dataclasses representing full production paths in a tree

class production_tree:
	def __init__(self, production_tree_dict):
		'''
		Creates a production tree dataclass that enables easy location of paths using path identifiers

		Parameters:
			production_tree_dict (dict): dictionary based production tree
		'''
		self.production_tree = production_tree_dict
	
	def get_branch(self, numeric_path, production_tree = None):
		if production_tree == None:
			production_tree = self.production_tree

		branch = {}
		current_key = list(production_tree.keys())[numeric_path[1]]
		branch[current_key] = []
		
		numeric_index = 3
		input_index = 0
		while numeric_index < len(numeric_path):
			
			branch[current_key].append(self.get_branch(numeric_path[numeric_index:numeric_index+numeric_path[numeric_index]], production_tree[current_key][input_index]))
			numeric_index += numeric_path[numeric_index]
			input_index += 1

		
		return branch
		


class simple_path:
	def __init__(self, path_information, iterable_path):
		'''
		Creates a simple production path with an iterable_path so that it's detailed path may be determined using the larger production tree

		Parameters:
			path_information (dict): dictionary containing basic path information (final recipe name, inputs, outputs, construction costs, energy use)
			iterable_path (iterable): ordered iterable of numbers representing the decisions to get this path in the production tree
		'''
		self.details = path_information

		self.numeric_path = np.array(iterable_path, dtype="uint8")
		'''
		numeric path formatting:
		[
			section length,
			first decision, 
			2 inputs,
			section length,
			second decision,
			2 inputs, 
			section length,
			first decision,
			0 inputs,
			section length,
			third decision,
			1 input,
			section length,
			first decision,
			0 inputs
		] -> [21, 0, 2, 12, 1, 2, 3, 0, 0, 6, 2, 1, 3, 0, 0, 6, 1, 1, 3, 0, 0]
		'''