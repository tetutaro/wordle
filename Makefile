.PHONY: clean
clean: clean-build clean-pyc clean-test

.PHONY: clean-build
clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf backend_build/
	rm -rf backend_dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

.PHONY: clean-test
clean-test:
	rm -f .coverage
	rm -rf htmlcov/

.PHONY: environ
environ:
	pip install -r requirements.txt

.PHONY: words
words:
	cd wordle && python ./create_words.py

.PHONY: local
local:
	python -m wordle

.PHONY: binary
binary:
	pyinstaller wordle.spec
	rm -rf build

.PHONY: binary-mac
binary-mac:
	pyinstaller wordle_mac.spec
	rm -rf build
