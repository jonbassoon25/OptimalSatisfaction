from tkinter import *
from tkinter import ttk

import Items
import Setup_Generator


class Optimal_Satisfaction_UI:
	def __init__(self):
		self.root = Tk()
		
		root = self.root
		root.title("Optimal Satisfaction")
		root.resizable(False, False)

		mainframe = ttk.Frame(root, padding="10 10")
		mainframe.grid(column=0, row=0)
		
		ttk.Label(mainframe, text="Output Item:").grid(column=0, row=0, sticky="W")

		self.output_str = StringVar()
		output_combo = ttk.Combobox(mainframe, textvariable=self.output_str)
		output_combo['values'] = tuple([resource.name for resource in Items.synthetic_resources + Items.semi_nautral_resources])
		output_combo.state(["readonly"])
		output_combo.grid(column=0, row=1, sticky="W", columnspan=2)

		ttk.Label(mainframe, text="Production rate (items/min): ").grid(column=0, row=3, sticky="W", columnspan=2)

		self.production_rate_str = StringVar(value="0")
		production_rate_inputbox = ttk.Entry(mainframe, textvariable=self.production_rate_str, width=8)
		production_rate_inputbox.bind("<FocusOut>", lambda _: self.finalize_production_rate_input())
		self.production_rate_str.trace_add("write", lambda *_: self.validate_production_rate_input())
		production_rate_inputbox.grid(column=1, row=3, sticky="E")

		ttk.Label(mainframe).grid(column=0, row=5, columnspan=2)

		ttk.Label(mainframe, text="Miner Tier:").grid(column=0, row=6, sticky="W")

		self.miner_tier = StringVar(value="mk1")
		miner_mk1 = ttk.Radiobutton(mainframe, text="MK 1", variable=self.miner_tier, value="mk1")
		miner_mk2 = ttk.Radiobutton(mainframe, text="MK 2", variable=self.miner_tier, value="mk2")
		miner_mk3 = ttk.Radiobutton(mainframe, text="MK 3", variable=self.miner_tier, value="mk3")
		miner_mk1.grid(column=0, row=7, sticky="W", padx=15)
		miner_mk2.grid(column=0, row=8, sticky="W", padx=15)
		miner_mk3.grid(column=0, row=9, sticky="W", padx=15)
		
		ttk.Label(mainframe, text="Recipe Type:").grid(column=1, row=6, sticky="W")

		self.recipe_type = StringVar(value="default")
		default_recipe = ttk.Radiobutton(mainframe, text="Default Recipes Only", variable=self.recipe_type, value="default")
		all_recipe = ttk.Radiobutton(mainframe, text="All Recipes", variable=self.recipe_type, value="all")
		default_recipe.grid(column=1, row=7, sticky="W", padx=15)
		all_recipe.grid(column=1, row=8, sticky="W", padx=15)

		self.input_resources = []
		input_resource_display = Display_Box(mainframe, root, text="Input Resources", content=self.input_resources)
		input_resource_display.grid(column=3, row=1, columnspan=2, padx=5, sticky="NW")

		self.resource_limits = [["SAM", 0]]
		resource_limit_display = Display_Box(mainframe, root, text="Resource Limits", content=self.resource_limits, allow_zero=True)
		resource_limit_display.grid(column=5, row=1, padx=5, columnspan=2, sticky="NW")

		self.construction_limits = []
		construction_limit_display = Display_Box(mainframe, root, text="Construction Limits", content=self.construction_limits, allow_zero=True)
		construction_limit_display.grid(column=7, row=1, columnspan=2, padx=5, sticky="NW")

		
		calculate = Button(mainframe, text="Calculate Paths", command=lambda:Production_Paths_Window(self, root, self._generate_production_tree()))
		calculate.grid(column=0, row=10, columnspan=2)


		#ds = Drag_Sort(root, ["Hello", "World", "test", "test", "test"])
		#ds.grid(column=0, row=5)

	def _generate_production_tree(self):
		if int(self.production_rate_str.get()) == 0 or self.output_str.get() == "":
			return None
		print(f"Generating production tree for {self.output_str.get()} with values:\n\tproduction rate: {int(self.production_rate_str.get())}\n\tminer level: {self.miner_tier.get()}\n\trecipe type: {self.recipe_type.get()}")
		if self.miner_tier.get() == "mk1":
			miner_tier = 1
		elif self.miner_tier.get() == "mk2":
			miner_tier = 2
		elif self.miner_tier.get() == "mk3":
			miner_tier = 3
		else:
			raise Exception(f"Unrecognized miner tier from self.miner_tier: {self.miner_tier.get}")
		return Setup_Generator.generate_production_tree(self.output_str.get(), int(self.production_rate_str.get()), miner_tier, default_only=self.recipe_type.get() == "default")
	

	def mainloop(self):
		self.root.mainloop()


	def calculate_production_rate(self):
		'''Calculates production rate from inputs and updates production rate input box to match the calculated value'''
		print("Calc production rate")
	

	def validate_production_rate_input(self):
		pri = list(self.production_rate_str.get())
		for char in pri:
			try:
				int(char)
			except:
				pri.remove(char)

		self.production_rate_str.set(''.join(pri))
	
	def finalize_production_rate_input(self):
		self.validate_production_rate_input()
		if self.production_rate_str.get() == "":
			self.production_rate_str.set("0")
		else:
			self.production_rate_str.set(str(int(self.production_rate_str.get())))


