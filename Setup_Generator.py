import itertools
import multiprocessing as mp
import multiprocessing.sharedctypes as mp_shared_ctypes
import ctypes

import Util
import Production_Machines
import Recipes
import Items
from Resource_Data import Resource_Data


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
	'''
	Creates a list of simple production paths from a production paths list
	
	Parameters:
		production_paths (list): production paths to generate the simple production paths for
	
	Returns:
		(list): the generated simple production paths
	'''
	simple_production_paths = []
	for production_branch in production_paths:
		simple_production_paths.append({
			"name": ' '.join(get_production_recipes(production_branch)[0].__class__.__name__.split("_")),
			"inputs": get_inputs(production_branch), 
			"outputs": get_outputs(production_branch)
			})
	return simple_production_paths


def get_production_recipes(production_branch):
	'''
	Calculates the recipes contained in a single production branch/path

	Parameters:
		production_branch (dict): production branch to get the paths of
	
	Returns:
		(list): paths of the production branch
	'''
	production_recipes = []
	for key in production_branch:
		production_recipes.append(key)
		for i in range(len(production_branch[key])): #Each input of the recipe, no inputs will end recursion
			production_recipes += get_production_recipes(production_branch[key][i])
	return production_recipes


def get_inputs(production_branch):
	'''
	Calculates the input resources for a single production branch/path

	Parameters:
		production_branch (dict): production branch to get the inputs of
	
	Returns:
		(dict): inputs of the production branch with their corresponding rates
	'''
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
	'''
	Calculates the output resources for a single production branch/path

	Parameters:
		production_branch (dict): production branch to get the outputs of
	
	Returns:
		(dict): outputs of the production branch with their corresponding rates
	'''
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
	'''
	Calculates the maximum energy use for a single production branch/path

	Parameters:
		production_branch (dict): production branch to get the maximum energy use of
	
	Returns:
		(number): maximum energy use of the production branch in MW
	'''
	production_recipes = get_production_recipes(production_branch)
	meu = 0 #max energy use
	for recipe in production_recipes:
		meu += recipe.production_machine.maximum_power_draw
	return meu


def get_construction_requirements(production_branch):
	'''
	Calculates the required construction resources for a single production branch/path

	Parameters:
		production_branch (dict): production branch to get the construction requirements of
	
	Returns:
		(dict): construction requirements of the production branch with their corresponding values
	'''
	production_recieps = get_production_recipes(production_branch)
	construction_requirements = {}
	for recipe in production_recieps:
		for key in recipe.production_machine.construction_requirements:
			if key in construction_requirements.keys():
				construction_requirements[key] += recipe.production_machine.construction_requirements[key]
			else:
				construction_requirements[key] = recipe.production_machine.construction_requirements[key]
	return construction_requirements


