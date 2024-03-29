PDF = magical-zilch-book.pdf
SRCS =                      \
	namespaces.tex            \
	config.tex              	\
	cover.tex               	\
	index.tex               	\
	part0-introduction.tex  	\
	part1-zilch.tex         	\
	part2-nstar.tex         	\
	part3-stdlib.tex        	\
	toc.tex                 	\
	preamble.tex              \
	main.bib
MAIN = main.tex

TEXFLAGS =                        \
	-interaction=batchmode        	\
	-latexoption=-shell-escape    	\
	-jobname="magical-zilch-book" 	\
	-use-make-

all: $(PDF)

rebuild: clean $(PDF)

book: $(PDF)
	latexmk -interaction=batchmode -jobname="book" -pdf book.tex

%.pdf: $(MAIN) $(SRCS)
	latexmk $(TEXFLAGS) -pdf $<

.PHONY: clean
clean: $(MAIN) $(SRCS)
	latexmk $(TEXFLAGS) -C $<
	-@rm -r _minted-*
	-@rm $(PDF)
# Clean latexmk left-overs
	-@rm *.ptc *.run.xml *.bbl *.aux *.bcf *.blg *.fdb_latexmk *.fls *.glg *.glo *.gls *.ist *.log *.out *.toc *.lol *.lof *.lot
