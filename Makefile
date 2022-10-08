clear:
	@rm -rf build dist *.egg-info

dist: clear
	@python setup.py bdist_wheel

