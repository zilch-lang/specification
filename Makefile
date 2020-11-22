PDF = magical-zilch-book.pdf
SRCS =                      \
	config.tex              \
	cover.tex               \
	index.tex               \
	part0-introduction.tex  \
	part1-zilch.tex         \
	part2-nstar.tex         \
	part3-stdlib.tex        \
	glossary.tex            \
	toc.tex                 \
	main.bib
MAIN = main.tex

TEXFLAGS =                        \
	-interaction=batchmode        \
	-latexoption=-shell-escape

all: $(PDF)

%.pdf: $(MAIN) $(SRCS)
	latexmk $(TEXFLAGS) -pdf $<
	@mv $(<:.tex=.pdf) $@

.PHONY: clean
clean: $(MAIN) $(SRCS)
	latexmk $(TEXFLAGS) -C $<
	-@rm -r _minted-main
	-@rm $(PDF)
	-@rm *.ptc *.run.xml *.bbl     # Clean latexmk left-overs
