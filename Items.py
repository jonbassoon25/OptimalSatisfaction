#Imports
import sys, inspect

import Recipes

class Item:
	name = "Undefined Item"
	default_recipes = []
	alternate_recipes = []
	sink_yield = None



#Raw Resources
class Iron_Ore(Item):
	name = "Iron Ore"
	default_recipes = [Recipes.Iron_Ore_MK1, Recipes.Iron_Ore_MK2, Recipes.Iron_Ore_MK3] #Recipes.Iron_Ore_SAM_L
	sink_yield = 1

class Copper_Ore(Item):
	name = "Copper Ore"
	default_recipes = [Recipes.Copper_Ore_MK1, Recipes.Copper_Ore_MK2, Recipes.Copper_Ore_MK3] #Recipes.Copper_Ore_SAM_Q, Recipes.Copper_Ore_SAM_S
	sink_yield = 3

class Limestone(Item):
	name = "Limestone"
	default_recipes = [Recipes.Limestone_MK1, Recipes.Limestone_MK2, Recipes.Limestone_MK3] #Recipes.Limestone_SAM_S
	sink_yield = 2

class Coal(Item):
	name = "Coal"
	default_recipes = [Recipes.Coal_MK1, Recipes.Coal_MK2, Recipes.Coal_MK3] #Recipes.Coal_SAM_I, Recipes.Coal_SAM_L
	alternate_recipes = [Recipes.Biocoal, Recipes.Charcoal]
	sink_yield = 3

class Quartz(Item):
	name = "Raw Quartz"
	default_recipes = [Recipes.Quartz_MK1, Recipes.Quartz_MK2, Recipes.Quartz_MK3] #Recipes.Quartz_SAM_B, Recipes.Quartz_SAM_O
	sink_yield = 15

class Caterium_Ore(Item):
	name = "Caterium Ore"
	default_recipes = [Recipes.Caterium_Ore_MK1, Recipes.Caterium_Ore_MK2, Recipes.Caterium_Ore_MK3] #Recipes.Caterium_Ore_SAM_C, Recipes.Caterium_Ore_SAM_Q
	sink_yield = 7

class Sulfer(Item):
	name = "Sulfer"
	default_recipes = [Recipes.Sulfer_MK1, Recipes.Sulfer_MK2, Recipes.Sulfer_MK3] #Recipes.Sulfer_SAM_O, Recipes.Sulfer_SAM_I
	sink_yield = 11

class Bauxite(Item):
	name = "Bauxite"
	default_recipes = [Recipes.Bauxite_MK1, Recipes.Bauxite_MK2, Recipes.Bauxite_MK3] #Recipes.Bauxite_SAM_G, Recipes.Bauxite_SAM_C
	sink_yield = 8

class Uranium_Ore(Item):
	name = "Uranium Ore"
	default_recipes = [Recipes.Uranium_Ore_MK1, Recipes.Uranium_Ore_MK2] #Recipes.Uranium_Ore_MK3, Recipes.Uranium_Ore_SAM_B
	sink_yield = 35

class SAM(Item):
	name = "SAM"
	default_recipes = [Recipes.SAM_MK1, Recipes.SAM_MK2, Recipes.SAM_MK3]
	sink_yield = 20

class Crude_Oil(Item):
	name = "Crude Oil"
	default_recipes = [Recipes.Crude_Oil, Recipes.Crude_Oil_Well, Recipes.Unpackage_Oil]

class Nitrogen_Gas(Item):
	name = "Nitrogen Gas"
	default_recipes = [Recipes.Nitrogen_Gas, Recipes.Unpackage_Nitrogen_Gas, Recipes.Nitrogen_Gas_SAM_B, Recipes.Nitrogen_Gas_SAM_C]

class Water(Item):
	name = "Water"
	default_recipes = [Recipes.Water, Recipes.Unpackage_Water, Recipes.Aluminum_Scrap, Recipes.Battery, Recipes.Non_Fissile_Uranium]
	alternate_recipes = [Recipes.Distilled_Silica, Recipes.Electrode_Aluminum_Scrap, Recipes.Fertile_Uranium, Recipes.Instant_Scrap]



#Player-Collected Biomass
class Alien_Remains(Item):
	name = "Alien Remains"

class Leaves(Item):
	name = "Leaves"
	sink_yield = 3

class Wood(Item):
	name = "Wood"
	sink_yield = 30

