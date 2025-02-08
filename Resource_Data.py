import joblib
import json
import numpy as np

class Resource_Data:
	resource_ratios = {}
	resource_commonality_table = [] #keys of resource ratios

	@classmethod
	def load_data_from_pack(cls, save_pack):
		cls.resource_ratios = save_pack["resource ratios"]
		cls.resource_commonality_table = save_pack["commonality table"]

	@classmethod
	def compile_resource_files(cls):
		node_data = {}
		well_data = {}

		with open("./Resource_Data_Files/resource_node_data.json") as node_data_file:
			node_data = json.load(node_data_file)
		with open("./Resource_Data_Files/resource_well_data.json") as well_data_file:
			well_data = json.load(well_data_file)

		resource_ratios = {}
		
		#assign special resource ratios
		resource_ratios["Water"] = 0 #free
		
		#compile resource ratios
		for key in node_data.keys():
			special_mult = 1
			if key == "Crude Oil":
				special_mult = 5

			resource_commonality_weight = special_mult * (node_data[key]["Impure"] + node_data[key]["Normal"] * 2 + node_data[key]["Pure"] * 4)

			if key in well_data:
				resource_commonality_weight += node_data[key]["Impure"] + node_data[key]["Normal"] * 2 + node_data[key]["Pure"] * 4

			resource_ratios[key] = 1 / resource_commonality_weight
		
		#assign well data ratios that weren't caught with the resource ratio assignements above
		for key in well_data.keys():
			if not key in node_data.keys():
				resource_commonality_weight = well_data[key]["Impure"] + well_data[key]["Normal"] * 2 + well_data[key]["Pure"] * 4
				resource_ratios[key] = 1 / resource_commonality_weight

		#build the commonality table (most common to least common) and assign ordered resource ratios
		rct = [] #resource commonality table
		resource_ratio_key_list = list(resource_ratios.keys())
		for i in range(len(resource_ratio_key_list)):
			key_of_smallest = resource_ratio_key_list[i]
			for j in range(len(resource_ratio_key_list)):
				if resource_ratio_key_list[j] in rct:
					continue
				cur_val = resource_ratios[resource_ratio_key_list[j]]
				if cur_val < resource_ratios[key_of_smallest]:
					key_of_smallest = resource_ratio_key_list[j]
			rct.append(key_of_smallest)
			Resource_Data.resource_ratios[key_of_smallest] = resource_ratios[key_of_smallest]
		
		#set the commonality table
		Resource_Data.resource_commonality_table = np.array(rct)

		#save files
		joblib.dump({"resource ratios": Resource_Data.resource_ratios, "commonality table": Resource_Data.resource_commonality_table}, "./Resource_Data_Files/data.pkl")
		print("Resource data successfully compiled")


if __name__ == "__main__":
	#compile resource data
	Resource_Data.compile_resource_files()

	#save resource files as plaintext for viewing
	with open("./Resource_Data_Files/resource_ratios.txt", "w") as rr_file:
		rr_file.write('\n'.join([f"{key}: {Resource_Data.resource_ratios[key]}" for key in Resource_Data.resource_ratios]))
	with open("./Resource_Data_Files/resource_commonality_table.txt", "w") as rc_file:
		rc_file.write('\n'.join(Resource_Data.resource_commonality_table))
	print("Resource data view-files generated in ./Resource_Data_Files")
else:
	#load resource data
	try:
		save_pack = joblib.load("./Resource_Data_Files/data.pkl")
		Resource_Data.load_data_from_pack(save_pack)
	except FileNotFoundError:
		Resource_Data.compile_resource_files()