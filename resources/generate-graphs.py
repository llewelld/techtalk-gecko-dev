#!/bin/python3
# vim: noet:ts=2:sts=2:sw=2

# SPDX-License-Identifier: MIT
# Copyright © 2024 David Llewellyn-Jones

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import matplotlib

# Total lines of gecko engine code

df = pd.read_csv("totals.csv", quotechar="\"", quoting=csv.QUOTE_NONNUMERIC)
print(df)

fig, ax = plt.subplots()
plt.grid(axis="y")
plt.ylim(0, 14000000)
bar_colours = ["#e2e57dff", "#94ec95ff"]
bar_colours_added = ["#e2e57dff", "#94ec95ff"]
bar_colours_removed = ["#a6a946ff", "#87bb87ff"]

categories = ["ESR 78", "ESR 91"]
df.sort_values(by="Lines", ascending=False, inplace=True)
versions = [df[df["Version"] == category] for category in categories]
bar_width = 1.0 / 2.0
multiplier = 0
for version in versions:
	x = np.arange(len(version))
	lines = np.array(version["Lines"])
	names = np.array(version["Name"])
	offset = bar_width * multiplier
	rects = ax.bar(x + offset, lines, bar_width * 0.8, label="{}".format(categories[multiplier]), color=bar_colours[multiplier])
	multiplier += 1

ax.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x / 1000000), ' ')))

fig.subplots_adjust(bottom=0.2, wspace=0.2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.set_axisbelow(True)
ax.set_xticks(x + 0.5 * bar_width, names)
ax.set_ylabel("Million lines of code")
ax.set_title("Gecko engine source by language")
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
ax.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, -0.1), handlelength=1, handleheight=1, fancybox=False, shadow=False, frameon=False, edgecolor="#ffffff00")

plt.savefig("totals.png", dpi=360)
plt.savefig("totals.svg", dpi=360)
plt.savefig("totals.pdf", dpi=360, transparent=True)

# Total lines of Chromium code

df = pd.read_csv("totals-chromium.csv", quotechar="\"", quoting=csv.QUOTE_NONNUMERIC)
print(df)

fig, ax = plt.subplots()
plt.grid(axis="y")
plt.ylim(0, 80000000)
bar_colours = ["#e2e57dff", "#94ec95ff"]
bar_colours_added = ["#e2e57dff", "#94ec95ff"]
bar_colours_removed = ["#a6a946ff", "#87bb87ff"]
bar_colours_chromium = ["#97bceaff"]

categories = ["Chromium"]
df.sort_values(by="Lines", ascending=False, inplace=True)
versions = [df[df["Version"] == category] for category in categories]
bar_width = 1.0 / 1.0
multiplier = 0
for version in versions:
	x = np.arange(len(version))
	lines = np.array(version["Lines"])
	names = np.array(version["Name"])
	offset = bar_width * multiplier
	rects = ax.bar(x + offset, lines, bar_width * 0.8, label="{}".format(categories[multiplier]), color=bar_colours_chromium[multiplier])
	multiplier += 1

ax.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x / 1000000), ' ')))

fig.subplots_adjust(bottom=0.2, wspace=0.2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.set_axisbelow(True)
ax.set_xticks(x + 0.0 * bar_width, names)
ax.set_ylabel("Million lines of code")
ax.set_title("Chromium source by language")
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
plt.xticks(rotation=90)

plt.savefig("totals-chromium.png", dpi=360)
plt.savefig("totals-chromium.svg", dpi=360)
plt.savefig("totals-chromium.pdf", dpi=360, transparent=True)

# Total lines of patched code

df = pd.read_csv("patches.csv", quotechar="\"", quoting=csv.QUOTE_NONNUMERIC)
print(df)

matplotlib.rc('ytick', labelsize=8)
fig, ax = plt.subplots()
plt.grid(axis="y")
plt.ylim(-10**5, 10**5)
bar_colours = ["#e2e57dff", "#94ec95ff"]

categories = ["ESR 78", "ESR 91"]
df.sort_values(by="Name", key=lambda x: df["Name"].map(lambda x: list(names).index(x)), inplace=True)

versions = [df[df["Version"] == category] for category in categories]
bar_width = 1.0 / 2.0
multiplier = 0
for version in versions:
	x = np.arange(len(version))
	added = np.array(version["Added"])
	removed = np.array(-version["Removed"])
	names = np.array(version["Name"])
	offset = bar_width * multiplier
	rects = ax.bar(x + offset, added, bar_width * 0.8, label="{} added".format(categories[multiplier]), color=bar_colours_added[multiplier])
	rects = ax.bar(x + offset, removed, bar_width * 0.8, label="{} removed".format(categories[multiplier]), color=bar_colours_removed[multiplier])
	multiplier += 1

fig.subplots_adjust(bottom=0.2, wspace=0.2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.set_axisbelow(True)
ax.set_xticks(x + 0.5 * bar_width, names)
ax.set_ylabel("Lines of code (log scale)")


ax.set_title("Gecko patch changes by language")
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
ax.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, -0.1), handlelength=1, handleheight=1, fancybox=False, shadow=False, frameon=False, edgecolor="#ffffff00")
plt.yscale("symlog")

plt.savefig("patches.png", dpi=360)
plt.savefig("patches.svg", dpi=360)
plt.savefig("patches.pdf", dpi=360, transparent=True)

