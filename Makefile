.PHONY venv:
venv:
	python3 -m venv venv

.PHONY: setup
setup: 
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

.PHONY: run
run:
	python3 main.py

.PHONY: run-cli
run-cli:
	python3 src/training_log_generator/cli.py

.PHONY: run-app
run-app:
	streamlit run src/training_log_generator/app.py
