#!/usr/bin/env bash
set -ex
coverage run --source=. -m unittest discover -s test/integration-test
coverage report -m
codeclimate-test-reporter --file .coverage --token $CODECLIMATE_REPO_TOKEN
