#!/bin/bash

pdflatex -synctex=1 -interaction=nonstopmode hines_hetland_2017_gji.tex
bibtex hines_hetland_2017_gji.aux
pdflatex -synctex=1 -interaction=nonstopmode hines_hetland_2017_gji.tex
pdflatex -synctex=1 -interaction=nonstopmode hines_hetland_2017_gji.tex
