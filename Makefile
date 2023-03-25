generate:
	python3 main.py
	plantuml -tsvg reports/report-$$(date +%F).md
