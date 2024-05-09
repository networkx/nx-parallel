#!/bin/bash

python _nx_parallel/update_get_info.py

# Check if the __init__.py file has been modified
if [[ $(git status --porcelain _nx_parallel/__init__.py) ]]; then
    black _nx_parallel/__init__.py
    ruff format _nx_parallel/__init__.py
    git add _nx_parallel/__init__.py
fi
