test: simple_anim.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py simple_anim.mdl

clean:
	rm anime/*
	touch anime/placeholder
	rm *pyc *out parsetab.py

clear:
	rm *pyc *out parsetab.py *ppm
