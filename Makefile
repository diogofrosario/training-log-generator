.PHONY setup:
setup: 
	. venv/bin/activate && pip install -r requirements.txt

.PHONY: run
run:
	python3 main.py