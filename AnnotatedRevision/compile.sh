#!/bin/bash
#pdflatex -synctex=1 -interaction=nonstopmode dissertation.tex
#bibtex ch1/ch1.aux
#bibtex ch2/ch2.aux
#bibtex ch3/ch3.aux
#bibtex ch4/ch4.aux
#bibtex ch5/ch5.aux
#bibtex ch6/ch6.aux
#pdflatex -synctex=1 -interaction=nonstopmode dissertation.tex

pdflatex -synctex=1 -interaction=nonstopmode diff.tex
bibtex diff.aux
pdflatex -synctex=1 -interaction=nonstopmode diff.tex
pdflatex -synctex=1 -interaction=nonstopmode diff.tex