def _calc_should_del(queue, production_path_ids, production_path_data_by_id, should_del, output_item, production_rate):
	'''
	Multiprocess compatable function to filter production paths
	The provided queue must end with a Null value

	Parameters:
		queue (multiprocessing.Queue): The queue to pull index groups from
		production_path_ids (list): list of production path ids
		production_path_data_by_id (dict): production path data that can be accessed by each path's corresponding id
		should_del (multiprocessing.Array): The linked array to flip boolean values of to indicate which paths should be deleted
		output_item (string): Name of the output item of the paths
		production_rate (number): Production rate of the output item of the paths
	'''
	while True:
		#Set constants for the loop
		#print("awaiting queued i-group")
		i_group = queue.get()
		#print("recieved queued i-group")
		if i_group == None:
			queue.put(None)
			break

		lp = len(production_path_ids)
		print(f"starting group {i_group[0]}-{i_group[-1]}/{lp}")

		indicies_to_flip = set()

		for i in i_group:
			production_path_data = production_path_data_by_id[production_path_ids[i]]

			branch_max_energy_use = production_path_data["max energy"]
			branch_requirements = production_path_data["construction requirements"]
			
			branch_inputs = production_path_data["inputs"]
			branch_outputs = production_path_data["outputs"]

			branch_input_keys_length = len(branch_inputs.keys())
			branch_output_keys_length = len(branch_inputs.keys())

			#Check for expected output amount
			if not output_item.name in branch_outputs.keys(): #Shouldn't need, but do if recipes were misinputted
				raise Exception(f"Output not in output items: {output_item.name}")
			if branch_outputs[output_item.name] != production_rate:
				indicies_to_flip.add(i)
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
				if j == i:
					continue

				check_data = production_path_data_by_id[production_path_ids[j]]

				#Check input and output resources
				check_inputs = check_data["inputs"]
				check_outputs = check_data["outputs"]

				if len(check_inputs.keys()) != branch_input_keys_length:
					continue #Input resources cannot be the same if they are of differing lengths
				if len(check_outputs.keys()) != branch_output_keys_length:
					continue #Output resources cannot be the same if they are of differing lengths

				#Check electrical consumption of this path to every other path
				if branch_max_energy_use <= check_data["max energy"]:
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
				check_requirements = check_data["construction requirements"]
				for requirement in check_requirements.keys():
					if not requirement in branch_requirements.keys():
						continue #if the resource in the check branch isn't required for this one
						
					if check_requirements[requirement] >= branch_requirements[requirement]:
						continue #if the resource in the check branch is more than or equal to the quantity this recipe needs
						
					#The null hypothesis was never proven so the alternate hypothesis is true and this branch should be removed
					indicies_to_flip.add(i)
					break #second part of the check is true, so this production branch can be removed
		
		#flip indicies in should_del
		for index in indicies_to_flip:
			should_del[index] = True
		

def filter_production_paths(production_paths, output_item, production_rate, num_helpers = mp.cpu_count(), group_size = 500):
	'''
	Filters a production paths list to only include paths that:
	  -  Output the expected amount
	  -  Don't include unnecessary intermediary steps that increase construction and energy costs
	
	Parameters:
		production_paths (list): list of possible production paths
		output_item (string): Name of the output item of the paths
		production_rate (number): Production rate of the output item of the paths
		num_helpers (number): number of processes to use
		group_size (number): size of the queued index groups
	
	Returns:
		(list): list of filtered production paths
	'''
	if type(output_item) == type(""):
		output_item = Items.get_item_by_name(output_item)

	lp = len(production_paths)

	#set shared types for multiprocessing
	should_del = mp_shared_ctypes.Array(ctypes.c_bool, lp)

	#precompile inputs, outputs, energy, and construction requirment values
	print(f"Pregenerating Filter Data for {lp} Possible Production Paths...")
	production_path_ids = []
	production_path_data_by_id = {}
	for production_path in production_paths:
		production_path_ids.append(id(production_path))
		production_path_data_by_id[id(production_path)] = {
			"inputs": get_inputs(production_path),
			"outputs": get_outputs(production_path),
			"max energy": get_max_energy_use(production_path),
			"construction requirements": get_construction_requirements(production_path)
		}

	#initialize queue with groups of indicies for each process to calculate
	queue = mp.Queue()
	for i in range(0, len(production_paths), group_size):
		queue.put(tuple(range(i, min(len(production_paths), i + group_size))))
	
	queue.put(None) #flag for detection of queue end

	#--------------------

	#generate processes
	processes = []
	for i in range(num_helpers):
		processes.append(mp.Process(target=_calc_should_del, args=(queue, production_path_ids, production_path_data_by_id, should_del, output_item, production_rate)))

	#start processes
	print(f"Starting Computation with {len(processes)} Processes...")
	for process in processes:
		process.start()

	#join processes
	for process in processes:
		process.join()
	
	#--------------------

	if len(processes) == 0: #if there were no other processes to run the filter computations, do it on the main thread
		_calc_should_del(queue, production_path_ids, production_path_data_by_id, should_del, output_item, production_rate)

	#remove paths that have been filtered out
	for i in range(len(should_del) - 1, -1, -1):
		if should_del[i]:
			del production_paths[i]

	return production_paths


