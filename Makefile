.PHONY: build clean publish test

build:
	python setup.py sdist bdist_wheel

clean:
	rm -fr rollback.egg-info dist build .eggs .tox .pytest_cache \
		coverage.xml .coverage
	find . -type d -name __pycache__ -exec /bin/rm -fr {} +
	find . -depth -type f -name '*.pyc' -exec /bin/rm -fr {} +

publish:
	twine upload dist/*

test:
	tox
