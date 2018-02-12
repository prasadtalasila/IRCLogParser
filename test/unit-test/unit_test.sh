#!/usr/bin/env bash
coverage run --source=. -m unittest discover -s .
coverage report -m
codecov