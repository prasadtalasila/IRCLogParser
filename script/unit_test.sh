#!/usr/bin/env bash
set -ex
coverage run --source=. -m unittest discover -s test/unit-test
coverage report -m
codecov -F unit
bash ext/doc_auto_deploy.sh
bash script/call_graph.sh
