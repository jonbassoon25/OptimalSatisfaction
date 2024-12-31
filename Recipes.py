#Imports
import Production_Machines as PMs

class Recipe:
	production_machine = PMs.Production_Machine
	inputs = {}
	outputs = {}

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
class Limestone_SAM_S:
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