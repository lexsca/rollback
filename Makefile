.PHONY: build clean publish test

build:
	python -m build --wheel --sdist --outdir dist .

clean:
	rm -fr *.egg-info dist build .tox .pytest_cache
	find . -type d -name __pycache__ -exec /bin/rm -fr {} +

publish:
	twine check --strict dist/*
	twine upload --verbose dist/*

test:
	tox
