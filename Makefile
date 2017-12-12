VERSION=$(shell python3 -c "import pygmsh; print(pygmsh.__version__)")

default:
	@echo "\"make publish\"?"

README.rst: README.md
	cat README.md | sed -e 's_<img src="\([^"]*\)" width="\([^"]*\)">_![](\1){width="\2"}_g' -e 's_<p[^>]*>__g' -e 's_</p>__g' > /tmp/README.md
	pandoc /tmp/README.md -o README.rst
	sed -i 's/python,test/python/g' README.rst
	python3 setup.py check -r -s || exit 1

upload: setup.py README.rst
	rm -f dist/*
	python3 setup.py bdist_wheel --universal
	gpg --detach-sign -a dist/*
	twine upload dist/*

tag:
	# Make sure we're on the master branch
	ifneq "$(shell git rev-parse --abbrev-ref HEAD)" "master"
	$(error Not on master branch)
	endif
	@echo "Tagging v$(VERSION)..."
	git tag v$(VERSION)
	git push --tags

publish: tag upload

clean:
	rm -f README.rst
