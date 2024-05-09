#!/bin/bash

python _nx_parallel/update_get_info.py
black _nx_parallel/__init__.py
ruff format _nx_parallel/__init__.py
git add _nx_parallel/__init__.py
