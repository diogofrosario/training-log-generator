.PHONY venv:
venv:
	python3 -m venv venv

.PHONY: setup
setup: 
	poetry install

.PHONY: run
run:
	poetry run python3 main.py

.PHONY: run-cli
run-cli:
	poetry run python3 src/training_log_generator/cli.py

.PHONY: run-app
run-app:
	poetry run streamlit run src/training_log_generator/app.py
