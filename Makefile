# convenience Makefile to run validation tests
# src: source path discovered in run time
# minimum_test_coverage: minimun test coverage allowed
# pep8_ignore: ignore listed PEP 8 errors and warnings
# max_complexity: maximum McCabe complexity allowed
# csslint_ignore: skip file names matching find pattern (use ! -name PATTERN)
# jshint_ignore: skip file names matching find pattern (use ! -name PATTERN)

SHELL = /bin/sh

src = `find . -type d | grep -m 1 "src/sc/contentrules/group"`
minimum_test_coverage = 80
pep8_ignore = E501
max_complexity = 12
csslint_ignore = ! -name jquery\*
jshint_ignore = ! -name jquery\*

python-validation:
	bin/flake8 --ignore=$(pep8_ignore) --max-complexity=$(max_complexity) $(src)

css-validation:
	npm install csslint -g 2>/dev/null
	find $(src) -type f -name *.css $(csslint_ignore) | xargs csslint

js-validation:
	npm install jshint -g 2>/dev/null
	find $(src) -type f -name *.js $(jshint_ignore) -exec jshint {} ';'

coverage-validation:
	bin/coverage.sh $(minimum_test_coverage)