class Mycelia(Item):
	name = "Mycelia"
	sink_yield = 10



#Player Crafted Items (that are used in construction / production)
class Portable_Miner(Item):
	name = "Portable Miner"
	default_recipes = []
	alternate_recipes = [Recipes.Portable_Miner]
	sink_yield = 56



#Tier 0 & 1 & 2 Items
class Iron_Ingot(Item):
	name = "Iron Ingot"
	default_recipes = [Recipes.Iron_Ingot]
	alternate_recipes = [Recipes.Basic_Iron_Ingot, Recipes.Iron_Alloy_Ingot, Recipes.Leached_Iron_Ingot, Recipes.Pure_Iron_Ingot]
	sink_yield = 2

class Iron_Plate(Item):
	name = "Iron Plate"
	default_recipes = [Recipes.Iron_Plate]
	alternate_recipes = [Recipes.Coated_Iron_Plate, Recipes.Steel_Cast_Plate]
	sink_yield = 6

class Iron_Rod(Item):
	name = "Iron Rod"
	default_recipes = [Recipes.Iron_Rod]
	alternate_recipes = [Recipes.Aluminum_Rod, Recipes.Steel_Rod]
	sink_yield = 4

class Copper_Ingot(Item):
	name = "Copper Ingot"
	default_recipes = [Recipes.Copper_Ingot]
	alternate_recipes = [Recipes.Copper_Alloy_Ingot, Recipes.Leached_Copper_Ingot, Recipes.Pure_Copper_Ingot, Recipes.Tempered_Copper_Ingot]
	sink_yield = 6

class Wire(Item):
	name = "Wire"
	default_recipes = [Recipes.Wire]
	alternate_recipes = [Recipes.Caterium_Wire, Recipes.Fused_Wire, Recipes.Iron_Wire]
	sink_yield = 6

class Cable(Item):
	name = "Cable"
	default_recipes = [Recipes.Cable]
	alternate_recipes = [Recipes.Coated_Cable, Recipes.Insulated_Cable, Recipes.Quickwire_Cable]
	sink_yield = 24

class Concrete(Item):
	name = "Concrete"
	default_recipes = [Recipes.Concrete]
	alternate_recipes = [Recipes.Fine_Concrete, Recipes.Rubber_Concrete, Recipes.Wet_Concrete]
	sink_yield = 12

class Screw(Item):
	name = "Screw"
	default_recipes = [Recipes.Screw]
	alternate_recipes = [Recipes.Cast_Screw, Recipes.Steel_Screw]
	sink_yield = 2

class Reinforced_Iron_Plate(Item):
	name = "Reinforced Iron Plate"
	default_recipes = [Recipes.Reinforced_Iron_Plate]
	alternate_recipes = [Recipes.Adhered_Iron_Plate, Recipes.Bolted_Iron_Plate, Recipes.Stitched_Iron_Plate]
	sink_yield = 120

class Biomass(Item):
	name = "Biomass"
	default_recipes = [Recipes.Biomass_A, Recipes.Biomass_L, Recipes.Biomass_M, Recipes.Biomass_W]
	alternate_recipes = []
	sink_yield = 12

class Copper_Sheet(Item):
	name = "Copper Sheet"
	default_recipes = [Recipes.Copper_Sheet]
	alternate_recipes = [Recipes.Steamed_Copper_Sheet]
	sink_yield = 24

class Rotor(Item):
	name = "Rotor"
	default_recipes = [Recipes.Rotor]
	alternate_recipes = [Recipes.Copper_Rotor, Recipes.Steel_Rotor]
	sink_yield = 140

class Modular_Frame(Item):
	name = "Modular Frame"
	default_recipes = [Recipes.Modular_Frame]
	alternate_recipes = [Recipes.Bolted_Frame, Recipes.Steeled_Frame]
	sink_yield = 408

class Smart_Plating(Item):
	name = "Smart Plating"
	default_recipes = [Recipes.Smart_Plating]
	alternate_recipes = [Recipes.Plastic_Smart_Plating]
	sink_yield = 520

class Solid_Biofuel(Item):
	name = "Solid Biofuel"
	default_recipes = [Recipes.Solid_Biofuel]
	sink_yield = 48



#Tier 3 & 4 Items
class Steel_Ingot(Item):
	name = "Steel Ingot"
	default_recipes = [Recipes.Steel_Ingot]
	alternate_recipes = [Recipes.Coke_Steel_Ingot, Recipes.Compacted_Steel_Ingot, Recipes.Solid_Steel_Ingot]
	sink_yield = 8

