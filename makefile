sections = $(wildcard sections/*.tex)
deps = notes.sty
cc = latexmk
flags = -outdir=build -pdf

build/main.pdf : main.tex $(sections) $(deps)
	$(cc) $(flags) $<
