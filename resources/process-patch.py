#!/bin/python3
# vim: noet:ts=2:sts=2:sw=2

# SPDX-License-Identifier: MIT
# Copyright © 2024 David Llewellyn-Jones

from unidiff import PatchSet
from pathlib import Path
import os, sys

def syntax():
	print("Syntax: process-patch.py <patch-dir>")

class Stats:
	name = ""
	count = 0
	added = 0
	removed = 0

	def __init__(self, name):
		self.name = name

class PatchStats:
	directory = None
	patch_dir = "/home/flypig/Documents/Development/jolla/gecko-dev-esr91/gecko-dev/rpm/"

	filetype_stats = {}
	filetype_groups = {
		"C++": ["h", "cpp", "cc", "c", "inc", "symbols"],
		"JavaScript": ["jsm", "js", "css"],
		"Build": ["configure", "mk", "build", "in", "conf", "yaml", "manifest", "ini", "gn", "gni", "json", "py", "spec", "merqtxulrunner", "sh", "patch", "pri", "mozbuild", "toml"],
		"IDL": ["ipdl", "idl", "ipdlh"],
		"Rust": ["rs"],
		"Docs": ["txt", "rst", "1", "html"],
		"QML": ["qml"],
		"Unknown": ["unknown"]
	}
	filetype_grousp_reverse = {}
	patch_count = 0

	def __init__(self, patch_dir):
		self.patch_dir = patch_dir
		self.filetype_grousp_reverse = {ext: name for name, exts in self.filetype_groups.items() for ext in exts}
		self.patch_count = 0
		self.directory = os.fsencode(patch_dir)

	def generate(self):
		for item in os.listdir(self.directory):
			filename = os.fsdecode(item)
			if filename.endswith(".patch"):
				self.patch_count += 1
				patch = PatchSet.from_filename(self.patch_dir + filename, encoding="utf-8")
				file_num = len(patch)
				for item in patch:
					path = Path(item.path)
					added = item.added
					removed = item.removed
					filetype = path.suffix.strip(".")
					name = self.filetype_grousp_reverse.get(filetype, None)
					if name == None:
						print("Patch: {}, file: {}".format(filename, path))
						name = "Unknown"
						filetype = "unknown"

					stats = self.filetype_stats.get(name, Stats(name = name))
					stats.count += 1
					stats.added += item.added
					stats.removed += item.removed

					self.filetype_stats[name] = stats

	def output(self):
		print("Patches: {}".format(self.patch_count))
		print("{}: {}, {}, {}".format("Name", "Files", "Added", "Removed"))
		for name, status in self.filetype_stats.items():
			print("{}: {}, {}, {}".format(name, status.count, status.added, status.removed))

	def output_csv(self):
		version = "ESR 91"
		print("\"{}\",\"{}\",\"{}\",\"{}\"".format("Version", "Name", "Added", "Removed"))
		for name, status in self.filetype_stats.items():
			print("\"{}\",\"{}\",{},{}".format(version, name, status.added, status.removed))

# Execution entry point
if __name__ == "__main__":
	if len(sys.argv) != 2:
		syntax()
	else:
		patchstats = PatchStats(sys.argv[1])
		patchstats.generate()
		patchstats.output_csv()

