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
	yarn

.PHONY: words
words:
	cd scripts && python ./create_words.py

.PHONY: http
http:
	python -m backend

.PHONY: browse
browse:
	./node_modules/.bin/electron browse.js

.PHONY: backend
backend:
	pyinstaller --distpath ./backend_dist --workpath ./backend_build backend.spec
	rm -rf backend_build

.PHONY: app
app:
	yarn start
