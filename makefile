all: techtalk-gecko-dev.pdf notes.pdf

slides.aux: slides.tex slides.bib
	xelatex slides.tex

#slides.bbl: slides.aux
#	bibtex slides.aux

slides.pdf: slides.tex macros.tex graphics/gantt.pdf graphics/internals.pdf graphics/blocks.pdf code-examples/*.*
	xelatex slides.tex
	xelatex slides.tex

graphics/gantt.pdf: resources/gantt.svg
	inkscape resources/gantt.svg -o graphics/gantt.pdf

graphics/internals.pdf: resources/internals.svg
	inkscape resources/internals.svg -o graphics/internals.pdf

graphics/blocks.pdf: resources/blocks.svg
	inkscape resources/blocks.svg -o graphics/blocks.pdf

resources/gantt.svg: resources/make-gantt.py resources/browsers.json
	cd ${PWD}/resources && python3 make-gantt.py browsers.json

resources/internals.svg: resources/make-blocks.py resources/internals.json
	cd ${PWD}/resources && python3 make-blocks.py internals.json

resources/blocks.svg: resources/make-blocks.py resources/blocks.json
	cd ${PWD}/resources && python3 make-blocks.py blocks.json

techtalk-gecko-dev.pdf: slides.pdf
	cp slides.pdf techtalk-gecko-dev.pdf

notes.aux: notes.tex slides.bib
	xelatex notes.tex

notes.pdf: notes.tex macros.tex
	xelatex notes.tex
	xelatex notes.tex

clean:
	rm -f *.blg *.log *.pdf *.bbl *.aux *.out *.nav *.snm *.toc *.vrb && \
	rm -f resources/internals.svg resources/gantt.svg resources/blocks.svg && \
	rm -f resources/internals.png resources/gantt.png resources/blocks.png && \
	rm -f graphics/internals.pdf graphics/gantt.pdf graphics/blocks.pdf

