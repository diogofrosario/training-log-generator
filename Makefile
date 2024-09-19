.PHONY venv:
venv:
	python3 -m venv venv

.PHONY: setup
setup: 
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

.PHONY: run
run:
	python3 main.py
