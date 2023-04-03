generate:
	python3 main.py
	plantuml -tsvg reports/report-$$(date +%F).md

test:
	python3 -m pytest

lint:
	python3 -m pylint --fail-under=9.5 $$(find . -name "*.py" -not -path "./tests/*")
