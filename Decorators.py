import random

#Custom Decorator classes

class Recursive_Production(object):
	'''
	Decorator
	Allows for accessing a progress proportion for the recursive production function that is currently being ran using the proportiaonl completion calculation method
	'''
	current_progress = 0

	def __init__(self, func):
		self.func = func
	
	def __call__(self, *args, master_proportion = 1):
		if master_proportion == 1:
			self.current_progress = 0

		return_val = self.func(*args)

		#Total Recipes
		#self.current_progress += self._calculate_delta_recipe_proportion(...args)

		#Proportional Completion
		#self.current_progress += self._calculate_proportional_change(...args)

		#Random Counter
		self.current_progress = max(1, self.current_progress + self._calculate_random_count_change())
		return return_val
	
	'''
	Methods of determining load proportion:
	  1) Total recipes - recipes_completed / total_recipes 
	  		  -  needs to know total number of recipes from start
			  -  recipes_completed needs to be reset at the end of the recursion loop
	
	  2) Proportional completion - sum of (parent_proportion / iterations) at lowest depth for each recursive path 
	  		  -  needs to keep track of parent proportion (progress proportion of parent recipe for the current recipe)
	  		  -  needs to know which recipes on a branch are the lowest
			  -  proportion adding is based on branches finished rather than based on total recipes
		
	  3) Random Counter - proportion is the max of (1, 1 / random_n + proportion)
	  		  -  doesn't actually show the real proportion of completed values
			  -  only serves to give the user the idea that the computer is doing something
	'''

	def _calculate_delta_recipe_proportion(self, total_recipes):
		'''
		Total recipes = recipes_completed / total_recipes
		'''
		return round(1 / total_recipes, 5)
	

	def _calculate_proportional_change(self, parent_proportion, sibling_iterations, return_val):
		'''
		Proportional completion = sum of (parent_proportion / iterations) at lowest depth for each recursive path

		Parameters:
			parent_proportion (float): proportion that the parent would add to the proportional completion if completed
			sibling_iterations (int): number of siblings that this recipe has (number of children of the recipe's parent)
			return_val (dict): eturn value of the recursive production function for this recipe
		
		Returns:
			(float): change in proportion from the recursive production function completing,
			(float): parent proportion to use for this recipe's children
		'''
		node_proportion = round(parent_proportion / sibling_iterations, 5)

		if len(return_val.keys()) == 1 and list(return_val.values())[0] == []: #return dictionary should only have 1 empty list value for both raw resources & user input resources
			return node_proportion, node_proportion
		else:
			return 0, node_proportion
	

	def _calculate_random_count_change(self, total_recipe_range = [20, 6000]):
		'''
		Random Counter = the max of (1, 1 / random_n + proportion)

		Returns:
			(float): change in the random proportion
		'''
		return 1 / random.randint(*total_recipe_range)
