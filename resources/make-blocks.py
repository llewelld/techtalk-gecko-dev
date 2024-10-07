#!/bin/python3
# vim: noet:ts=2:sts=2:sw=2

# SPDX-License-Identifier: MIT
# Copyright © 2024 David Llewellyn-Jones

import drawsvg as draw
import json
from math import sin, pi

class Graph:
	data = None
	cellwidth = 32
	cellheight = 32
	gapwidth = 16
	gapheight = 16

	width = 0
	height = 0

	canvas = None
	headerheight = 192
	bar_border = 16
	arrow_head = None
	arrow_head_offset = 1
	path_offset = 32
	colour_cycle = "block"
	colour_total = 0
	connections_side_total= []
	connection_scale = 0.2
	curve_strength = 2/3
	path_width = 3
	node_border_width = 2
	offset_x = 0
	offset_y = 0

	def __init__(self, data_file):
		with open(data_file) as fh:
			self.data = json.load(fh)
		
		self.cellwidth = self.data["cellwidth"]
		self.cellheight = self.data["cellheight"]
		self.gapwidth = self.data["gapwidth"]
		self.gapheight = self.data["gapheight"]

		self.offset_x = self.gapwidth / 2
		self.offset_y = self.headerheight

		self.width = self.data["width"] * (self.cellwidth + self.gapwidth) - (self.gapheight / 2.0) + self.offset_x
		self.height = self.data["height"] * (self.cellheight + self.gapheight) - self.gapheight + self.offset_y

		self.path_offset = self.cellwidth / 2

		scale = 8
		shift = self.arrow_head_offset / scale
		self.arrow_head = draw.Marker(-1.0 + shift, -0.5, 0.0 + shift, 0.5, scale=scale, orient="auto")
		self.arrow_head.append(draw.Lines(-1.0 + shift, -0.5, -1.0 + shift, 0.5, 0.0 + shift, 0.0, fill="black", close=True))

		self.colour_cycle = self.data["colour_cycle"]
		if self.colour_cycle == "node":
			self.colour_total = len(self.data["nodes"])
		elif self.colour_cycle == "position":
			self.colour_total = self.data["width"] * self.data["height"]
		elif self.colour_cycle == "height":
			self.colour_total = self.data["height"]
		elif self.colour_cycle == "width":
			self.colour_total = self.data["width"]
		elif self.colour_cycle == "group":
			self.colour_total = len(self.data["groups"])

		count = 0
		for node in self.data["nodes"]:
			node["count"] = count
			count += 1

		self.connections_side_total = [[0, 0, 0, 0] for _ in range(count)]
		for connection in self.data["connections"]:
			start = self.get_node_by_name(connection["start"])
			end = self.get_node_by_name(connection["end"])
			best_side = self.best_side(start, end)
			connection["offset_in"] = self.connections_side_total[end["count"]][best_side[1]]
			connection["offset_out"] = self.connections_side_total[start["count"]][best_side[0]]
			self.connections_side_total[end["count"]][best_side[1]] += 1
			self.connections_side_total[start["count"]][best_side[0]] += 1

	def draw_node(self, cellx, celly, colour):
		x = cellx * (self.cellwidth + self.gapwidth) + self.offset_x
		y = celly * (self.cellheight + self.gapheight) + self.offset_y
		width = self.cellwidth
		height = self.cellheight
		rect = draw.Rectangle(x, y, width, height, fill=colour, stroke="black", stroke_width=self.node_border_width, rx=self.bar_border)
		self.canvas.append(rect)

	def add_text_cell(self, text, cellx, celly):
			item = draw.Text(
				text,
				24,
				x=(cellx * (self.cellwidth + self.gapwidth)) + (self.cellwidth / 2.0) + self.offset_x,
				y=(celly * (self.cellheight + self.gapheight)) + (self.cellheight / 2.0) + self.offset_y,
				text_anchor="middle",
				dominant_baseline="middle",
				line_offset=-1,
			)
			item
			self.canvas.append(item)

	def get_node_by_name(self, name):
		found = None
		for node in self.data["nodes"]:
			if node["name"] == name:
				found = node
		return found

	def get_colour(self, count):
		proportion = 0.95 - (count / self.colour_total)
		pale = 0.7
		red = round(255 * (pale + (1.0 - pale) * (sin(2 * pi * (proportion + (1/3))) + 1) / 2))
		green = round(255 * (pale + (1.0 - pale) * (sin(2 * pi * (proportion + (2/3))) + 1) / 2))
		blue = round(255 * (pale + (1.0 - pale) * (sin(2 * pi * (proportion + (0/3))) + 1) / 2))
		hex_colour = "#{:02X}{:02X}{:02X}".format(red, green, blue)
		return hex_colour

	def best_side(self, start, end):
		sides = (0, 0)
		startx = start["x"]
		starty = start["y"]
		endx = end["x"]
		endy = end["y"]
		deltax = abs(startx - endx)
		deltay = abs(starty - endy)
		if (deltax <= deltay):
			# Vertical lines
			if (starty <= endy):
				sides = (2, 0)
			else:
				sides = (0, 2)
		else:
			if (startx <= endx):
				sides = (3, 1)
			else:
				sides = (1, 3)
		return sides

	def draw_connection(self, text, start, end, offset_out, offset_in, total_out, total_in):
		startx = start["x"] * (self.cellwidth + self.gapwidth) + (self.cellwidth / 2.0) + self.offset_x
		starty = start["y"] * (self.cellheight + self.gapheight) + (self.cellheight / 2.0) + self.offset_y
		endx = end["x"] * (self.cellwidth + self.gapwidth) + (self.cellwidth / 2.0) + self.offset_x
		endy = end["y"] * (self.cellheight + self.gapheight) + (self.cellheight / 2.0) + self.offset_y

		best_side = self.best_side(start, end)
		startx_offset = self.cellwidth * ([0, 0.5, 0, -0.5][best_side[1]])
		starty_offset = self.cellheight * ([0.5, 0, -0.5, 0][best_side[1]])
		endx_offset = self.cellwidth * ([0, 0.5, 0, -0.5][best_side[0]])
		endy_offset = self.cellheight * ([0.5, 0, -0.5, 0][best_side[0]])
		
		horizontal = (best_side[0] % 2 != 0)

		if total_out > 1:
			if horizontal:
				starty_offset += self.connection_scale * self.cellheight * ((2 * offset_out / (total_out - 1)) - 1)
			else:
				startx_offset += self.connection_scale * self.cellwidth * ((2 * offset_out / (total_out - 1)) - 1)

		if total_in > 1:
			if horizontal:
				endy_offset += self.connection_scale * self.cellheight * ((2 * offset_in / (total_in - 1)) - 1)
			else:
				endx_offset += self.connection_scale * self.cellwidth * ((2 * offset_in / (total_in - 1)) - 1)

		startx += startx_offset
		starty += starty_offset
		endx += endx_offset
		endy += endy_offset

		path = self.draw_arrow(startx, starty, endx, endy, horizontal)

		item = draw.Text(
			text,
			20,
			text_anchor="middle",
			line_offset=-1,
			offset="50%",
			side="right",
			path=path
		)
		self.canvas.append(item)		

	def draw_arrow(self, startx, starty, endx, endy, horizontal):
		path = draw.Path(stroke_width=self.path_width, stroke="black", fill="none", marker_end=self.arrow_head)
		path.M(startx, starty)
		if horizontal:
			x_ctl_1 = startx + self.curve_strength * (endx - startx)
			y_ctl_1 = starty
			x_ctl_2 = startx + (1 - self.curve_strength) * (endx - startx)
			y_ctl_2 = endy
			x_end = endx
			y_end = endy
		else:
			x_ctl_1 = startx
			y_ctl_1 = starty + self.curve_strength * (endy - starty)
			x_ctl_2 = endx
			y_ctl_2 = starty + (1 - self.curve_strength) * (endy - starty)
			x_end = endx
			y_end = endy
		path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)
		self.canvas.append(path)
		return path

	def draw_brace(self, x_min, x_max, y_min):
		path = draw.Path(stroke_width=self.path_width, stroke="black", fill="none")
		height = self.bar_border * 2
		y_mid = y_min + height / 2
		x_mid = (x_min + x_max) / 2
		y = y_min + height
		x = x_min
		path.M(x, y)

		y_ctl_1 = y - (height / 4)
		x_ctl_1 = x
		y_ctl_2 = y - (height / 2)
		x_ctl_2 = x + (height / 4)
		y_end = y - (height / 2)
		x_end = x + (height / 2)
		path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)
		
		y = y - (height / 2)
		x = x_mid - (height / 2)
		path.H(x)

		y_ctl_1 = y
		x_ctl_1 = x + (height / 4)
		y_ctl_2 = y - (height / 4)
		x_ctl_2 = x + (height / 2)
		y_end = y - (height / 2)
		x_end = x + (height / 2)
		path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)

		y = y - (height / 2)
		x = x + (height / 2)
		
		y_ctl_1 = y + (height / 4)
		x_ctl_1 = x
		y_ctl_2 = y +	(height / 2)
		x_ctl_2 = x + (height / 4)
		y_end = y + (height / 2)
		x_end = x + (height / 2)
		path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)

		y = y + (height / 2)
		x = x_max - (height / 2)
		path.H(x)

		y_ctl_1 = y
		x_ctl_1 = x + (height / 4)
		y_ctl_2 = y + (height / 4)
		x_ctl_2 = x + (height / 2)
		y_end = y + (height / 2)
		x_end = x + (height / 2)
		path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)

		self.canvas.append(path)

	def draw_group(self, xstart, ystart, width, height, name):
		overlap = self.gapwidth / 2.0 - self.bar_border
		x = xstart * (self.cellwidth + self.gapwidth) - overlap + self.offset_x
		y = ystart * (self.cellheight + self.gapheight) + self.offset_y - (self.headerheight / 2.0)
		x_size = ((self.cellwidth + self.gapwidth) * width) - self.gapwidth + (overlap * 2)
		y_size = ((self.cellheight + self.gapheight) * height)

		if ystart > 0:
			y += self.bar_border

		self.draw_brace(x, x + x_size, y)

		item = draw.Text(
			name,
			24,
			x=x + (x_size / 2.0),
			y=y - (self.bar_border * 2.0),
			text_anchor="middle",
			dominant_baseline="middle",
			line_offset=-1,
		)
		item
		self.canvas.append(item)

	def draw_group_line(self, xstart, ystart, yend):
		overlap = self.gapwidth / 2.0
		x = xstart * (self.cellwidth + self.gapwidth) - overlap + self.offset_x
		y = ystart * (self.cellheight + self.gapheight) + self.offset_y - (self.headerheight / 2.0) + self.bar_border

		y_size = ((self.cellheight + self.gapheight) * (yend - ystart)) - (2 * self.bar_border)
		if yend == self.data["height"]:
			y_size = self.height - y

		item = draw.Line(x, y + (4 * self.bar_border), x, y + y_size, stroke="black", stroke_width=2, stroke_dasharray="3,9")
		self.canvas.append(item)

	def draw_groups(self):
		count = 0
		for group in self.data["groups"]:
			items = group["items"]
			end = count + items
			xstart = (count // self.data["height"])
			xend = ((end + self.data["height"] - 1) // self.data["height"])
			ystart = (count % self.data["height"])
			yend = (end % self.data["height"])
			if yend == 0:
				yend = self.data["height"]
			width = xend - xstart
			height = yend - ystart
			self.draw_group(xstart, ystart, width, height, group["name"])
			count += items

		gaps = [[False for _ in range(self.data["height"])] for _ in range(self.data["width"])]
		count = 0
		for group in self.data["groups"]:
			items = group["items"]
			x = count // self.data["height"] + 1
			y = count % self.data["height"] + 1
			if y < self.data["height"]:
				gaps[x][y] = True
				if x < self.data["width"]:
					gaps[x + 1][y] = True

		for x in range(1, self.data["width"]):
			ystart = 0
			for y in range(self.data["height"] - 1):
				if gaps[x][y + 1]:
					self.draw_group_line(x, ystart, y + 1)
					ystart = y + 1
			self.draw_group_line(x, ystart, self.data["height"])

	def draw(self):
		self.canvas = draw.Drawing(self.width + 4, self.height + 4, origin=(0, 0))

		colours = []
		count = 0
		if self.colour_cycle == "node":
			for node in self.data["nodes"]:
				colours.append(count)
				count += 1
		elif self.colour_cycle == "position":
			count = 0
			for node in self.data["nodes"]:
				cellx = node["x"]
				celly = node["y"]
				colour = celly * self.data["width"] + cellx
				colours.append(colour)
				count += 1
		elif self.colour_cycle == "height":
			count = 0
			for node in self.data["nodes"]:
				celly = node["y"]
				colours.append(celly)
				count += 1
		elif self.colour_cycle == "width":
			count = 0
			for node in self.data["nodes"]:
				cellx = node["x"]
				colours.append(cellx)
				count += 1
		elif self.colour_cycle == "group":
			group_grid = []
			count = 0
			for group in self.data["groups"]:
				for _ in range(group["items"]):
					group_grid.append(count)
				count += 1
			for node in self.data["nodes"]:
				count = node["x"] * self.data["height"] + node["y"]
				colours.append(group_grid[count])

		count = 0
		for node in self.data["nodes"]:
			colour = node.get("colour", None)
			if colour:
				node["colour"] = self.get_node_by_name(colour)["colour"]
			else:
				node["colour"] = self.get_colour(colours[count])
			count += 1

		count = 0
		for node in self.data["nodes"]:
			colour = node["colour"]
			cellx = node["x"]
			celly = node["y"]
			self.draw_node(cellx, celly, colour)
			name = node.get("label", node["name"])
			self.add_text_cell(name, cellx, celly)
			count += 1

		for connection in self.data["connections"]:
			start = self.get_node_by_name(connection["start"])
			end = self.get_node_by_name(connection["end"])
			sides = self.best_side(start, end)
			offset_out = connection["offset_out"]
			offset_in = connection["offset_in"]
			total_out = self.connections_side_total[start["count"]][sides[0]]
			total_in = self.connections_side_total[end["count"]][sides[1]]
			name = connection.get("label", connection["name"])
			self.draw_connection(name, start, end, offset_out, offset_in, total_out, total_in)

		self.draw_groups()

		self.canvas.save_svg("internals.svg")
		self.canvas.save_png("internals.png")

graph = Graph("internals.json")
graph.draw()

