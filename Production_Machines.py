#Imports
import math

#Resource Nodes
class Resource_Node:
	purity = "Normal"

	def __init__(self, purity = "Normal"):
		#Set purity
		if not (purity == "Impure" or purity == "Normal" or purity == "Pure"):
			raise Exception(f"Purity: {purity}, is not a valid purity.")
		else:
			self.purity = purity

class Resource_Well:
	num_extractors = 0
	extractor_purities = []

	def __init__(self, extractor_purities):
		self.num_extractors = len(extractor_purities)
		
		#Set purities
		self.extractor_purities = []
		for purity in extractor_purities:
			if purity == "Impure" or purity == "Normal" or purity == "Pure":
				self.extractor_purities.append(purity)
			else:
				raise Exception(f"Purity: {purity}, is not a valid purity.")


#Production 
class Production_Machine:
	clock_speed = 1.0
	production_amplification_multiplier = 1.0
	num_machines = 0

	maximum_power_draw = 0
	total_somersloop_slots = 1

	construction_requirements = {}

	def __init__(self, num_machines, clock_speed = 1.0, filled_somersloop_slots = 0):
		self.num_machines = math.ceil(num_machines)
		self.clock_speed = num_machines / self.num_machines
		if self.total_somersloop_slots == 0:
			self.production_amplification_multiplier = 1
		else:
			self.production_amplification_multiplier = 1 + round(filled_somersloop_slots / self.total_somersloop_slots, 2)

		#Correct power draw for overclock
		self.maximum_power_draw = self.maximum_power_draw * round((self.clock_speed) ** math.log2(2.5), 3)

		#Correct power draw for somersloop production amplifier
		self.maximum_power_draw = self.maximum_power_draw * round((1 + (filled_somersloop_slots / self.total_somersloop_slots)) ** 2, 3)

		self.maximum_power_draw *= self.num_machines

		self.construction_requirements = self.construction_requirements.copy()
		for resource in self.construction_requirements.keys():
			self.construction_requirements[resource] *= self.num_machines


class Player(Production_Machine):
	num_machines = 1


class Resource_Miner(Production_Machine):
	resource_node = None

	def __init__(self, num_machines, resource_node = None, clock_speed = 1.0): #No production amplification
		super().__init__(num_machines, clock_speed)
		self.resource_node = resource_node	

class Resource_Miner_MK1(Resource_Miner):
	maximum_power_draw = 5

	construction_requirements = {
		"Portable Miner": 1,
		"Iron Plate": 10,
		"Concrete": 10
	}

class Resource_Miner_MK2(Resource_Miner):
	maximum_power_draw = 5

	construction_requirements = {
		"Portable Miner": 2,
		"Encased Industrial Beam": 10,
		"Steel Pipe": 20,
		"Modular Frame": 10
	}

class Resource_Miner_MK3(Resource_Miner):
	maximum_power_draw = 5

	construction_requirements = {
		"Portable Miner": 3,
		"Steel Pipe": 50,
		"Supercomputer": 5,
		"Fused Modular Frame": 10,
		"Turbo Motor": 3
	}

class Oil_Extractor(Resource_Miner):
	maximum_power_draw = 40

	construction_requirements = {
		"Motor": 15,
		"Encased Industrial Beam": 20,
		"Cable": 60
	}

class Resource_Well_Extractor(Resource_Miner):
	maximum_power_draw = 150

	construction_requirements = {
		"Radio Control Unit": 10,
		"Heavy Modular Frame": 25,
		"Motor": 50,
		"Alclad Aluminum Sheet": 50,
		"Rubber": 100
	}

class Water_Extractor(Resource_Miner):
	maximum_power_draw = 20
	resource_node = Resource_Node("Normal")

	construction_requirements = {
		"Copper Sheet": 20,
		"Reinforced Iron Plate": 10,
		"Rotor": 10
	}

class Converter(Production_Machine):
	maximum_power_draw = 400
	
	total_somersloop_slots = 2

	construction_requirements = {
		"Fused Modular Frame": 10,
		"Cooling System": 25,
		"Radio Control Unit": 50,
		"SAM Fluctuator": 100
	}

class Packager(Production_Machine):
	maximum_power_draw = 10

	construction_requirements = {
		"Steel Beam": 20,
		"Rubber": 10,
		"Plastic": 10
	}

class Constructor(Production_Machine):
	maximum_power_draw = 4

	construction_requirements = {
		"Reinforced Iron Plate": 2,
		"Cable": 8
	}

class Assembler(Production_Machine):
	maximum_power_draw = 15
	total_somersloop_slots = 2

	construction_requirements = {
		"Reinforced Iron Plate": 8,
		"Rotor": 4,
		"Cable": 10
	}

class Smelter(Production_Machine):
	maximum_power_draw = 4

	construction_requirements = {
		"Iron Rod": 5,
		"Wire": 8
	}

class Foundry(Production_Machine):
	maximum_power_draw = 16
	total_somersloop_slots = 2

	construction_requirements = {
		"Modular Frame": 10,
		"Rotor": 10,
		"Concrete": 20
	}

class Refinery(Production_Machine):
	maximum_power_draw = 30
	total_somersloop_slots = 2

	construction_requirements = {
		"Motor": 10,
		"Encased Industrial Beam": 10,
		"Steel Pipe": 30,
		"Copper Sheet": 20
	}

class Manufacturer(Production_Machine):
	maximum_power_draw = 55
	total_somersloop_slots = 4

	construction_requirements = {
		"Motor": 10,
		"Modular Frame": 20,
		"Plastic": 50,
		"Cable": 50
	}

class Blender(Production_Machine):
	maximum_power_draw = 75
	total_somersloop_slots = 4

	construction_requirements = {
		"Computer": 10,
		"Heavy Modular Frame": 10,
		"Motor": 20,
		"Aluminum Casing": 50
	}