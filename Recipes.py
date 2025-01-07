#Imports
import Util
import Production_Machines as PMs

class Recipe:
	quantity_multiplier = 1
	production_machine = PMs.Production_Machine
	inputs = {}
	outputs = {}
	
	def __init__(self, quantity_multiplier = 1):
		'''
		Parameters:
			quantity_produced (float): amount of times this recipe is produced
		'''
		self.inputs = Util.copy_flat_dict(self.inputs)
		self.outputs = Util.copy_flat_dict(self.outputs)

		self.quantity_multiplier = quantity_multiplier
		for input in self.inputs.keys():
			self.inputs[input] *= self.quantity_multiplier
		for output in self.outputs.keys():
			self.outputs[output] *= self.quantity_multiplier

class User_Provided_Resource(Recipe):
	inputs = {}
	outputs = {}

	def __init__(self, outputs):
		self.outputs = outputs

#Ores
class Iron_Ore_MK1(Recipe):
	production_machine = PMs.Resource_Miner_MK1
	outputs = {"Iron Ore": 60}
class Iron_Ore_MK2(Recipe):
	production_machine = PMs.Resource_Miner_MK2
	outputs = {"Iron Ore": 120}
class Iron_Ore_MK3(Recipe):
	production_machine = PMs.Resource_Miner_MK3
	outputs = {"Iron Ore": 240}