def sort_production_paths(production_paths, output_resource_name, order_of_importance, input_resources, resource_efficiency_determinator = "ratio", construction_cost_determinator = "sink"):
	'''
	Sorts a production paths list based on the given order of importance

	Parameters:
		production_paths (list): list of possible production paths
		output_resource_name (string): Name of the output item of the paths
		order_of_importance (list): Sort order (will weight paths based on first element, then sorts those of the same weight by the next element and so on)
		input_resources (dict): Input resources dictionary
		resource_efficiency_determinator (string): efficiency determinator for resource efficiency weight
		construction_cost_determinator (string): efficiency determinator for construction cost weight

	Returns:
		(list): sorted production paths
	'''
	#Convert order of importance strings to functions
	weight_order = []
	for i in range(len(order_of_importance)):
		if order_of_importance[i] == "resource efficiency":
			weight_order.append(lambda production_path: _get_resource_efficiency_weight(production_path, resource_efficiency_determinator))
		elif order_of_importance[i] == "input resources":
			weight_order.append(lambda production_path: _get_input_weight(production_path, input_resources))
		elif order_of_importance[i] == "byproducts":
			weight_order.append(lambda production_path: _get_byproduct_weight(production_path, output_resource_name))
		elif order_of_importance[i] == "electrical consumption":
			weight_order.append(lambda production_path: _get_electrical_consumption_weight(production_path))
		elif order_of_importance[i] == "construction cost":
			weight_order.append(lambda production_path: _get_construction_efficiency_weight(production_path, construction_cost_determinator))
		else:
			raise Exception(f"Importance identifier: {order_of_importance[i]} not recognized.")
	
	sorted_paths = _get_sorted_production_paths(production_paths, weight_order)
	
	return sorted_paths
	

def _get_sorted_production_paths(production_paths, ordered_weight_lambdas):
	'''
	Sorts production paths based on a list of ordered weight lambdas

	Parameters:
		production_paths (list): list of production paths to sort
		ordered_weight_lambdas (list): list of ordered weight lambdas to use to determine sorting weights

	Returns:
		(list): sorted production paths
	'''
	production_paths_by_weight = {}

	#get path weights
	for path in production_paths:
		path_weight = ordered_weight_lambdas[0](path)
		if path_weight in production_paths_by_weight.keys():
			production_paths_by_weight[path_weight].append(path)
		else:
			production_paths_by_weight[path_weight] = [path]
	
	#sort path weights from smallest to largest
	sorted_ppbw = {}
	key_list = list(production_paths_by_weight.keys())
	for i in range(len(key_list)):
		smallest_weight = key_list[i]
		for j in range(len(production_paths_by_weight.keys())):
			if key_list[j] in sorted_ppbw.keys():
				continue
			if smallest_weight in sorted_ppbw.keys():
				smallest_weight = key_list[j]
				continue
			check_weight = key_list[j]
			if check_weight < smallest_weight:
				smallest_weight = check_weight

		sorted_ppbw[smallest_weight] = production_paths_by_weight[smallest_weight]

	#change sorted ppbw into an array without keys
	sorted_production_paths = []
	append_flag = False
	for value in sorted_ppbw.values():
		if len(value) == 1:
			sorted_production_paths.append(value[0])
		else:
			sorted_production_paths.append(value)
			append_flag = True

	if append_flag: #if there is more than one sorted production path with values of the same weight
		#call this function with one less ordered weight lambda for each key with more than one value in its array
		for i in range(len(sorted_production_paths) - 1, -1, -1):
			if type(sorted_production_paths[i]) == list:
				if len(ordered_weight_lambdas) > 1:
					new_sorted_paths = _get_sorted_production_paths(sorted_production_paths.pop(i), ordered_weight_lambdas[1:])
				else:
					#print("Warning: There are multiple paths of equal weight.")
					new_sorted_paths = sorted_production_paths.pop(i)

				#Add paths to full storted production path list
				for path in reversed(new_sorted_paths):
					sorted_production_paths.insert(i, path)

	if len(sorted_production_paths) != len(production_paths):
		raise Exception(f"{len(production_paths) - len(sorted_production_paths)} paths were deleted in sort of lambda {5 - len(ordered_weight_lambdas)}")
	
	return sorted_production_paths
			

