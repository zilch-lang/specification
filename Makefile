PDF = magical-zilch-book.pdf
SRCS =
MAIN = main.tex

TEXFLAGS =                        \
	-interaction=batchmode        \
	-latexoption=-shell-escape

all: $(PDF)

%.pdf: $(MAIN) $(SRCS)
	latexmk $(TEXFLAGS) -pdf $^
	@mv $(<:.tex=.pdf) $@

.PHONY: clean
clean: $(MAIN) $(SRCS)
	latexmk $(TEXFLAGS) -C $^
	@rm $(PDF)
