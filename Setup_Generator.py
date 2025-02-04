import itertools
import math
import time
import sys
import numpy as np

from PDL import *

import Util
import Production_Machines
import Recipes
import Items

import Production_Tree_Dataclasses


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

def get_simple_production_paths(production_paths):
	simple_production_paths = []
	for production_branch in production_paths:
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


@memoized
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


@memoized
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


@memoized
def get_max_energy_use(production_branch):
	production_recipes = get_production_recipes(production_branch)
	meu = 0 #max energy use
	for recipe in production_recipes:
		meu += recipe.production_machine.maximum_power_draw
	return meu


@memoized
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


def filter_production_tree(production_tree):
	'''
	Filters a production tree to only include paths that:
	  -  Output the expected amount
	  -  Don't include unnecessary intermediary steps that increase construction and energy costs
	
	Parameters:
		production_tree (dict): production tree
	
	Returns:
		(dict): filtered production tree
	'''

	#For each possible output recipe
	for recipe in production_tree:
		#Go down to lowest depth
		sub_requirements = production_tree[recipe]
		while sub_requirements != []: #while not at the lowest depth
			if sub_requirements == [{}]:
				print("Broken item in production tree. Fixing output.")
				sub_requirements = []
				break

			for sub_tree in sub_requirements: #for each production possiblity
				pass#sub_requirements = sub_tree[]



def filter_production_paths(production_paths, output_item, production_rate):
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
	del_indicies = set()

	lp = len(production_paths)
	memoized.memory_size = lp
	for i in range(lp):
		print(f"{i}/{lp}")
		#Set constants for the loop
		production_branch = production_paths[i]
		branch_max_energy_use = get_max_energy_use(production_branch)
		branch_requirements = get_construction_requirements(production_branch)

		branch_inputs = get_inputs(production_branch)
		branch_outputs = get_outputs(production_branch)

		branch_input_keys_length = len(branch_inputs.keys())
		branch_output_keys_length = len(branch_inputs.keys())

		#Check for expected output amount
		if branch_outputs[output_item.name] != production_rate:
			del_indicies.add(i)
			continue

		#Check for unnecessary intermediary steps

		# A path with unnecessary steps is considered such if it has:
		#  the same input/output quantities as another path 
		#  and 
		#  has a higher electrical consumption than the other path
		#  and
		#  more of each type of construction resource as the other path

		#Check if this path has the same inputs and outputs as any other paths and a higher electrical consumption
		#Then for each path that it does, check to see if this path has the same or more of each construction resouce of the path thereof
		for j in range(lp):
			#Don't check the path against itself or ones that have been removed
			if j == i or j in del_indicies:
				continue

			check_branch = production_paths[j]

			#Check input and output resources
			check_inputs = get_inputs(check_branch)
			check_outputs = get_outputs(check_branch)


			if len(check_inputs.keys()) != branch_input_keys_length:
				continue #Input resources cannot be the same if they are of differing lengths
			if len(check_outputs.keys()) != branch_output_keys_length:
				continue #Output resources cannot be the same if they are of differing lengths


			#Check electrical consumption of this path to every other path
			if branch_max_energy_use <= get_max_energy_use(production_paths[j]):
				continue #this check isn't true, so check is always false regardless of the others


			#Check input resource types
			broken = False
			for resource in branch_inputs.keys():
				if not resource in check_inputs.keys():
					broken = True
					break
				if branch_inputs[resource] != check_inputs[resource]:
					broken = True
					break
			if broken:
				continue #Loop was broken so the input resources of the paths are not the same


			#Check input resource types
			broken = False
			for resource in branch_outputs.keys():
				if not resource in check_outputs.keys():
					broken = True
					break
				if branch_outputs[resource] != check_outputs[resource]:
					broken = True
					break
			if broken:
				continue #Loop was broken so the output resources of the paths are not the same


			#Check construction resources of this path to every other path
			#Null hypothesis = this branch contains less or an equal amount of each construction resource than any other path
			#Alternate hypotheses = this branch contains more of each construction resource than any other path
			check_requirements = get_construction_requirements(production_paths[j])
			for requirement in check_requirements.keys():
				if not requirement in branch_requirements.keys():
					continue #if the resource in the check branch isn't required for this one
				

				if check_requirements[requirement] >= branch_requirements[requirement]:
					continue #if the resource in the check branch is more than or equal to the quantity this recipe needs
				
				#The null hypothesis was never proven so the alternate hypothesis is true and this branch should be removed
				del_indicies.add(i)
				break #second part of the check is true, so this production branch can be removed

	#Remove del indices
	for index in reversed(sorted(list(del_indicies))):
		del production_paths[index]
	
	memoized.memory_size = 50

	return production_paths

#["resource efficiency", "input resources", "byproducts", "construction cost", "electrical consumption"]
def sort_production_paths(production_paths, order_of_importance, input_resources, resource_efficiency_determinator = "ratio", construction_cost_determinator = "sink"):
	#Convert order of importance strings to functions
	for i in range(len(order_of_importance)):
		if order_of_importance[i] == "resource efficiency":
			order_of_importance[i] = lambda _production_paths: _sort_on_resource_efficiency(_production_paths, resource_efficiency_determinator)
		elif order_of_importance[i] == "input resources":
			order_of_importance[i] = lambda _production_paths: _sort_on_inputs(_production_paths, input_resources)
		elif order_of_importance[i] == "byproducts":
			order_of_importance[i] = lambda _production_paths: _sort_on_byproducts(_production_paths)
		elif order_of_importance[i] == "electrical consumption":
			order_of_importance[i] = lambda _production_paths: _sort_on_electrical_consumption(_production_paths)
		elif order_of_importance[i] == "construction cost":
			order_of_importance[i] = lambda _production_paths: _sort_on_construction_efficiency(_production_paths, construction_cost_determinator)
	
def _single_sort_production_paths(production_paths, sort_function):
	pass

def _sort_on_resource_efficiency(production_paths, efficiency_determinator):
	pass #efficiency level determined by ratio of input resources in the world, commanlity of input resource in the world, or sink value of input resources

def _sort_on_inputs(production_paths, input_resources):
	pass

def _sort_on_byproducts(production_paths):
	pass

def _sort_on_electrical_consumption(production_paths):
	pass

def _sort_on_construction_efficiency(production_paths, cost_determinator):
	pass #efficiency level determined by sink value of each construction resource, for now


def optimize_production_paths(sorted_production_paths, resource_rate_limitations, construction_limitations):
	'''
	Optimizes production paths to meet resource and construction limitations

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
	item_name = "Computer"
	quantity = 10 #per min

	gpt = generate_production_tree(Items.get_item_by_name(item_name), quantity, 2, False)

	production_tree = Production_Tree_Dataclasses.production_tree(gpt)
	simple_paths = production_tree.get_simple_paths()
	spt = split_production_tree(gpt)

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