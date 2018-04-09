#!/usr/bin/env bash
coverage run --source=. -m unittest discover -s test/functional-test
coverage report -m
codecov -F functional
coveralls
