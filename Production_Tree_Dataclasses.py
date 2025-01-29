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
	
	def get_branch(self, numeric_identifier):
		pass

class simple_path:
	def __init__(self, path_infornmation, iterable_identifier):
		'''
		Creates a simple production path with an numberic identifier so it's detailed path may be located within the larger production tree

		Parameters:
			path_infornmation (dict): dictionary containing basic path information (final recipe name, inputs, outputs, construction costs, energy use)
			iterable_identifier (iterable): ordered iterable of numbers representing the decisions to get this path in the production tree
		'''
		self.details = path_infornmation

		self.numeric_path = np.array(iterable_identifier, dtype="uint8")
		'''
		numeric path formatting:
		[
			section length,
			first decision, 
			1 input, 
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
		] -> [15, 0, 1, 12, 1, 2, 3, 0, 0, 6, 2, 1, 3, 0, 0]
		'''