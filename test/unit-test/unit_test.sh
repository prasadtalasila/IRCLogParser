#!/usr/bin/env bash
coverage run --source=. -m unittest discover -s test/unit-test
coverage report -m
codecov
bash ext/doc_auto_deploy.sh