class Item_Selection_Window:
	def __init__(self, root, display_box):
		self.display_box = display_box

		self.root = Toplevel(root)
		root = self.root

		root.title("Item Selection")
		root.resizable(False, False)

		mainframe = ttk.Frame(root, padding="10 10")
		mainframe.grid(column=0, row=0)

		self.item_list = [resource.name for resource in Items.resources]
		self.items = StringVar(value=self.item_list)
		self.item_listbox = Listbox(mainframe, height=20, listvariable=self.items)
		self.item_listbox.grid(column=0, row=1, padx=15, rowspan=18)

		ttk.Label(mainframe, text="Production rate (items/min): ").grid(column=1, row=17, sticky="E")

		self.production_rate_str = StringVar(value="0")
		production_rate_inputbox = ttk.Entry(mainframe, textvariable=self.production_rate_str, width=6)
		production_rate_inputbox.bind("<FocusOut>", lambda _: self.finalize_production_rate_input())
		self.production_rate_str.trace_add("write", lambda *_: self.validate_production_rate_input())
		production_rate_inputbox.grid(column=2, row=17, sticky="W")

		add = Button(mainframe, text="Add", command=self.add)
		add.grid(column=1, row=18, sticky="N", columnspan=2)


	def validate_production_rate_input(self):
		pri = list(self.production_rate_str.get())
		for char in pri:
			try:
				int(char)
			except:
				pri.remove(char)

		self.production_rate_str.set(''.join(pri))
	
	def finalize_production_rate_input(self):
		self.validate_production_rate_input()
		if self.production_rate_str.get() == "":
			self.production_rate_str.set("0")
		else:
			self.production_rate_str.set(str(int(self.production_rate_str.get())))

	def add(self):
		#self.listvariable.set((self.listvariable.get() + "".join([" " + Items.get_item_by_name(self.item_list[i]).__name__ for i in self.item_listbox.curselection()])).strip())
		if len(self.item_listbox.curselection()) == 0:
			return
		self.display_box.add_content([[self.item_list[self.item_listbox.curselection()[0]], int(self.production_rate_str.get())]])
		self.display_box.validate_display_values()
		self.destroy()
	
	def destroy(self):
		self.root.destroy()
	
