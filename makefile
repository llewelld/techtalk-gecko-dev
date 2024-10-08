all: techtalk-gecko-dev.pdf

slides.aux: slides.tex slides.bib
	xelatex slides.tex

#slides.bbl: slides.aux
#	bibtex slides.aux

slides.pdf: slides.tex macros.tex graphics/gantt.pdf graphics/internals.pdf code-examples/*.*
	xelatex slides.tex
	xelatex slides.tex

graphics/gantt.pdf: resources/gantt.svg
	inkscape resources/gantt.svg -o graphics/gantt.pdf

graphics/internals.pdf: resources/internals.svg
	inkscape resources/internals.svg -o graphics/internals.pdf

resources/gantt.svg: resources/make-gantt.py resources/browsers.json
	cd ${PWD}/resources && python3 make-gantt.py

resources/internals.svg: resources/make-blocks.py resources/internals.json
	cd ${PWD}/resources && python3 make-blocks.py

techtalk-gecko-dev.pdf: slides.pdf
	cp slides.pdf techtalk-gecko-dev.pdf

clean:
	rm -f *.blg *.log *.pdf *.bbl *.aux *.out *.nav *.snm *.toc *.vrb

