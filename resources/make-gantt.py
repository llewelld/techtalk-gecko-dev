#!/bin/python3
# vim: noet:ts=2:sts=2:sw=2

# SPDX-License-Identifier: MIT
# Copyright © 2024 David Llewellyn-Jones

import drawsvg as draw
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import json
from math import sin, pi

class Gantt:
	data = None
	cellwidth = 32
	cellheight = 32
	width = 0
	height = 0
	canvas = None
	headerheight = 32
	groupwidth = 64
	bar_border = 4
	arrow_head = None
	arrow_head_offset = 1
	path_offset = 32
	colour_cycle = "row"
	colour_total = 0

	def __init__(self, data_file, cellwidth, cellheight):
		with open(data_file) as fh:
			self.data = json.load(fh)
		
		row = 0
		for bar in self.data["bars"]:
			if bar.get("row"):
				bar["row"] = self.get_bar_by_name(bar["row"])["row"]
			else:
				bar["row"] = row
				row += 1

		self.cellwidth = cellwidth
		self.cellheight = cellheight
		self.groupwidth = self.cellwidth * 3
		self.headerheight = self.cellheight
		self.width = self.groupwidth + ((self.data["end"] - self.data["start"]) * self.cellwidth)
		self.height = self.headerheight + (row * self.cellheight)
		self.path_offset = self.cellwidth / 2

		scale = 8
		shift = self.arrow_head_offset / scale
		self.arrow_head = draw.Marker(-1.0 + shift, -0.5, 0.0 + shift, 0.5, scale=scale, orient="auto")
		self.arrow_head.append(draw.Lines(-1.0 + shift, -0.5, -1.0 + shift, 0.5, 0.0 + shift, 0.0, fill="black", close=True))

		self.colour_cycle = self.data["colour_cycle"]
		if self.colour_cycle == "bar":
			self.colour_total = len(self.data["bars"])
		elif self.colour_cycle == "row":
			self.colour_total = row
		elif self.colour_cycle == "group":
			self.colour_total = len(self.data["groups"])

	def draw_grid(self, x, y, width, height, cellwidth, cellheight):
		for xpos in range(x, x + width, cellwidth):
			line = draw.Line(xpos, y, xpos, y + height, stroke="black", stroke_width=1, stroke_dasharray="1,3")
			self.canvas.append(line)
		for ypos in range(y, y + height, cellheight):
			line = draw.Line(x, ypos, x + width, ypos, stroke="black", stroke_width=1, stroke_dasharray="1,3")
			self.canvas.append(line)

	def draw_bar(self, row, start, end, colour):
		x = self.groupwidth + (start * self.cellwidth)
		y = self.headerheight + (row * self.cellheight)
		width = (end * self.cellwidth) - (start * self.cellwidth)
		height = self.cellheight
		rect = draw.Rectangle(x, y + self.bar_border, width, height - (2 * self.bar_border), fill=colour, stroke="black", stroke_width=1, rx=self.bar_border)
		self.canvas.append(rect)

	def draw_group(self, text, row_start, row_end):
		if row_start == 0:
			item = draw.Line(0, self.headerheight, self.groupwidth, self.headerheight, stroke="black", stroke_width=1, stroke_dasharray="1,3")
			self.canvas.append(item)

		item = draw.Line(0, self.headerheight + (row_end * self.cellheight), self.groupwidth, self.headerheight + (row_end * self.cellheight), stroke="black", stroke_width=1, stroke_dasharray="1,3")
		self.canvas.append(item)
		item = draw.Text(
			text,
			12,
			x=self.groupwidth - (self.cellwidth / 12) - (self.bar_border * 3),
			y=self.headerheight + (row_end + row_start)*0.5*self.cellheight,
			text_anchor="end",
			dominant_baseline="middle",
			font_weight="bold",
		)
		self.canvas.append(item)

	def add_text_cell(self, text, row, column):
			item = draw.Text(
				text,
				12,
				x=self.groupwidth + (column * self.cellwidth) + (self.cellwidth / 10),
				y=self.headerheight + ((row + 0.5) * self.cellheight),
				text_anchor="start",
				dominant_baseline="middle",
			)
			self.canvas.append(item)

	def draw_header(self):
		for count in range(0, self.data["end"] - self.data["start"]):
			text = "{:02}".format((self.data["start"] + count) % 100)
			item = draw.Text(
				text,
				12,
				x=self.groupwidth + (count*self.cellwidth) + (self.cellwidth / 2),
				y=(self.headerheight / 2),
				text_anchor="middle",
				dominant_baseline="middle",
			)
			self.canvas.append(item)

	def draw_path_middle_start(self, col_start, row_start, col_end, row_end):
		path = draw.Path(stroke_width=1, stroke="black", fill="none", marker_end=self.arrow_head)
		x = self.groupwidth + (col_start + 0.5) * self.cellwidth
		y = self.headerheight + (row_start + 1) * self.cellheight - self.bar_border
		path.M(x, y)
		y = self.headerheight + (row_end + 0.5) * self.cellheight - self.bar_border
		path.V(y)
		x_ctl_1 = x
		y_ctl_1 = y + (self.bar_border / 2)
		x_ctl_2 = x + (self.bar_border / 2)
		y_ctl_2 = y + self.bar_border
		x_end = x + self.bar_border
		y_end = y + self.bar_border
		path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)
		x = self.groupwidth + (col_end * self.cellwidth) - self.arrow_head_offset
		path.H(x)
		self.canvas.append(path)

	def draw_path_end_start_down_right(self, path, col_start, row_start, col_end, row_end):
			x_mid = self.groupwidth + ((col_start + col_end) / 2.0) * self.cellwidth
			x = self.groupwidth + (col_start + 0.0) * self.cellwidth
			y = self.headerheight + (row_start + 0.5) * self.cellheight
			path.M(x, y)
			x = x_mid - self.bar_border
			path.H(x)
			x_ctl_1 = x + (self.bar_border / 2)
			y_ctl_1 = y
			x_ctl_2 = x + self.bar_border
			y_ctl_2 = y + (self.bar_border / 2.0)
			x_end = x + self.bar_border
			y_end = y + self.bar_border
			path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)
			x = x_mid
			y = self.headerheight + (row_end + 0.5) * self.cellheight - self.bar_border
			path.V(y)
			x_ctl_1 = x
			y_ctl_1 = y + (self.bar_border / 2.0)
			x_ctl_2 = x + (self.bar_border / 2.0)
			y_ctl_2 = y + self.bar_border
			x_end = x + self.bar_border
			y_end = y + self.bar_border
			path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)
			x = self.groupwidth + (col_end * self.cellwidth) - self.arrow_head_offset
			path.H(x)

	def draw_path_end_start_down_left(self, path, col_start, row_start, col_end, row_end):
			x_mid = self.groupwidth + ((col_start + col_end) / 2.0) * self.cellwidth
			y_mid = self.headerheight + ((row_start + row_end + 1.0) / 2.0) * self.cellheight
			x = self.groupwidth + (col_start + 0.0) * self.cellwidth
			y = self.headerheight + (row_start + 0.5) * self.cellheight
			path.M(x, y)

			x = x + self.path_offset - self.bar_border
			path.H(x)

			x_ctl_1 = x + (self.bar_border / 2)
			y_ctl_1 = y
			x_ctl_2 = x + self.bar_border
			y_ctl_2 = y + (self.bar_border / 2.0)
			x_end = x + self.bar_border
			y_end = y + self.bar_border
			path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)

			x = x + self.bar_border
			y = y_mid - self.bar_border
			path.V(y)

			x_ctl_1 = x
			y_ctl_1 = y + (self.bar_border / 2)
			x_ctl_2 = x - (self.bar_border / 2)
			y_ctl_2 = y + self.bar_border
			x_end = x - self.bar_border
			y_end = y + self.bar_border
			path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)

			x = self.groupwidth + (col_end - 0.0) * self.cellwidth - self.path_offset + self.bar_border
			y = y + self.bar_border
			path.H(x)
			
			x_ctl_1 = x - (self.bar_border / 2)
			y_ctl_1 = y
			x_ctl_2 = x - self.bar_border
			y_ctl_2 = y + (self.bar_border / 2.0)
			x_end = x - self.bar_border
			y_end = y + self.bar_border
			path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)

			x = x - self.bar_border
			y = self.headerheight + (row_end + 0.5) * self.cellheight - self.bar_border
			path.V(y)
			
			x_ctl_1 = x
			y_ctl_1 = y + (self.bar_border / 2)
			x_ctl_2 = x + (self.bar_border / 2)
			y_ctl_2 = y + self.bar_border
			x_end = x + self.bar_border
			y_end = y + self.bar_border
			path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)
			
			x = self.groupwidth + (col_end * self.cellwidth) - self.arrow_head_offset
			path.H(x)

	def draw_path_end_start_up_left(self, path, col_start, row_start, col_end, row_end):
			x_mid = self.groupwidth + ((col_start + col_end) / 2.0) * self.cellwidth
			y_mid = self.headerheight + ((row_start + row_end + 1.0) / 2.0) * self.cellheight
			x = self.groupwidth + (col_start + 0.0) * self.cellwidth
			y = self.headerheight + (row_start + 0.5) * self.cellheight
			path.M(x, y)

			x = x + self.path_offset - self.bar_border
			path.H(x)

			x_ctl_1 = x + (self.bar_border / 2)
			y_ctl_1 = y
			x_ctl_2 = x + self.bar_border
			y_ctl_2 = y - (self.bar_border / 2.0)
			x_end = x + self.bar_border
			y_end = y - self.bar_border
			path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)

			x = x + self.bar_border
			y = y_mid + self.bar_border
			path.V(y)

			x_ctl_1 = x
			y_ctl_1 = y - (self.bar_border / 2)
			x_ctl_2 = x - (self.bar_border / 2)
			y_ctl_2 = y - self.bar_border
			x_end = x - self.bar_border
			y_end = y - self.bar_border
			path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)

			x = self.groupwidth + (col_end - 0.0) * self.cellwidth - self.path_offset + self.bar_border
			y = y - self.bar_border
			path.H(x)
			
			x_ctl_1 = x - (self.bar_border / 2)
			y_ctl_1 = y
			x_ctl_2 = x - self.bar_border
			y_ctl_2 = y - (self.bar_border / 2.0)
			x_end = x - self.bar_border
			y_end = y - self.bar_border
			path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)

			x = x - self.bar_border
			y = self.headerheight + (row_end + 0.5) * self.cellheight + self.bar_border
			path.V(y)
			
			x_ctl_1 = x
			y_ctl_1 = y - (self.bar_border / 2)
			x_ctl_2 = x + (self.bar_border / 2)
			y_ctl_2 = y - self.bar_border
			x_end = x + self.bar_border
			y_end = y - self.bar_border
			path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)
			
			x = self.groupwidth + (col_end * self.cellwidth) - self.arrow_head_offset
			path.H(x)

	def draw_path_end_start(self, col_start, row_start, col_end, row_end):
		path = draw.Path(stroke_width=1, stroke="black", fill="none", marker_end=self.arrow_head)
		if col_start < col_end:
			self.draw_path_end_start_down_right(path, col_start, row_start, col_end, row_end)
		else:
			if row_start <= row_end:
				self.draw_path_end_start_down_left(path, col_start, row_start, col_end, row_end)
			else:
				self.draw_path_end_start_up_left(path, col_start, row_start, col_end, row_end)
		self.canvas.append(path)

	def draw_connection(self, start, end, pos_out, pos_in):
		offset = self.data["start"]
		if pos_out == "end" and pos_in == "start":
			self.draw_path_end_start(start["end"] - offset, start["row"], end["start"] - offset, end["row"])
		if pos_out == "body" and pos_in == "start":
			if start["start"] < end["start"]:
				if start["end"] >= end["start"]:
					self.draw_path_middle_start(end["start"] - 1 - offset, start["row"], end["start"] - offset, end["row"])
				else:
					self.draw_path_middle_start(start["end"] - 1 - offset, start["row"], end["start"] - offset, end["row"])
			else:
				print("Error: bar connection not supported from {} to {}".format(start["name"], end["name"]))

	def draw_brace(self, x_min, y_min, y_max):
		path = draw.Path(stroke_width=1, stroke="black", fill="none")
		width = self.bar_border * 2
		x_mid = x_min + width / 2
		y_mid = (y_min + y_max) / 2
		x = x_min + width
		y = y_min
		path.M(x, y)

		x_ctl_1 = x - (width / 4)
		y_ctl_1 = y
		x_ctl_2 = x - (width / 2)
		y_ctl_2 = y + (width / 4)
		x_end = x - (width / 2)
		y_end = y + (width / 2)
		path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)
		
		x = x - (width / 2)
		y = y_mid - (width / 2)
		path.V(y)

		x_ctl_1 = x
		y_ctl_1 = y + (width / 4)
		x_ctl_2 = x - (width / 4)
		y_ctl_2 = y + (width / 2)
		x_end = x - (width / 2)
		y_end = y + (width / 2)
		path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)

		x = x - (width / 2)
		y = y + (width / 2)
		
		x_ctl_1 = x + (width / 4)
		y_ctl_1 = y
		x_ctl_2 = x +	 (width / 2)
		y_ctl_2 = y + (width / 4)
		x_end = x + (width / 2)
		y_end = y + (width / 2)
		path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)

		x = x + (width / 2)
		y = y_max - (width / 2)
		path.V(y)

		x_ctl_1 = x
		y_ctl_1 = y + (width / 4)
		x_ctl_2 = x + (width / 4)
		y_ctl_2 = y + (width / 2)
		x_end = x + (width / 2)
		y_end = y + (width / 2)
		path.C(x_ctl_1, y_ctl_1, x_ctl_2, y_ctl_2, x_end, y_end)

		self.canvas.append(path)

	def get_bar_by_name(self, name):
		found = None
		for bar in self.data["bars"]:
			if bar["name"] == name:
				found = bar
		return found

	def get_colour(self, count):
		proportion = 0.95 - (count / self.colour_total)
		pale = 0.7
		red = round(255 * (pale + (1.0 - pale) * (sin(2 * pi * (proportion + (1/3))) + 1) / 2))
		green = round(255 * (pale + (1.0 - pale) * (sin(2 * pi * (proportion + (2/3))) + 1) / 2))
		blue = round(255 * (pale + (1.0 - pale) * (sin(2 * pi * (proportion + (0/3))) + 1) / 2))
		hex_colour = "#{:02X}{:02X}{:02X}".format(red, green, blue)
		return hex_colour

	def draw(self):
		self.canvas = draw.Drawing(self.width + 4, self.height + 4, origin=(0, 0))
		self.draw_grid(self.groupwidth, self.headerheight, self.width - self.groupwidth + 1, self.height - self.headerheight + 1, self.cellwidth, self.cellheight)
		self.draw_header()

		colours = []
		count = 0
		row_colours = []
		if self.colour_cycle == "group":
			bars_in_row = []
			count = 0
			for bar in self.data["bars"]:
				if bar["row"] >= count:
					bars_in_row.append(1)
					count += 1
				else:
					bars_in_row[bar["row"]] += 1
			row = 0
			count = 0
			for group in self.data["groups"]:
				for item in range(group["items"]):
					for bar in range(bars_in_row[row]):
						colours.append(count)
					row += 1
				count += 1
		else:
			for bar in self.data["bars"]:
				if self.colour_cycle == "bar":
					colours.append(count)
					count += 1
				elif self.colour_cycle == "row":
					print("{}: {}, {}".format(bar["name"], count, bar["row"]))
					if bar["row"] >= count:
						colours.append(count)
						row_colours.append(count)
						count += 1
					else:
						colours.append(row_colours[bar["row"]])

		count = 0
		for bar in self.data["bars"]:
			start = bar["start"] - self.data["start"]
			colour = self.get_colour(colours[count])
			self.draw_bar(bar["row"], start, bar["end"] - self.data["start"], colour)
			name = bar.get("label", bar["name"])
			self.add_text_cell(name, bar["row"], start)
			count += 1

		row_start = 0
		for group in self.data["groups"]:
			self.draw_group(group["name"], row_start, row_start + group["items"])
			x_start = self.groupwidth - self.bar_border * 3
			y_start = (row_start * self.cellheight) + self.headerheight + self.bar_border
			y_end = ((row_start + group["items"]) * self.cellheight) + self.headerheight - self.bar_border
			self.draw_brace(x_start, y_start, y_end)
			row_start += group["items"]

		for connection in self.data["connections"]:
			start = self.get_bar_by_name(connection["start"])
			end = self.get_bar_by_name(connection["end"])
			self.draw_connection(start, end, connection["out"], connection["in"])

		self.canvas.save_svg("gantt.svg")
		self.canvas.save_png("gantt.png")

gantt = Gantt("browsers.json", 32, 32)
gantt.draw()