class Item_Deletion_Window:
	def __init__(self, root, display_box):
		self.display_box = display_box

		self.root = Toplevel(root)
		root = self.root

		root.title("Item Deletion")
		root.resizable(False, False)

		mainframe = ttk.Frame(root, padding="10 10")
		mainframe.grid(column=0, row=0)

		self.selection_listbox = Listbox(mainframe, height=7, listvariable=StringVar(value=[item[0] for item in self.display_box.get_content()]))
		self.selection_listbox.grid(column=0,row=0)

		remove = Button(mainframe, text="Remove", command=self.remove)
		remove.grid(column=0, row=1)

	def remove(self):
		if len(self.selection_listbox.curselection()) == 0:
			return
		content = self.display_box.get_content()
		del content[self.selection_listbox.curselection()[0]]
		self.display_box.set_content(content)
		self.destroy()

	def destroy(self):
		self.root.destroy()


class Display_Box(Frame):
	def __init__(self, master, root, text="Display Box", content=[], allow_zero=False):
		'''
		Parameters:
			master: master
			content (list): content. format: [["item name", quantity], ...]
		'''
		super().__init__(master)
		self.root = root
		self["borderwidth"] = 2
		self["relief"] = "groove"
		self.content = content
		self.allow_zero = allow_zero
		Label(self, text=f"{text}:    ").grid(column=0, row=0, columnspan=2, sticky="W")

		self.labels = []
		self.set_content(content)

		remove_button = Button(self, text="Remove Item", command=lambda: Item_Deletion_Window(self.root, self))
		remove_button.grid(column=0, row=255)

		add_button = Button(self, text="Add Item", command=lambda: Item_Selection_Window(self.root, self))
		add_button.grid(column=1, row=255)


	def get_content(self):
		return self.content[:]
	
	def set_content(self, content):
		content = content[:] #if content == self.content, it should be seperated on at least the surface level
		self.content.clear()
		for label in self.labels:
			label.destroy()
		self.labels = []

		self.add_content(content)
	
	def add_content(self, content):
		for thing in content:
			self.labels.append(Label(self, text=f"{thing[0]}: {thing[1]} / min"))
			self.labels[-1].grid(column=0, row=len(self.labels), padx=7, pady=1, sticky="W", columnspan=2)
		self.content += content
	
	def validate_display_values(self):
		for thing in self.content:
			if thing[1] == 0 and not self.allow_zero:
				self.content.remove(thing)
		self.set_content(self.content)


class Drag_Sort(Canvas):
	def __init__(self, master, options, x_scale = 1, y_scale = 1, orient = VERTICAL):
		width = x_scale * 100
		height = y_scale * 20

		if orient == VERTICAL:
			height *= len(options)
		elif orient == HORIZONTAL:
			width *= len(options)
		else:
			raise Exception(f"Orient not recognized: {orient.__name__}")

		super().__init__(master, width=width, height=height)
		self.orient = orient

		self.selected_item = None
		self.dy = 0
		

		self.bind("<Enter>", lambda event: self.enter_canvas(event))
		self.bind("<Leave>", lambda event: self.exit_canvas(event))
		
		self.bind("<Button>", self.on_canvas_pressed)
		self.bind("<ButtonRelease>", self.on_canvas_released)

		items = [Label(self, text=item_name) for item_name in options]
		self.dragable_block_ids = []
		
		
		for i in range(len(items)):
			item = items[i]

			if orient == VERTICAL:
				id = self.create_window(width/2, (i + 0.5) * height/len(options), width=width, height=height/len(options), window=item, tags=("dragable_block"))
			else:
				id = self.create_window((i + 0.5) * width/len(options), height/2, width=width/len(options), height=height, window=item, tags=("dragable_block"))

			self.dragable_block_ids.append(id)
			

	def on_canvas_pressed(self, event):
		print("canvas was pressed")
		#self.selected_item = item
		self.dy = event.y #- item.y
	
	def on_canvas_released(self, event):
		print("canvas was released")

	def enter_canvas(self, event):
		print("entered canvas area")
		if self.selected_item == None:
			return
		target_y = event.y - self.dy
		cur_y = 0

	def exit_canvas(self, event):
		print("exited canvas area")
		if self.selected_item == None:
			return
		self.selected_item = None


