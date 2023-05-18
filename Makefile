pretty:
	black -t py311 .

build:
	rm -rf dist barvikron.egg-info
	python -m build
	# python -m twine upload --repository testpypi dist/*
	# twine upload dist/*