class Iron_Ore_SAM_L(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Limestone": 240}
	outputs = {"Iron Ore": 120}

class Copper_Ore_MK1(Recipe):
	production_machine = PMs.Resource_Miner_MK1
	outputs = {"Copper Ore": 60}
class Copper_Ore_MK2(Recipe):
	production_machine = PMs.Resource_Miner_MK2
	outputs = {"Copper Ore": 120}
class Copper_Ore_MK3(Recipe):
	production_machine = PMs.Resource_Miner_MK3
	outputs = {"Copper Ore": 240}
class Copper_Ore_SAM_Q(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Raw Quartz": 100}
	outputs = {"Copper Ore": 120}
class Copper_Ore_SAM_S(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Sulfer": 120}
	outputs = {"Copper Ore": 120}

class Limestone_MK1(Recipe):
	production_machine = PMs.Resource_Miner_MK1
	outputs = {"Limestone": 60}
class Limestone_MK2(Recipe):
	production_machine = PMs.Resource_Miner_MK2
	outputs = {"Limestone": 120}
class Limestone_MK3(Recipe):
	production_machine = PMs.Resource_Miner_MK3
	outputs = {"Limestone": 240}
class Limestone_SAM_S(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Sulfer": 20}
	outputs = {"Limestone": 120}

class Coal_MK1(Recipe):
	production_machine = PMs.Resource_Miner_MK1
	outputs = {"Coal": 60}
class Coal_MK2(Recipe):
	production_machine = PMs.Resource_Miner_MK2
	outputs = {"Coal": 120}
class Coal_MK3(Recipe):
	production_machine = PMs.Resource_Miner_MK3
	outputs = {"Coal": 240}
class Coal_SAM_I(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Iron Ore": 180}
	outputs = {"Coal": 120}
class Coal_SAM_L(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Limestone": 360}
	outputs = {"Coal": 120}
class Biocoal(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Biomass": 37.5}
	outputs = {"Coal": 45}
class Charcoal(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Wood": 15}
	outputs = {"Coal": 150}

class Quartz_MK1(Recipe):
	production_machine = PMs.Resource_Miner_MK1
	outputs = {"Raw Quartz": 60}
class Quartz_MK2(Recipe):
	production_machine = PMs.Resource_Miner_MK2
	outputs = {"Raw Quartz": 120}
class Quartz_MK3(Recipe):
	production_machine = PMs.Resource_Miner_MK3
	outputs = {"Raw Quartz": 240}
class Quartz_SAM_B(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Bauxite": 100}
	outputs = {"Raw Quartz": 120}
class Quartz_SAM_O(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Coal": 240}
	outputs = {"Raw Quartz": 120}

class Caterium_Ore_MK1(Recipe):
	production_machine = PMs.Resource_Miner_MK1
	outputs = {"Caterium Ore": 60}
class Caterium_Ore_MK2(Recipe):
	production_machine = PMs.Resource_Miner_MK2
	outputs = {"Caterium Ore": 120}
class Caterium_Ore_MK3(Recipe):
	production_machine = PMs.Resource_Miner_MK3
	outputs = {"Caterium Ore": 240}
class Caterium_Ore_SAM_C(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Copper Ore": 150}
	outputs = {"Caterium Ore": 120}
class Caterium_Ore_SAM_Q(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Raw Quartz": 120}
	outputs = {"Caterium Ore": 120}

class Sulfer_MK1(Recipe):
	production_machine = PMs.Resource_Miner_MK1
	outputs = {"Sulfer": 60}
class Sulfer_MK2(Recipe):
	production_machine = PMs.Resource_Miner_MK2
	outputs = {"Sulfer": 120}
class Sulfer_MK3(Recipe):
	production_machine = PMs.Resource_Miner_MK3
	outputs = {"Sulfer": 240}
class Sulfer_SAM_O(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Coal": 200}
	outputs = {"Sulfer": 120}
class Sulfer_SAM_I(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Iron Ore": 300}
	outputs = {"Sulfer": 120}

class Bauxite_MK1(Recipe):
	production_machine = PMs.Resource_Miner_MK1
	outputs = {"Bauxite": 60}
class Bauxite_MK2(Recipe):
	production_machine = PMs.Resource_Miner_MK2
	outputs = {"Bauxite": 120}
class Bauxite_MK3(Recipe):
	production_machine = PMs.Resource_Miner_MK3
	outputs = {"Bauxite": 240}
class Bauxite_SAM_G(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Caterium": 150}
	outputs = {"Bauxite": 120}
class Bauxite_SAM_C(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Copper Ore": 180}
	outputs = {"Bauxite": 120}

class Uranium_Ore_MK1(Recipe):
	production_machine = PMs.Resource_Miner_MK1
	outputs = {"Uranium Ore": 60}
class Uranium_Ore_MK2(Recipe):
	production_machine = PMs.Resource_Miner_MK2
	outputs = {"Uranium Ore": 120}
class Uranium_Ore_MK3(Recipe):
	production_machine = PMs.Resource_Miner_MK3
	outputs = {"Uranium Ore": 240}
class Uranium_Ore_SAM_B(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Bauxite": 480}
	outputs = {"Uranium Ore": 120}

class SAM_MK1(Recipe):
	production_machine = PMs.Resource_Miner_MK1
	outputs = {"SAM": 60}
class SAM_MK2(Recipe):
	production_machine = PMs.Resource_Miner_MK2
	outputs = {"SAM": 120}
class SAM_MK3(Recipe):
	production_machine = PMs.Resource_Miner_MK3
	outputs = {"SAM": 240}

class Crude_Oil(Recipe):
	production_machine = PMs.Oil_Extractor
	outputs = {"Crude Oil": 120}
class Crude_Oil_Well(Recipe):
	production_machine = PMs.Resource_Well_Extractor
	outputs = {"Crude Oil": 60}
class Unpackage_Oil(Recipe):
	production_machine = PMs.Packager
	inputs = {"Packaged Oil": 60}
	outputs = {"Crude Oil": 60, "Empty Canister": 60}

class Nitrogen_Gas(Recipe):
	production_machine = PMs.Resource_Well_Extractor
	outputs = {"Nitrogen Gas": 60}
class Unpackage_Nitrogen_Gas(Recipe):
	production_machine = PMs.Packager
	inputs = {"Packaged Nitrogen Gas": 60}
	outputs = {"Nitrogen Gas": 240, "Empty Fluid Tank": 60}
class Nitrogen_Gas_SAM_B(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Bauxite": 100}
	outputs = {"Nitrogen Gas": 120}
class Nitrogen_Gas_SAM_C(Recipe):
	production_machine = PMs.Converter
	inputs = {"Reanimated SAM": 10, "Caterium": 120}
	outputs = {"Nitrogen Gas": 120}

class Water(Recipe):
	production_machine = PMs.Water_Extractor
	outputs = {"Water": 120}
class Unpackage_Water(Recipe):
	production_machine = PMs.Packager
	inputs = {"Packaged Water": 120}
	outputs = {"Water": 120, "Empty Canister": 120}

class Portable_Miner(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Steel Pipe": 4, "Iron Plate": 4}
	outputs = {"Portable Miner": 1}

class Iron_Ingot(Recipe):
	production_machine = PMs.Smelter
	inputs = {"Iron Ore": 30}
	outputs = {"Iron Ingot": 30}
class Basic_Iron_Ingot(Recipe):
	production_machine = PMs.Foundry
	inputs = {"Iron Ore": 25, "Limestone": 40}
	outputs = {"Iron Ingot": 50}
class Iron_Alloy_Ingot(Recipe):
	production_machine = PMs.Foundry
	inputs = {"Iron Ore": 40, "Copper Ore": 10}
	outputs = {"Iron Ingot": 75}
class Leached_Iron_Ingot(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Iron Ore": 50, "Sulfuric Acid": 10}
	outputs = {"Iron Ingot": 100}
class Pure_Iron_Ingot(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Iron Ore": 35, "Water": 20}
	outputs = {"Iron Ingot": 65}

class Iron_Plate(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Iron Ingot": 30}
	outputs = {"Iron Plate": 20}
class Coated_Iron_Plate(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Iron Ingot": 37.5, "Plastic": 7.5}
	outputs = {"Iron Plate": 75}
class Steel_Cast_Plate(Recipe):
	production_machine = PMs.Foundry
	inputs = {"Iron Ingot": 15, "Steel Ingot": 15}
	outputs = {"Iron Plate": 45}

class Iron_Rod(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Iron Ingot": 15}
	outputs = {"Iron Rod": 15}
class Aluminum_Rod(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Aluminum Ingot": 7.5}
	outputs = {"Iron Rod": 52.5}
class Steel_Rod(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Steel Ingot": 12}
	outputs = {"Iron Rod": 48}

class Copper_Ingot(Recipe):
	production_machine = PMs.Smelter
	inputs = {"Copper Ore": 30}
	outputs = {"Copper Ingot": 30}
class Copper_Alloy_Ingot(Recipe):
	production_machine = PMs.Foundry
	inputs = {"Copper Ore": 50, "Iron Ore": 50}
	outputs = {"Copper Ore": 100}
class Leached_Copper_Ingot(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Copper Ore": 45, "Sulfuric Acid": 25}
	outputs = {"Copper Ingot": 110}
class Pure_Copper_Ingot(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Copper Ore": 15, "Water": 10}
	outputs = {"Copper Ingot": 37.5}
class Tempered_Copper_Ingot(Recipe):
	production_machine = PMs.Foundry
	inputs = {"Copper Ore": 25, "Petroleum Coke": 40}
	outputs = {"Copper Ingot": 60}

class Wire(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Copper Ingot": 15}
	outputs = {"Wire": 30}
class Caterium_Wire(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Caterium Ingot": 15}
	outputs = {"Wire": 120}
class Fused_Wire(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Copper Ingot": 12, "Caterium Ingot": 3}
	outputs = {"Wire": 90}
class Iron_Wire(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Iron Ingot": 12.5}
	outputs = {"Wire": 22.5}

class Cable(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Wire": 60}
	outputs = {"Cable": 30}
class Coated_Cable(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Wire": 37.5, "Heavy Oil Residue": 15}
	outputs = {"Cable": 67.5}
class Insulated_Cable(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Wire": 45, "Rubber": 30}
	outputs = {"Cable": 100}
class Quickwire_Cable(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Quickwire": 7.5, "Rubber": 5}
	outputs = {"Cable": 27.5}

class Concrete(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Limestone": 45}
	ouputs = {"Concrete": 15}
class Fine_Concrete(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Silica": 15, "Limestone": 60}
	outputs = {"Concrete": 50}
class Rubber_Concrete(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Limestone": 100, "Rubber": 20}
	outputs = {"Concrete": 90}
class Wet_Concrete(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Limestone": 120, "Water": 100}
	outputs = {"Concrete": 80}

class Screw(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Iron Rod": 10}
	outputs = {"Screw": 40}
class Cast_Screw(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Iron Ingot": 12.5}
	outputs = {"Screw": 50}
class Steel_Screw(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Steel Beam": 5}
	outputs = {"Screw": 260}

class Reinforced_Iron_Plate(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Iron Plate": 30, "Screw": 60}
	outputs = {"Reinforced Iron Plate": 5}
class Adhered_Iron_Plate(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Iron Plate": 11.25, "Rubber": 3.75}
	outputs = {"Reinforced Iron Plate": 3.75}
class Bolted_Iron_Plate(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Iron Plate": 90, "Screw": 250}
	outputs = {"Reinforced Iron Plate": 15}
class Stitched_Iron_Plate(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Iron Plate": 18.75, "Wire": 37.5}

class Biomass_A(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Alien Protein": 15}
	outputs = {"Biomass": 1500}
class Biomass_L(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Leaves": 120}
	outputs = {"Biomass": 60}
class Biomass_M(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Mycelia": 15}
	outputs = {"Biomass": 150}
class Biomass_W(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Wood": 60}
	outputs = {"Biomass": 300}

class Copper_Sheet(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Copper Ingot": 20}
	outputs = {"Copper Sheet": 10}
class Steamed_Copper_Sheet(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Copper Ingot": 22.5, "Water": 22.5}
	outputs = {"Copper Sheet": 22.5}

class Rotor(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Iron Rod": 20, "Screw": 100}
	outputs = {"Rotor": 4}
class Copper_Rotor(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Copper Sheet": 22.5, "Screw": 195}
	outputs = {"Rotor": 11.25}
class Steel_Rotor(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Steel Pipe": 10, "Wire": 30}
	outputs = {"Rotor": 5}

class Modular_Frame(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Reinforced Iron Plate": 3, "Iron Rod": 12}
	outputs = {"Modular Frame": 2}
class Bolted_Frame(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Reinforced Iron Plate": 7.5, "Screw": 140}
	outputs = {"Modular Frame": 5}
class Steeled_Frame(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Reinforced Iron Plate": 2, "Steel Pipe": 10}
	outputs = {"Modular Frame": 3}

class Smart_Plating(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Reinforced Iron Plate": 2, "Rotor": 2}
	outputs = {"Smart Plating": 2}
class Plastic_Smart_Plating(Recipe):
	production_machine = PMs.Manufacturer
	inputs = {"Reinforced Iron Plate": 2.5, "Rotor": 2.5, "Plastic": 7.5}
	outputs = {"Smart Plating": 5}

class Solid_Biofuel(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Biomass": 120}
	outputs = {"Solid Biofuel": 60}

class Steel_Ingot(Recipe):
	production_machine = PMs.Foundry
	inputs = {"Iron Ore": 45, "Coal": 45}
	outputs = {"Steel Ingot": 45}
class Coke_Steel_Ingot(Recipe):
	production_machine = PMs.Foundry
	inputs = {"Iron Ore": 75, "Petroleum Coke": 75}
	outputs = {"Steel Ingot": 100}
class Compacted_Steel_Ingot(Recipe):
	production_machine = PMs.Foundry
	inputs = {"Iron Ore": 5, "Compacted Coal": 2.5}
	outputs = {"Steel Ingot": 10}
class Solid_Steel_Ingot(Recipe):
	production_machine = PMs.Foundry
	inputs = {"Iron Ingot": 40, "coal": 40}
	outputs = {"Steel Ingot": 60}

class Steel_Beam(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Steel Ingot": 60}
	outputs = {"Steel Beam": 15}
class Alternate_Beam(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Aluminum Ingot": 22.5}
	outputs = {"Steel Beam": 22.5}
class Molded_Beam(Recipe):
	production_machine = PMs.Foundry
	inputs = {"Steel Ingot": 120, "Concrete": 80}
	outputs = {"Steel Beam": 45}

class Steel_Pipe(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Steel Ingot": 30}
	outputs = {"Steel Pipe": 20}
class Iron_Pipe(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Iron Ingot": 100}
	outputs = {"Steel Pipe": 25}
class Molded_Steel_Pipe(Recipe):
	production_machine = PMs.Foundry
	inputs = {"Steel Ingot": 50, "Concrete": 30}
	outputs = {"Steel Pipe": 50}

class Versatile_Framework(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Modular Frame": 2.5, "Steel Beam": 30}
	outputs = {"Versatile Framework": 5}
class Flexible_Framework(Recipe):
	production_machine = PMs.Manufacturer
	inputs = {"Modular Frame": 3.75, "Steel Beam": 22.5, "Rubber": 30}
	outputs = {"Versatile Framework": 7.5}

class Encased_Industrial_Beam(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Steel Beam": 18, "Concrete": 36}
	outputs = {"Encased Industrial Beam": 6}
class Encased_Industrial_Pipe(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Steel Pipe": 24, "Concrete": 20}
	outputs = {"Encased Industrial Beam": 4}

class Stator(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Steel Pipe": 15, "Wire": 40}
	outputs = {"Stator": 5}
class Quickwire_Stator(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Steel Pipe": 16, "Quickwire": 60}
	outputs = {"Stator": 8}

class Motor(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Rotor": 10, "Stator": 10}
	outputs = {"Motor": 5}
class Electric_Motor(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Electromagnetic Control Rod": 3.75, "Rotor": 7.5}
	outputs = {"Motor": 7.5}
class Rigor_Motor(Recipe):
	production_machine = PMs.Manufacturer
	inputs = {"Rotor": 3.75, "Stator": 3.75, "Crystal Oscillator": 1.25}
	outputs = {"Motor": 7.5}

class Automated_Wiring(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Stator": 2.5, "Cable": 50}
	outputs = {"Automated Wiring": 2.5}
class Automated_Speed_Wiring(Recipe):
	production_machine = PMs.Manufacturer
	inputs = {"Stator": 3.75, "Wire": 75, "High Spweed Connector": 1.875}
	outputs = {"Automated Wiring": 7.5}

class Plastic(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Crude Oil": 30}
	outputs = {"Plastic": 20, "Heavy Oil Residue": 10}
class Residual_Plastic(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Polymer Resin": 60, "Water": 20}
	outputs = {"Plastic": 20}
class Recycled_Plastic(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Rubber": 30, "Fuel": 30}
	outputs = {"Plastic": 60}

class Rubber(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Crude Oil": 30}
	outputs = {"Rubber": 20, "Heavy Oil Residue": 20}
class Residual_Rubber(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Polymer Resin": 40, "Water": 40}
	outputs = {"Rubber": 20}
class Recycled_Rubber(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Plastic": 30, "Fuel": 30}
	outputs = {"Rubber": 60}

class Fuel(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Crude Oil": 60}
	outputs = {"Fuel": 40, "Polymer Resin": 30}
class Residual_Fuel(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Heavy Oil Residue": 60}
	outputs = {"Fuel": 40}
class Unpackage_Fuel(Recipe):
	production_machine = PMs.Packager
	inputs = {"Packaged Fuel": 60}
	outputs = {"Fuel": 60, "Empty Canister": 60}
class Diluted_Fuel(Recipe):
	production_machine = PMs.Blender
	inputs = {"Heavy Oil Residue": 50, "Water": 100}
	outputs = {"Fuel": 100}

class Unpackage_Heavy_Oil_Residue(Recipe):
	production_machine = PMs.Packager
	inputs = {"Packaged Heavy Oil Residue": 20}
	outputs = {"Heavy Oil Residue": 20, "Empty Canister": 20}
class Heavy_Oil_Residue(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Crude Oil": 30}
	outputs = {"Heavy Oil Residue": 40, "Polymer Resin": 20}

class Polymer_Resin(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Crude Oil": 60}
	outputs = {"Polymer Resin": 130, "Heavy Oil Residue": 20}

class Petroleum_Coke(Recipe):
	production_machine = PMs.Refinery
	inputs = {"Heavy Oil Residue": 40}
	outputs = {"Petroleum Coke": 120}

class Circuit_Board(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Copper Sheet": 15, "Plastic": 30}
	outputs = {"Circuit Board": 7.5}
class Caterium_Circuit_Board(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Plastic": 12.5, "Quickwire": 37.5}
	outputs = {"Circuit Board": 8.75}
class Electrode_Circuit_Board(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Rubber": 20, "Petroleum Coke": 40}
	outputs = {"Circuit Board": 5}
class Silicon_Circuit_Board(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Copper Sheet": 27.5, "Silica": 27.5}
	outputs = {"Circuit Board": 12.5}

class Empty_Canister(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Plastic": 30}
	outputs = {"Empty Canister": 60}
class Coated_Iron_Canister(Recipe):
	production_machine = PMs.Assembler
	inputs = {"Iron Plate": 30, "Copper Sheet": 15}
	outputs = {"Empty Canister": 60}
class Steel_Canister(Recipe):
	production_machine = PMs.Constructor
	inputs = {"Steel Ingot": 40}
	outputs = {"Empty Canister": 40}




#-----Incomplete-----#

class Aluminum_Scrap(Recipe):
	production_machine = None #Refinery
	inputs = {"Alumina Solution": 240, "Coal": 120}
	outputs = {"Aluminum Scrap": 360, "Water": 120}

class Battery(Recipe):
	production_machine = None #Blender
	inputs = {"Sulfuric Acid": 50, "Alumina Solution": 40, "Aluminum Casing": 20}
	outputs = {"Battery": 20, "Water": 30}

class Non_Fissile_Uranium(Recipe):
	production_machine = None #Blender
	inputs = {"Uranium Waste": 37.5, "Silica": 25, "Nitric Acid": 15, "Sulfuric Acid": 15}
	outputs = {"Non-Fissile Uranium": 50, "Water": 15}

class Distilled_Silica(Recipe):
	production_machine = None #Blender
	inputs = {"Dissolved Silica": 120, "Limestone": 50, "Water": 100}
	outputs = {"Silica": 270, "Water": 80}

class Electrode_Aluminum_Scrap(Recipe):
	production_machine = None #Refinery
	inputs = {"Alumina Solution": 180, "Petroleum Coke": 60}
	outputs = {"Aluminum Scrap": 300, "Water": 105}

class Fertile_Uranium(Recipe):
	production_machine = None #Blender
	inputs = {"Uranium Ore": 25, "Uranium Waste": 25, "Nitric Acid": 15, "Sulfuric Acid": 25}
	outputs = {"Non-Fissile Uranium": 100, "Water": 40}

class Instant_Scrap(Recipe):
	production_machine = None #Blender
	inputs = {"Bauxite": 150, "Coal": 100, "Sulfuric Acid": 50, "Water": 60}
	outputs = {"Aluminum Scrap": 300, "Water": 50}