class Production_Paths_Window:
	def __init__(self, main_window, root, production_tree):
		if production_tree == None:
			return
		
		self.root = Toplevel(root)
		root = self.root

		self.production_tree = production_tree
		print("Saving Production Tree...")

		with open("text.txt", "w") as dumpFile:
			dumpFile.write(str(self.production_tree))

		print("Splitting tree...")
		self.production_paths = Setup_Generator.split_production_tree(production_tree)
		print("Filtering tree...")
		self.production_paths = Setup_Generator.filter_production_paths(self.production_paths, main_window.output_str.get(), int(main_window.production_rate_str.get()))
		print("Sorting tree...")
		self.production_paths = Setup_Generator.sort_production_paths(self.production_paths, main_window.output_str.get(), ["resource efficiency", "input resources", "byproducts", "electrical consumption", "construction cost"], {})
		print("Getting simple paths...")
		self.simple_production_paths = Setup_Generator.get_simple_production_paths(self.production_paths)

		root.title("Production Paths")
		root.resizable(False, False)

		mainframe = ttk.Frame(root, padding="10 10")
		mainframe.grid(column=0, row=0)

		Label(mainframe, text="Production Paths:").grid(column=0, row=0, sticky="W")
		
		#listbox of simple production paths
		simple_production_paths_text = []
		for path in self.simple_production_paths:
			simple_production_paths_text.append(f"{path['name']} - {', '.join([key + ': ' + str(round(path['inputs'][key], 2)) + '/min' for key in path['inputs'].keys()])} --> {', '.join([key + ': ' + str(round(path['outputs'][key], 2)) + '/min' for key in path['outputs'].keys()])}")
		production_path_listbox = Listbox(mainframe, width=80, height=10, listvariable=StringVar(value=simple_production_paths_text))
		production_path_listbox.grid(column=0, row=1)
		production_path_listbox.bind("<Double-1>", lambda _: Production_Path_Window(self.root, self.simple_production_paths[production_path_listbox.curselection()[0]], self.production_paths[production_path_listbox.curselection()[0]]))


class Production_Path_Window:
	def __init__(self, root, simple_production_path, production_path):
		self.root = Toplevel(root)
		root = self.root

		root.title(simple_production_path["name"])
		root.resizable(False, False)

		mainframe = ttk.Frame(root, padding="10 10")
		mainframe.grid(column=0, row=0)

		Label(mainframe, text=f"Maximum Energy Consumption: {round(Setup_Generator.get_max_energy_use(production_path), 2)} MW").grid(column=0, row=2, columnspan=2, sticky="W")

		construction_requirments_frame = Frame(mainframe)
		construction_requirments_frame.grid(column=0, row=3, padx=10, pady=10, rowspan=3, sticky="NW")
		construction_requirments_frame["borderwidth"] = 2
		construction_requirments_frame["relief"] = "groove"

		Label(construction_requirments_frame, text="Construction Requirements: ").grid(column=0, row=0, sticky="W")
		construction_requirments = Setup_Generator.get_construction_requirements(production_path)
		for i in range(len(construction_requirments.keys())):
			key = list(construction_requirments.keys())[i]
			Label(construction_requirments_frame, text=f"{key}: {round(construction_requirments[key], 4)}").grid(column=0, row=i+1, padx=10, sticky="W")

		input_frame = Frame(mainframe)
		input_frame.grid(column=1, row=3, padx=10, pady=10, sticky="NW")
		input_frame["borderwidth"] = 2
		input_frame["relief"] = "groove"

		Label(input_frame, text="Inputs:").grid(column=0, row=0, sticky="W")
		for i in range(len(simple_production_path["inputs"].keys())):
			key = list(simple_production_path["inputs"].keys())[i]
			Label(input_frame, text=f"{key}: {round(simple_production_path['inputs'][key], 4)}").grid(column=0, row=i+1, padx=10, sticky="W")


		output_frame = Frame(mainframe)
		output_frame.grid(column=1, row=4, padx=10, pady=10, sticky="NW")
		output_frame["borderwidth"] = 2
		output_frame["relief"] = "groove"

		Label(output_frame, text="Outputs:").grid(column=0, row=0, sticky="W")
		for i in range(len(simple_production_path["outputs"].keys())):
			key = list(simple_production_path["outputs"].keys())[i]
			Label(output_frame, text=f"{key}: {round(simple_production_path['outputs'][key], 4)}").grid(column=0, row=i+1, padx=10, sticky="W")

		view_path_tree_button = Button(mainframe, text="View Production Tree", command=lambda:Production_Path_Tree_Window(self.root, simple_production_path, production_path))
		view_path_tree_button.grid(column=1, row=5, sticky="N")

