#!/bin/bash

python _nx_parallel/update_get_info.py

ruff format "_nx_parallel/temp__init__.py"

# Check if there's any difference between the original file and the formatted one
if diff -q "_nx_parallel/__init__.py" "_nx_parallel/temp__init__.py" >/dev/null; then
    rm "_nx_parallel/temp__init__.py"
else
    mv "_nx_parallel/temp__init__.py" "_nx_parallel/__init__.py"
fi
