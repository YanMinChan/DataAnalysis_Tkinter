SUBMIT_FOLDER	=	f21sc_cw2_yc89_xm3001

CLEAN_THIS	=	./dist					\
				./build					\
				./src/__pycache__		\
				./$(SUBMIT_FOLDER)		\
				./$(SUBMIT_FOLDER).zip	\
				$(wildcard ./samples/*.pkl)

CP_THIS		=	./src				\
				./cw2				\
				./.python-version	\
				./pyproject.toml	\
				./README.md			\
				./samples			\
				./requirements.txt	\
				./Report.pdf


submit: clean bundle
	rm -rf ./$(SUBMIT_FOLDER) $(SUBMIT_FOLDER).zip
	mkdir $(SUBMIT_FOLDER)
	cp -r $(CP_THIS) ./$(SUBMIT_FOLDER)
	zip -9 -r $(SUBMIT_FOLDER).zip $(SUBMIT_FOLDER)

bundle:
	uv run ./scripts/bundle.sh
	mv f21sccw2 cw2

clean:
	rm -rf $(CLEAN_THIS)
