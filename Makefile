# YOU NEED TO SET THE FOLLOWING VARIABLES!

KINDLEGEN=./kindlegen

DICTIONARY_NAME='Custom German Dictionary'
DICTIONARY_AUTHOR='Anonymous'
DICTIONARY_LANG=de
DICTIONARY_IN_LANG=de
DICTIONARY_OUT_LANG=en

COPYRIGHT_REMARK='Copyleft'

#COVER_IMG='cover.jpg'

INPUT_FILE=input.csv
INPUT_TYPE=default_tsv



# Other variables -- no need to touch unless you know what you are doing
PY=python3
INPUT_TO_CONTENT=input2content.py
GEN_BOILERPLATE=generate_boilerplate.py
GEN_OPF=generate_opf.py


.PHONY: $(INPUT_TYPE)


dict.mobi: dict.opf
	$(KINDLEGEN) dict.opf

dict.opf: content.html cover.html copyright.html usage.html
	$(PY) $(GEN_OPF) $(DICTIONARY_NAME) $(DICTIONARY_AUTHOR) $(DICTIONARY_LANG) $(DICTIONARY_IN_LANG) $(DICTIONARY_OUT_LANG)

usage.html copyright.html cover.html:
	$(PY) $(GEN_BOILERPLATE) $(DICTIONARY_NAME) $(DICTIONARY_AUTHOR) $(COPYRIGHT_REMARK)

content.html: $(INPUT_TYPE) $(INPUT_FILE)
	$(PY) $(INPUT_TO_CONTENT) --format=$^

clean:
	rm content.html cover.html usage.html copyright.html dict.opf