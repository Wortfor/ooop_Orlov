.PHONY: run test lint clean

run:
	python -m src.main

test:
	pytest tests/ -v

lint:
	flake8 src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +