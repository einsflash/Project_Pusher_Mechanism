report.pdf: report.tex literature.bib 
	pdflatex $<
	bibtex $(basename $<)
	pdflatex $<
	pdflatex $<

clean: 
	rm -f *.toc *.aux *.ps *.log *.lof *.bbl *.blg *.dvi *.pdf

.PHONY: clean
