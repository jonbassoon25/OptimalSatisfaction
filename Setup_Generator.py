import itertools

import Util
import Production_Machines
import Recipes
import Items

def generate_production_tree(output_item, production_rate, miner_level, default_only = True, input_resources = {}):
	'''
	Recursivly generates a complete production tree for the given output item
	Excess input resources are not included as part of the tree

	Parameters:
		output_item (Item): Item to create the production tree for
		production_rate (number): Production rate in quantity per minute of the output item
		default_only (bool): Should only default recipes be used
		input_resources (dict): Dictionary of input resources formatted as {"item name": quantity per minute}
	
	Returns:
		(dict): Dictionary with array of possible production trees for each input of the output item going to only input resources, which have empty arrays
	'''
	if type(output_item) == type(""):
		output_item = Items.get_item_by_name(output_item)

	production_tree = {}
	recipes = output_item.default_recipes
	if not default_only:
		recipes += output_item.alternate_recipes

	#copy input resources for each recipe so that all production paths don't pull from a common input_resources object. Recursion will call this line for all sub-recipes
	input_resources = Util.copy_flat_dict(input_resources)
	
	if output_item.name in input_resources.keys():
		if production_rate <= input_resources[output_item.name]:
			input_resources[output_item.name] -= production_rate
			production_tree[Recipes.User_Provided_Resource({output_item.name: production_rate})] = []
			return production_tree
		else:
			production_rate -= input_resources[output_item.name]
			del input_resources[output_item.name]
	
	#get the defualt production paths
	#Build a tree that starts with each initial recipe and branches to each recipe of the initial recipe's input. Each branch of the tree should only use given inputs from its same branch
	for recipe in recipes:
		#Correct for special miner recipes. Don't allow miner levels that aren't specified
		#Correction bc work was already put in to do the miner levels in a not so good way
		if issubclass(recipe.production_machine, Production_Machines.Resource_Miner):
			if recipe.__name__.count("MK1") > 0 and miner_level != 1:
				continue
			elif recipe.__name__.count("MK2") > 0 and miner_level != 2:
				continue
			elif recipe.__name__.count("MK3") > 0 and miner_level != 3:
				continue

		recipe_quantity = production_rate / recipe.outputs[output_item.name]
		recipe = recipe(recipe_quantity)
		production_tree[recipe] = []

		for input in recipe.inputs.keys(): #length of 0 when pulling from raw resource which will end recursion
			production_tree[recipe].append(generate_production_tree(Items.get_item_by_name(input), recipe.inputs[input], miner_level, default_only, input_resources))
	
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

def get_inputs(production_branch):
	production_recipes = get_production_recipes(production_branch)
	inputs = {}
	for recipe in production_recipes:
		if recipe.inputs == {}:
			recipe_output = list(recipe.outputs.keys())[0] #there is only 1 output for input / raw resources
			if recipe_output in inputs:
				inputs[recipe_output] += list(recipe.outputs.values())[0]
			else:
				inputs[recipe_output] = list(recipe.outputs.values())[0]
	return inputs

def get_outputs(production_branch):
	production_recipes = get_production_recipes(production_branch)
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

def generate_setup(output_item_name, production_rate, miner_level, input_resources = {},
				   order_of_importance = ["maximize resource efficiency", "use input resources", "minimize byproducts", "minimize construction cost", "minimize energy consumption"], 
				   resource_rate_limitations = {"SAM": 0}, 
				   construction_limitations = {"Power Shard": 0, "Somersloop": 0}
		):
	'''
	Generates the production setup that meets the given requirements
	'''
	output_item = Items.get_item_by_name(output_item_name)

	#construct all production trees using only default recipes
	default_production_tree = generate_production_tree(output_item, production_rate, miner_level, True, input_resources)

	#construct all production trees using default and alternate recipes
	#complete_production_tree = generate_production_tree(output_item, production_rate, 2, False, input_resources)
	complete_production_tree = {}

	#When deciding which branch of a production tree to use, use the best recipe until it is not possible then the second best, and so on unil no recipes are possible or the resource requirement is fufilled

if __name__ == "__main__":
	item_name = "Smart Plating"
	quantity = 2000 #per min

	gpt = generate_production_tree(Items.get_item_by_name(item_name), quantity, 1)
	spt = split_production_tree(gpt)
	for production_branch in spt:
		print()
		production_recipes = get_production_recipes(production_branch)
		print(production_recipes)
		print()
		print([recipe.inputs if recipe.inputs != {} else None for recipe in production_recipes])
		print()
		print(get_inputs(production_branch))
		print(get_outputs(production_branch))
		print()