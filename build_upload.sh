#!/bin/bash
rm -rf dist/
python3 setup.py bdist_wheel sdist
twine upload dist/*
