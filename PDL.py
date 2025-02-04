#From the Python Decorator Library: https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
#Classes may be edited, this is noted in comments above their declarations

from collections.abc import Hashable
import functools

#Edited
class memoized(object):
	'''Decorator. Caches a function's return value each time it is called.
		If called later with the same arguments, the cached value is returned
		(not reevaluated).
	'''
	memory_size = 10
	def __init__(self, func):
		self.func = func
		self.cache = {}
	def __call__(self, *args):
		if len(args) > 1:
			parameter = args[1]
		else:
			parameter = args[0]
		if not isinstance(parameter, Hashable):
			parameter_name = id(parameter)
		else:
			parameter_name = parameter

		if parameter_name in self.cache:
			return self.cache[parameter_name]
		else:
			value = self.func(*args)
			self.cache[parameter_name] = value

			cache_key_list = list(self.cache.keys())
			while len(self.cache.keys()) > self.memory_size:
				del self.cache[cache_key_list.pop(0)]

			return value
	def __repr__(self):
		'''Return the function's docstring.'''
		return self.func.__doc__
	def __get__(self, obj, objtype):
		'''Support instance methods.'''
		return functools.partial(self.__call__, obj)