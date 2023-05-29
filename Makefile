demo:
	python3 pytmac.py --demo

test:
	python3 -m pytest

lint:
	python3 -m pylint --fail-under=9.5 $$(find . -name "*.py" -not -path "./tests/*")

dev:
	pip3 uninstall pytmac -y
	pip3 install .

gen-docs:
	python3 ./scripts/generate_docs.py
	gendocs --config mkgendocs.yaml

mkdocs:
	make gen-docs
	mkdocs serve