class Steel_Beam(Item):
	name = "Steel Beam"
	default_recipes = [Recipes.Steel_Beam]
	alternate_recipes = [Recipes.Alternate_Beam, Recipes.Molded_Beam]
	sink_yield = 64

class Steel_Pipe(Item):
	name = "Steel Pipe"
	default_recipes = [Recipes.Steel_Pipe]
	alternate_recipes = [Recipes.Iron_Pipe, Recipes.Molded_Steel_Pipe]
	sink_yield = 24

class Versatile_Framework(Item):
	name = "Versatile Framework"
	default_recipes = [Recipes.Versatile_Framework]
	alternate_recipes = [Recipes.Flexible_Framework]
	sink_yield = 1176

class Encased_Industrial_Beam(Item):
	name  = "Encased Industrial Beam"
	default_recipes = [Recipes.Encased_Industrial_Beam]
	alternate_recipes = [Recipes.Encased_Industrial_Pipe]
	sink_yield = 528

class Stator(Item):
	name = "Stator"
	default_recipes = [Recipes.Stator]
	alternate_recipes = [Recipes.Quickwire_Stator]
	sink_yield = 240

class Motor(Item):
	name = "Motor"
	default_recipes = [Recipes.Motor]
	alternate_recipes = [Recipes.Electric_Motor, Recipes.Rigor_Motor]
	sink_yield = 1520

class Automated_Wiring(Item):
	name = "Automated Wiring"
	default_recipes = [Recipes.Automated_Wiring]
	alternate_recipes = [Recipes.Automated_Speed_Wiring]
	sink_yield = 1440

class Plastic(Item):
	name = "Plastic"
	default_recipes = [Recipes.Plastic, Recipes.Residual_Plastic]
	alternate_recipes = [Recipes.Recycled_Plastic]
	sink_yield = 75

class Rubber(Item):
	name = "Rubber"
	default_recipes = [Recipes.Rubber, Recipes.Residual_Rubber]
	alternate_recipes = [Recipes.Recycled_Rubber]
	sink_yield = 60

class Fuel(Item):
	name = "Fuel"
	default_recipes = [Recipes.Fuel, Recipes.Residual_Fuel, Recipes.Unpackage_Fuel]
	alternate_recipes = [Recipes.Diluted_Fuel]

class Heavy_Oil_Residue(Item):
	name = "Heavy Oil Residue"
	default_recipes = [Recipes.Unpackage_Heavy_Oil_Residue, Recipes.Plastic, Recipes.Rubber]
	alternate_recipes = [Recipes.Heavy_Oil_Residue, Recipes.Polymer_Resin]

class Polymer_Resin(Item):
	name = "Polymer Resin"
	default_recipes = [Recipes.Fuel]
	alternate_recipes = [Recipes.Heavy_Oil_Residue, Recipes.Polymer_Resin]
	sink_yield = 12

class Petroleum_Coke(Item):
	name = "Petroleum Coke"
	default_recipes = [Recipes.Petroleum_Coke]
	sink_yield = 20

class Circuit_Board(Item):
	name = "Circuit Board"
	default_recipes = [Recipes.Circuit_Board]
	alternate_recipes = [Recipes.Caterium_Circuit_Board, Recipes.Electrode_Circuit_Board, Recipes.Silicon_Circuit_Board]
	sink_yield = 696

class Empty_Canister(Item):
	name = "Empty Canister"
	default_recipes = []
	alternate_recipes = []
	sink_yield = 60

class Reanimated_Sam(Item): #Not complete
	name = "Reanimated SAM"

resources = [ret[1] for ret in inspect.getmembers(sys.modules[__name__], inspect.isclass)] #Get list of all resource classes
#remove non-lookup classes
resources.remove(Item)

nautral_resources = []
for resource in resources:
	if resource.default_recipes == [] and resource.alternate_recipes == []:
		nautral_resources.append(resource)

semi_nautral_resources = []
for resource in resources:
	if resource.default_recipes == [] and resource.alternate_recipes != []:
		semi_nautral_resources.append(resource)

synthetic_resources = []
for resource in resources:
	if resource.default_recipes != []:
		synthetic_resources.append(resource)

def get_item_by_name(item_name):
	for item in resources:
		if item.name == item_name:
			return item
	raise Exception(f"{item_name} is not an Item.")