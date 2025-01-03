import itertools

import Items


def generate_production_tree(output_item, production_rate, default_only = True):
	production_tree = {}
	recipes = output_item.default_recipes
	if not default_only:
		recipes += output_item.alternate_recipes
	
	#get the defualt production paths
	#Build a tree that starts with each initial recipe and branches to each recipe of the initial recipe's input. Each branch of the tree should only use given inputs from its same branch
	for recipe in recipes:
		recipe_quantity = production_rate / recipe.outputs[output_item.name]
		recipe = recipe(recipe_quantity)
		production_tree[recipe] = []

		for input in recipe.inputs.keys(): #length of 0 when pulling from raw resource which will end recursion
			production_tree[recipe].append(generate_production_tree(Items.get_item_by_name(input), recipe.inputs[input], default_only))
	
	return production_tree

def split_production_tree(production_tree):
	'''
	Splits a production tree into a list of production paths
	'''
	production_paths = []
	for key in production_tree.keys(): #Each recipe
		input_paths = []
		for i in range(len(production_tree[key])): #Each input of the recipe, no inputs will end recursion
			input_paths.append(split_production_tree(production_tree[key][i]))

		#Each input from each input path should be paired with one other input from all other input paths
		for tup in itertools.product(*input_paths):
			production_paths.append({key: list(tup)})
	return production_paths

def get_production_recipes(production_branch):
	production_recipes = []
	for key in production_branch:
		production_recipes.append(key)
		for i in range(len(production_branch[key])): #Each input of the recipe, no inputs will end recursion
			production_recipes += get_production_recipes(production_branch[key][i])
	return production_recipes

#print(get_production_recipes(split_production_tree(generate_production_tree(Items.get_item_by_name("Automated Wiring"), 1))[0]))

def generate_setup(output_item_name, production_rate, power_limit = -1, given_inputs = {}, resource_rate_limitations = {"SAM": 0}, construction_limitations = {"Power Shard": 0, "Somersloop": 0}):
	'''
	Generates the production setup that meets the given requirements
	'''
	output_item = Items.get_item_by_name(output_item_name)

	#construct all production trees using only default recipes
	default_production_tree = generate_production_tree(output_item, production_rate, True)

	#construct all production trees using default and alternate recipes
	#complete_production_tree = generate_production_tree(output_item, production_rate, False)
	complete_production_tree = {}

	#When deciding which branch of a production tree to use, use the best recipe until it is not possible then the second best, and so on unil no recipes are possible or the resource requirement is fufilled