class Production_Path_Tree_Window:
	def __init__(self, root, simple_production_path, production_path):
		self.root = Toplevel(root, width=600, height=600)
		root = self.root

		self.production_path = production_path

		root.title(f"Production Tree for {simple_production_path['name']}")
		root.resizable(False, False)

		mainframe = ttk.Frame(root, padding="10 10")
		mainframe.grid(column=0, row=0)

		Label(mainframe, text="Production Path Tree").grid(column=0, row=0)

		#s = StringVar(value=Setup_Generator.get_production_recipes(production_path))
		#Listbox(mainframe, height=40, width=80, listvariable=s).grid(column=0, row=1)

		self.ppt_plan = self.get_ppt_plan()

		self.recipe_box_width = 200
		self.recipe_box_height = 75
		self.recipe_box_padding = (75, 50)
		self.text_height = 20

		self.tree_canvas = Canvas(mainframe, background="#232323",
								  width = self.recipe_box_padding[0]/2 + max(*self.ppt_plan[1]) * (self.recipe_box_width + self.recipe_box_padding[0]) - self.recipe_box_padding[0]/2, 
								  height = self.recipe_box_padding[1]/2 + len(self.ppt_plan[1]) * (self.recipe_box_height + self.recipe_box_padding[1]) - self.recipe_box_padding[1]/2
								)
		self.tree_canvas.grid(column=0, row=1)

		#debug print
		for row in self.ppt_plan[0]:
			print(row)
		
		self._draw_ppt()


	def _draw_ppt(self):
		ppt_rows = self.ppt_plan[0]
		ppt_dimensions = self.ppt_plan[1]

		#Draw base structure
		for i in range(len(ppt_dimensions)):
			cur_row = ppt_rows[i]
			for j in range(ppt_dimensions[i]):
				pos = (
					  self.recipe_box_padding[0]/2 + (self.recipe_box_width + self.recipe_box_padding[0]) * ((max(*self.ppt_plan[1]) - ppt_dimensions[i]) / 2 + j),
					  self.recipe_box_padding[1]/2 + (self.recipe_box_height + self.recipe_box_padding[1]) * i
					)
				self.tree_canvas.create_rectangle(pos[0], pos[1], pos[0] + self.recipe_box_width, pos[1] + self.recipe_box_height, fill="#808080", outline="#CFECF7")
				
				cur_recipe = cur_row[j]

				description = (
					cur_recipe.__class__.__name__.replace("_", " ") + "\n" + "\n" +
					cur_recipe.production_machine.__class__.__name__.replace("_", " ") + ": " + str(cur_recipe.production_machine.num_machines) + "\n" +
					"at clock speed of " + str(round(cur_recipe.production_machine.clock_speed * 100, 3)) + "%"
				)

				self.tree_canvas.create_text(pos[0] + 5, pos[1] + 5, text=description, anchor="nw", font="monospace", fill="#000000")
		
		#Fill in connecting lines
		for i in range(len(ppt_dimensions) - 1): #for each row
			cur_row = ppt_rows[i]
			draw_index = 0
			for j in range(ppt_dimensions[i]): #for each recipe in the row
				#draw connecting lines to this recipe's input recipes
				#input length can be found with the length of the recipe's input keys
				pos = self._get_pos_at(i, j)

				cur_recipe = cur_recipe = cur_row[j]
				input_recipe_count = len(cur_recipe.inputs.keys())
				line_start = (
						pos[0] + self.recipe_box_width / 2,
						pos[1] + self.recipe_box_height
					)

				if input_recipe_count == 0: #input resource
					#draw input line
					self.tree_canvas.create_line(
						line_start[0], line_start[1],
						line_start[0], line_start[1] + self.recipe_box_padding[1]/3,
						fill="#CFECF7"
					)
				else:
					#draw resource input line
					self.tree_canvas.create_line(
						line_start[0], line_start[1],
						line_start[0], line_start[1] + self.recipe_box_padding[1]/2,
						fill="#CFECF7"
					)
					for k in range(input_recipe_count):
						#draw connecting bar
						input_recipe_pos = self._get_pos_at(i + 1, k + draw_index)
						bar_start_pos = (min(input_recipe_pos[0], pos[0]) + self.recipe_box_width/2, line_start[1] + self.recipe_box_padding[1]/2)
						bar_end_pos = (max(self._get_pos_at(i + 1, input_recipe_count - 1 + draw_index)[0], pos[0]) + self.recipe_box_width/2, line_start[1] + self.recipe_box_padding[1]/2)

						self.tree_canvas.create_line(*bar_start_pos, *bar_end_pos, fill="#CFECF7")

						#draw connections to connecting bar
						self.tree_canvas.create_line(
							input_recipe_pos[0] + self.recipe_box_width/2, input_recipe_pos[1],
							input_recipe_pos[0] + self.recipe_box_width/2, input_recipe_pos[1] - self.recipe_box_padding[1]/2,
							fill="#CFECF7"
						)

					#incriment draw index
					draw_index += input_recipe_count

	def _get_pos_at(self, row, col):
		return (
				self.recipe_box_padding[0]/2 + (self.recipe_box_width + self.recipe_box_padding[0]) * ((max(*self.ppt_plan[1]) - self.ppt_plan[1][row]) / 2 + col),
				self.recipe_box_padding[1]/2 + (self.recipe_box_height + self.recipe_box_padding[1]) * row
			)

	
	def get_ppt_plan(self, production_path = None, depth = 0):
		'''
		Returns this window's production path as a list of rows

		Parameters:
			production_path (dict): production path to convert
			depth (int): depth of this function
		
		Returns:
			(list): production path as a list of rows
			(tuple): shape of the production path row list
		'''
		if production_path == None:
			production_path = self.production_path

		production_path_tree = []
		dimensions = []
		for i in range(depth):
			production_path_tree.append([])
			dimensions.append(0)

		production_path_tree.append([list(value.keys())[0] for value in list(production_path.values())[0]]) 
		dimensions.append(len(list(production_path.values())[0]))

		if len(list(production_path.values())[0]) > 0: #has inputs / sublevels
			input_paths = list(production_path.values())[0]
			for input_path in input_paths:
				#add path lengths of sub paths
				sub_ppt_rows, sub_ppt_dims = self.get_ppt_plan(input_path, depth + 1)
				
				for i in range(len(sub_ppt_rows)):
					if i == len(production_path_tree):
						production_path_tree.append(sub_ppt_rows[i])
						dimensions.append(sub_ppt_dims[i])
					else:
						production_path_tree[i] += sub_ppt_rows[i]
						dimensions[i] += sub_ppt_dims[i]
		
		if depth == 0:
			return [[list(production_path.keys())[0]]] + production_path_tree, [1] + dimensions #to account for inital recipe of the tree that isn't shown in any inputs
		else:
			return production_path_tree, tuple(dimensions)


Optimal_Satisfaction_UI().mainloop()