#!/bin/python3
# vim: noet:ts=2:sts=2:sw=2

# SPDX-License-Identifier: MIT
# Copyright © 2024 David Llewellyn-Jones

from unidiff import PatchSet
from pathlib import Path
import os, sys

def syntax():
	print("Syntax: process-repo.py <repo-dir>")

class Stats:
	name = ""
	count = 0
	lines = 0

	def __init__(self, name):
		self.name = name

class RepoStats:
	repo_dir = "/home/flypig/Documents/Development/jolla/gecko-dev-esr91/gecko-dev/rpm/"
	count = 0
	unknown = set()

	filetype_stats = {}
	filetype_groups = {
		"C++": ["h", "cpp", "cc", "c", "inc", "symbols", "hin", "cxx", "hxx"],
		"JavaScript": ["jsm", "js", "css"],
		"Build": ["configure", "mk", "build", "in", "conf", "yaml", "manifest", "ini", "gn", "gni", "json", "py", "spec", "merqtxulrunner", "sh", "patch", "pri", "am", "ac", "list", "pro", "pri", "m4", "pc", "Makefile", "install-sh", "allowlist", "icon_system_install", "pbxproj", "Jenkinsfile", "rules", "nmf", "04-manylinux2014", "json5", "install", "Dockerfile", "make", "yml", "tmpl", "makefile", "jinja", "jinja2", "vcproj", "lua", "OWNERS"],
		"IDL": ["ipdl", "idl", "ipdlh", "webidl", "pidl", "proto"],
		"Rust": ["rs"],
		"Docs": ["txt", "rst", "1", "html", "dtd", "qdoc", "qdocconf", "qhp", "qch", "index", "README", "COPYING", "LICENSE", "changes", "docs", "terms", "mit", "man", "md", "jsp", "f"],
		"QML": ["qml", "qmltypes", "qmldir", "qm"],
		"Graphics": ["svg", "png", "jpg", "jpeg", "gif", "ttf", "webm", "404", "icon", "tiff", "mpeg", "PNG", "ico"],
		"Config": ["xml", "service", "xhtml", "user", "guess", "bashrc"],
		"WASM": ["wasm"],
		"Java": ["java"],
		"Go": ["Go", "go", "go2"],
		"Obj-C": ["m", "mm"],
		"TypeScript": ["ts"],
		"Other code": ["applescript", "rint", "glsl", "tcl", "wgsl", "win32_vulkan"],
		"Ignore": ["o", "moc", "so", "qrc", "sha1", "zip", "pyc", "subtest", "hpack", "apk", "acf", "44", "svgz", "acd", "jsv", "tflite", "22-email_mix_args_uri", "sdp", "01-menu_user_forceupdate", "vyml", "keychain", "abj", "7", "macho32b", "spv", "12", "icc", "md5", "pickle", "eps", "lzo", "bz2", "gzip", "sha512", "dll", "gz", "wav", "xslt", "obj", "7z"],
		"Unknown": ["unknown", ""]
	}
	filetype_grousp_reverse = {}

	def __init__(self, repo_dir):
		self.repo_dir = repo_dir
		self.filetype_grousp_reverse = {ext: name for name, exts in self.filetype_groups.items() for ext in exts}
		self.count = 0

	def search_directory(self, search_dir):
		with os.scandir(search_dir) as scan:

			for item in scan:
				filename = os.fsdecode(item.path)
				path = Path(filename)
				if not item.name.startswith('.'):
					if item.is_dir() and not item.is_symlink():
						self.search_directory(path)
					else:
						self.count += 1
						filetype = path.suffix.strip(".")
						original_filetype = filetype
						if filetype == "":
							filetype = path.name
						name = self.filetype_grousp_reverse.get(filetype, None)
						lines = 0
						if name == None:
							print("File: {}".format(item.path))
							self.unknown.add(original_filetype)
							name = "Unknown"
							filetype = "unknown"
						else:
							if name != "Ignore" and not item.is_symlink():
								with open(path, "r", encoding="utf8", errors="surrogateescape") as fh:
									lines = sum(1 for _ in fh)

						stats = self.filetype_stats.get(name, Stats(name = name))
						stats.count += 1
						stats.lines += lines

						self.filetype_stats[name] = stats

	def generate(self):
		self.search_directory(self.repo_dir)

	def output(self):
		filename = Path(self.repo_dir)
		print("Repo: {}".format(filename.name))
		print("Files: {}".format(self.count))
		print("{}: {}, {}".format("Name", "Files", "Lines"))
		for name, status in self.filetype_stats.items():
			print("{}: {}, {}".format(name, status.count, status.lines))
		print("Untracked filetypes:")
		print(self.unknown)

	def output_csv(self, version):
		print("\"{}\",\"{}\",\"{}\"".format("Version", "Name", "Lines"))
		for name, status in self.filetype_stats.items():
			print("\"{}\",\"{}\",{}".format(version, name, status.lines))

# Execution entry point
if __name__ == "__main__":
	if len(sys.argv) == 1:
		files = [
			"/home/flypig/Documents/Development/jolla/sailfish-browser",
			"/home/flypig/Documents/Development/jolla/sailfish-components-webview",
			"/home/flypig/Documents/Development/jolla/embedlite-components",
			"/home/flypig/Documents/Development/jolla/qtmozembed",
			"/home/flypig/Documents/Development/jolla/gecko-dev-project/gecko-dev",
		]
		repostats = RepoStats("")
		for file in files:
			repostats.repo_dir = file
			repostats.generate()
		repostats.output_csv("ESR 78")
	elif len(sys.argv) != 2:
		syntax()
	else:
		repostats = RepoStats(sys.argv[1])
		repostats.generate()
		repostats.output_csv("Chromium")