def _get_resource_efficiency_weight(production_path, efficiency_determinator = "ratio"):
	'''
	Calculates the resource efficiency weight of a production path

	Parameters:
		production_path (dict): path to determine the weight of
		efficiency_determinator (string): method of determining efficiency weight
	
	Returns:
		(number): weight of the path (lower is better)
	'''
	#efficiency level determined by ratio of input resources in the world, commonality of input resource in the world, or sink value of input resources
	inputs = get_inputs(production_path)
	weight = 0
	for input in inputs.keys():
		weight += _get_resource_weight(input, efficiency_determinator) * inputs[input]
		#print(f"weight of {inputs[input]} {input} is {_get_resource_weight(input, efficiency_determinator) * inputs[input]}")
	
	return weight


def _get_input_weight(production_path, input_resources):
	'''
	Calculates the input utilization weight of a production path

	Parameters:
		production_path (dict): path to determine the weight of
		input_resources (dict): player provided input resources
	
	Returns:
		(number): weight of the path (lower is better)
	'''
	#based on avg proportion of input resources used
	inputs = get_inputs(production_path)
	input_resources = input_resources.copy()
	weight = 0
	for input_resource in input_resources.keys():
		if input_resource in inputs.keys():
			input_resources[input] = 1 - (max(0, input_resources[input_resource] - inputs[input_resource]) / input_resources[input_resource])
		weight += input_resources[input]
	
	if len(input_resources.keys()) > 0:
		return weight / len(input_resources.keys())
	else:
		return 0


def _get_byproduct_weight(production_path, output_resource_name):
	'''
	Calculates the byproduct weight of a production path

	Parameters:
		production_path (dict): path to determine the weight of
		output_resource_name (string): name of the desired output resource of the production path
	
	Returns:
		(number): weight of the path (lower is better)
	'''
	#based on sink value of byproducts
	outputs = get_outputs(production_path)
	weight = 0
	for output in list(outputs.keys()):
		if output == output_resource_name:
			continue #this resource is the desired output
		weight += _get_resource_weight(output, "sink") * outputs[output]
	
	return weight


def _get_electrical_consumption_weight(production_path):
	'''
	Calculates the electrical consumption weight of a production path

	Parameters:
		production_path (dict): path to determine the weight of
	
	Returns:
		(number): weight of the path (lower is better)
	'''
	return get_max_energy_use(production_path)


def _get_construction_efficiency_weight(production_path, cost_determinator = "sink"):
	'''
	Calculates the construction efficiency weight of a production path

	Parameters:
		production_path (dict): path to determine the weight of
		cost_determinator (string): method of determining efficiency weight
	
	Returns:
		(number): weight of the path (lower is better)
	'''
	#efficiency level determined by sink value of each construction resource, for now
	construction_requirements = get_construction_requirements(production_path)
	weight = 0
	for requirement in construction_requirements.keys():
		weight += _get_resource_weight(requirement, cost_determinator) * construction_requirements[requirement]

	return weight


def _get_resource_weight(resource_name, determinator):
	'''
	Calculates the weight value for a resource

	Parameters:
		resource_name (string): name of the resource to calculate the weight of
		determinator (string): method of calculating the weight
	
	Returns:
		(number): weight of the resource (lower means more common)
	'''
	if determinator == "ratio":
		if not resource_name in Resource_Data.resource_ratios:
			return 0 #input resources not in the ratios table are either supplied by player or are water
		return Resource_Data.resource_ratios[resource_name]
	elif determinator == "commonality":
		if not resource_name in Resource_Data.resource_commonality_table:
			return -1
		return Resource_Data.resource_commonality_table.index(resource_name)
	elif determinator == "sink":
		sink_yield = Items.get_item_by_name(resource_name).sink_yield
		if sink_yield == None:
			#print(f"Item: {resource_name} has a sink yield of None")
			sink_yield = 0
		return sink_yield
	else:
		raise Exception(f"Determinator: {determinator} not recognized")


if __name__ == "__main__":
	#Test Case
	item_name = "Plastic"
	quantity = 10 #per min

	gpt = generate_production_tree(Items.get_item_by_name(item_name), quantity, 2, False)
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