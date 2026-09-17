RA-L DOUBLE-ANONYMOUS LATEX PROJECT
========================================

Main source file: root.tex
Document class:    ieeeconf.cls (official RAS/PaperCept package)
Bibliography:      references.bib with IEEEtran.bst
Figures:           pictures/

Compile sequence:
  pdflatex root.tex
  bibtex root
  pdflatex root.tex
  pdflatex root.tex

Double-anonymous preparation:
- Author names, affiliations, funding acknowledgments, corresponding-author
  information, running headers, biographies, and publication identifiers are
  not included in root.tex.
- The PDF Author metadata is explicitly empty.
- Plot PDFs that contained Type 3 fonts were converted to high-resolution PNG
  files so the compiled manuscript does not inherit prohibited Type 3 fonts.

Before submission, run the RA-L/PaperCept online PDF compliance test and check
all optional multimedia or supplementary files separately for identifying
information.
