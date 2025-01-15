from tkinter import *
from tkinter import ttk
from Drag_Sort import Drag_Sort

import Items


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

		ttk.Label(mainframe).grid(column=0, row=2, columnspan=2)

		ttk.Label(mainframe, text="Production rate (items/min): ").grid(column=0, row=3, sticky="W")

		self.production_rate_str = StringVar(value="0")
		production_rate_inputbox = ttk.Entry(mainframe, textvariable=self.production_rate_str, width=6)
		production_rate_inputbox.bind("<FocusOut>", lambda _: self.finalize_production_rate_input())
		self.production_rate_str.trace_add("write", lambda *_: self.validate_production_rate_input())
		production_rate_inputbox.grid(column=1, row=3, sticky="W")

		automatic_production_rate_checkbox = ttk.Button(mainframe, text="Calculate production rate from inputs", command=self.calculate_production_rate)
		automatic_production_rate_checkbox.grid(column=0, row=4, sticky="W", columnspan=2)

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

		ttk.Button(mainframe, command=lambda: Item_Selection(root, self.input_resources), text="test").grid(column=0, row=10)

		#ds = Drag_Sort(root, ["Hello", "World", "test", "test", "test"])
		#ds.grid(column=0, row=5)
	

	def mainloop(self):
		self.root.mainloop()


	def calculate_production_rate(self):
		'''Calculates production rate from inputs, updates production rate input box to match the calculated value, and disables user input to that box'''
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


class Item_Selection:
	def __init__(self, root, listvariable):
		self.listvariable = listvariable

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
		self.listvariable.append([self.item_list[self.item_listbox.curselection()[0]], int(self.production_rate_str.get())])
		print(self.listvariable)
		self.destroy()


	def destroy(self):
		self.root.destroy()

Optimal_Satisfaction_UI().mainloop()