#!/bin/bash

python _nx_parallel/update_get_info.py
pip install black ruff
black _nx_parallel/__init__.py
ruff format _nx_parallel/__init__.py
