from tkinter import *

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
