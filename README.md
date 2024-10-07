# Tech Talk: Anatomy of a Browser - Embedded Mobile Lizards

[![LaTeX build](../../actions/workflows/pdflatex.yml/badge.svg)](../../actions/workflows/pdflatex.yml)
[![Slides](https://img.shields.io/badge/PDF-Slides-orange.svg?style=flat)](../gh-action-result/pdf-output/techtalk-gecko-dev.pdf)

The Alan Turing Institute Tech Talk series

19/11/2024

## Details

This folder contains slides for the "Anatomy of a Browser - Embedded Mobile Lizards" presentation to be given as a Tech Talk at The Alan Turing Institute.

## Schedule

Tuesday 19th November 2024, 12:30 -- 13:30 GMT

50 minutes talk, 5 minutes question

## Abstract

TBC

Links:
1. [Daily dev diary](https://www.flypig.co.uk/gecko)
2. [EmbedLite source](https://github.com/llewelld/gecko-dev)
3. [Sailfish Browser source and issue tracking](https://github.com/sailfishos/sailfish-browser)

## Prebuilt slides

Slides built from the latest successfully built push to the repository are available in the [pdf-output branch](../gh-action-result/pdf-output/techtalk-gecko-dev.pdf).

## Building the presentation into a PDF

Requirements:

1. Beamer packages
2. xelatex
3. Source Sans Pro font family:
   https://fonts.google.com/specimen/Source+Sans+Pro
4. Inkscape

In order to generate the graphics you'll need to create and activate a Python virtual environment:
```
pushd resources
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
popd
```

Build the PDF output using the included makefile:
```
make
```

The final output can be found as `techtalk-gecko-dev.pdf`.

To clean out the intermediary build files and output files:
```
make clean
```

