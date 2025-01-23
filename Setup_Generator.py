import itertools
import math
import time

import Util
import Production_Machines
import Recipes
import Items

def generate_production_tree(output_item, production_rate, miner_level, default_only = True, input_resources = {}, blacklist_recipes = set()):
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
	recipes = output_item.default_recipes.copy()
	if not default_only:
		recipes += output_item.alternate_recipes.copy()


	#copy input resources for each recipe so that all production paths don't pull from a common input_resources object. Recursion will call this line for all sub-recipes
	input_resources = Util.copy_flat_dict(input_resources)


	if output_item.name in input_resources.keys():
		if output_item.name == "Empty Canister":
			production_tree[Recipes.User_Provided_Resource({"Empty Canister": production_rate})] = []
			return production_tree
		
		if production_rate <= input_resources[output_item.name]:
			input_resources[output_item.name] -= production_rate
			production_tree[Recipes.User_Provided_Resource({output_item.name: production_rate})] = []
			return production_tree
		else:
			production_rate -= input_resources[output_item.name]
			del input_resources[output_item.name]

	#get the default production paths
	#Build a tree that starts with each initial recipe and branches to each recipe of the initial recipe's input. Each branch of the tree should only use given inputs from its same branch
	for recipe in recipes:
		#Correct for blacklisted recipes to avoid looping production
		if recipe in blacklist_recipes:
			continue

		#Only use package recipes if there are canisters in input resources
		if "Empty Canister" in recipe.inputs.keys() and not "Empty Canister" in input_resources.keys():
			continue

		#Only use unpackage recipes if there is a provided input of that packaged resource. Only 1 input for unpackage recipes
		if "Empty Canister" in recipe.outputs.keys() and not list(recipe.inputs.keys())[0] in input_resources.keys():
			continue

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

		next_blacklist_recipes = blacklist_recipes.copy()
		next_blacklist_recipes.add(recipe.__class__)

		for input in recipe.inputs.keys(): #length of 0 when pulling from raw resource which will end recursion
			production_tree[recipe].append(generate_production_tree(Items.get_item_by_name(input), recipe.inputs[input], miner_level, default_only, input_resources, blacklist_recipes=next_blacklist_recipes))

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

def get_simple_production_paths(production_branch):
	simple_production_paths = []
	for production_branch in production_branch:
		simple_production_paths.append({
			"name": ' '.join(get_production_recipes(production_branch)[0].__class__.__name__.split("_")),
			"inputs": get_inputs(production_branch), 
			"outputs": get_outputs(production_branch)
			})
	return simple_production_paths

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


def get_max_energy_use(production_branch):
	production_recipes = get_production_recipes(production_branch)
	meu = 0 #max energy use
	for recipe in production_recipes:
		meu += recipe.production_machine.maximum_power_draw
	return meu

def get_construction_requirements(production_branch):
	production_recieps = get_production_recipes(production_branch)
	construction_requirements = {}
	for recipe in production_recieps:
		for key in recipe.production_machine.construction_requirements:
			if key in construction_requirements.keys():
				construction_requirements[key] += recipe.production_machine.construction_requirements[key] * math.ceil(recipe.quantity_multiplier)
			else:
				construction_requirements[key] = recipe.production_machine.construction_requirements[key]
	return construction_requirements


def filter_production_paths(simple_production_paths, production_paths, output_item, production_rate):
	'''
	Filters a production paths list to only include paths that:
	  -  Output the expected amount
	  -  Don't include unnecessary intermediary steps that increase construction and energy costs
	
	Parameters:
		production_paths (list): list of possible production paths
	
	Returns:
		(list): list of filtered production paths
	'''
	if type(output_item) == type(""):
		output_item = Items.get_item_by_name(output_item)

	for production_branch in production_paths:
		#Check for expected output amount
		if get_outputs(production_branch)[output_item.name] != production_rate:
			del production_paths[production_paths.index(production_branch)]
			continue
			
		#Check for unnecessary intermediary steps

		# A path with unnecessary steps is considered such if it has:
		#  the same inputs/outputs as another path with a higher electrical consumption
		#  and
		#  the same or more of each type of construction resource as the other path

		#Check if this path has the same inputs and outputs as any other paths and a higher electrical consumption
		pass

		#For each path that it does, check to see if this path has the same or more of each construction resouce of the path thereof
		for other_path in []:
			for i in []: #loop through construction resources
				pass #If this path has the same or more of all construction resources, this path should be deleted as it is unnecessary
	
	return production_paths


def sort_production_paths(production_paths, order_of_importance, input_resources):
	pass


def optimize_production_paths(sorted_production_paths, resource_rate_limitations, construction_limitations):
	'''
	Optimizes production paths to meet resource and construction limitations by using the best possible path until it is no longer possible and then using the next best

	Parameters:
		sorted_production_paths (list): list of sorted production paths
		resource_rate_limitations (dict): dictionary of resource rate limitations (format: {"resource": quantity/min})
		construction_limitations (dict): dictionary of construction limitations (format: {"resource": quantity})
	
	Returns:
		(list): sorted list of optimized production paths
	'''


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
	item_name = "Plastic"
	quantity = 10 #per min

	gpt = generate_production_tree(Items.get_item_by_name(item_name), quantity, 1, False)
	spt = split_production_tree(gpt)
	print(spt)
	for production_branch in spt:
		print()
		print(production_branch)
		print()
		production_recipes = get_production_recipes(production_branch)
		print(production_recipes)
		print()
		print([recipe.inputs for recipe in production_recipes])
		print()
		print(get_inputs(production_branch))
		print(get_outputs(production_branch))
		print()