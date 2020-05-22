test:
	@coverage run manage.py test --no-input

coverage:
	@coverage report -m

lint:
	@pylint drafthub --fail-under=5

doc:
	@make -C docs/ html SPHINXOPTS="--keep-going -q"


