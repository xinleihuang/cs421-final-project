init:
		python -m venv .venv
		chmod u+x .venv/bin/activate
		.venv/bin/activate
		pip install --upgrade pip
		pip install -r requirements.txt

run:
		python src/main.py

test:
		python -m unittest -v

performance:
		python -m src.performance.execution_time
