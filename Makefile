build:
	python setup.py zip
	python setup.py bdist_wheel --universal

upload:
	twine upload dist/*

clean:
	rm -rf *.egg-info templates/*.zip build dist