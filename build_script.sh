#!/usr/bin/env bash

if [ -d "dist" ]; then
    rm dist/*
fi

python3 setup.py bdist_wheel && twine upload dist/*
