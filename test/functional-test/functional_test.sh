#!/usr/bin/env bash
set -ex
coverage run --source=. -m unittest discover -s test/functional-test
coverage report -m
coveralls