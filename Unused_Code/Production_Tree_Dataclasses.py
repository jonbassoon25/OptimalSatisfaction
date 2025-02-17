import numpy as np
import itertools
import math

#Dataclasses representing full production paths in a tree

class production_tree:
	def __init__(self, production_tree_dict):
		'''
		Creates a production tree dataclass that enables easy location of paths using path identifiers

		Parameters:
			production_tree_dict (dict): dictionary based production tree
		'''
		self.production_tree = production_tree_dict

	def _get_numeric_paths(self, production_tree = None, depth = 0):
		if production_tree == None:
			production_tree = self.production_tree

		production_paths = []

		listed_keys = list(production_tree.keys())
		for i in range(len(listed_keys)): #Each recipe
			key = listed_keys[i]

			input_paths = []
			for j in range(len(production_tree[key])): #Each input of the recipe, no inputs will end recursion
				input_paths.append(self._get_numeric_paths(production_tree[key][j], depth + 1))
			
			#Join input paths
			if len(input_paths) == 0:
				production_paths.append([np.int8(2), np.int8(i)])
			else:
				total_products = math.prod([len(path) for path in input_paths])
				print([len(path) for path in input_paths])
				print(f"starting {total_products} products from {len(input_paths)} paths")

				product = itertools.product(*input_paths)
				print("finished product")

				for tup in product: #trillions of reps at scale (for computers)
					tup_list = []
					for val in tup: #not the issue (tup length not that long, ~1-3 for short test on computer production)
						tup_list += val

					production_paths.append([np.int8(len(tup_list) + 2), np.int8(i)] + tup_list)
				print("finished")

		#print(f"Current Depth: {depth}")
		return production_paths


	def _get_branch_recipes(self, branch):
		production_recipes = []
		for key in branch:
			production_recipes.append(key)
			for i in range(len(branch[key])): #Each input of the recipe, no inputs will end recursion
				production_recipes += self._get_branch_recipes(branch[key][i])
		return production_recipes
	
	def _get_branch_inputs(self, production_recipes):
		inputs = {}
		for recipe in production_recipes:
			if recipe.inputs == {}:
				recipe_output = list(recipe.outputs.keys())[0] #there is only 1 output for input / raw resources
				if recipe_output in inputs:
					inputs[recipe_output] += list(recipe.outputs.values())[0]
				else:
					inputs[recipe_output] = list(recipe.outputs.values())[0]
		return inputs
	
	def _get_branch_outputs(self, production_recipes):
		inputs = {}
		outputs = {}

		#add all inputs and outputs from each recipe
		for recipe in production_recipes:
			for input in recipe.inputs.keys():
				if input in inputs.keys():
					inputs[input] += recipe.inputs[input]
				else:
					inputs[input] = recipe.inputs[input]

			for output in recipe.outputs.keys():
				if output in outputs.keys():
					outputs[output] += recipe.outputs[output]
				else:
					outputs[output] = recipe.outputs[output]

		#get differences between values of outputs and inputs, clear 0's
		for output in list(outputs.keys()):
			if output in inputs.keys():
				outputs[output] -= inputs[output]
			if outputs[output] == 0: #Will be 0 if produced in exact quantity
				del outputs[output]
			
		return outputs
	
	def _get_max_energy_use(self, production_recipes):
		meu = 0 #max energy use
		for recipe in production_recipes:
			meu += recipe.production_machine.maximum_power_draw
		return meu

	def _get_construction_requirements(self, production_recipes):
		construction_requirements = {}
		for recipe in production_recipes:
			for key in recipe.production_machine.construction_requirements:
				if key in construction_requirements.keys():
					construction_requirements[key] += recipe.production_machine.construction_requirements[key] * math.ceil(recipe.quantity_multiplier)
				else:
					construction_requirements[key] = recipe.production_machine.construction_requirements[key]
		return construction_requirements
				

	def get_simple_paths(self):
		numeric_paths = self._get_numeric_paths()
		print(f"There are {len(numeric_paths)} paths")
		simple_paths = []
		for i in range(len(numeric_paths)):
			numeric_path = numeric_paths.pop(0)
			branch = self.get_branch(numeric_path)
			
			branch_recipes = self._get_branch_recipes(branch)

			#final recipe name, inputs, outputs, construction costs, energy use
			path_info = {
				"name": list(branch.keys())[0].__class__.__name__.replace("_", " "),
				"inputs": self._get_branch_inputs(branch_recipes),
				"outputs": self._get_branch_outputs(branch_recipes),
				"construction requirements": self._get_construction_requirements(branch_recipes),
				"max energy consumption": self._get_max_energy_use(branch_recipes)
			}

			simple_paths.append(simple_path(path_info, numeric_path))
		
		return simple_paths

	
	def get_branch(self, numeric_path, production_tree = None):
		if production_tree == None:
			production_tree = self.production_tree

		branch = {}
		current_key = list(production_tree.keys())[numeric_path[1]]
		branch[current_key] = []
		
		numeric_index = 2
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
		self.name = path_information["name"]
		self.inputs = path_information["inputs"]
		self.outputs = path_information["outputs"]
		self.construction_requirements = path_information["construction requirements"]
		self.max_energy_consumption = path_information["max energy consumption"]

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