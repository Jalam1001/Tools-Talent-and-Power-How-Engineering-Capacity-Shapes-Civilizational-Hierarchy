# Build the monograph PDF and the GitHub Pages site.
# Intermediate LaTeX files stay in paper/; official artifacts are copied to the
# repository root and to docs/.

.PHONY: all pdf site clean

all: pdf site

pdf:
	cd paper && latexmk -pdf -interaction=nonstopmode main.tex
	cp paper/main.pdf The-Oldest-Law-of-Power-v0.2.pdf
	mkdir -p docs
	cp The-Oldest-Law-of-Power-v0.2.pdf docs/The-Oldest-Law-of-Power-v0.2.pdf

figures:
	cd paper/figures && \
	for f in fig1-niche fig2-chain fig3-pyramid fig4-layers fig5-sovereignty; do \
		pdflatex -interaction=nonstopmode $$f.tex; \
		pdf2svg $$f.pdf $$f.svg; \
	done

site: pdf
	pandoc paper/main.tex -o /tmp/essay-raw.html \
		--bibliography=paper/references.bib --citeproc \
		--standalone --from=latex --to=html5
	python3 scripts/build_site.py

clean:
	cd paper && latexmk -C
	rm -f paper/figures/*.aux paper/figures/*.log
