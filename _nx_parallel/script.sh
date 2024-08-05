#!/bin/bash

echo "inside script"
# Create a temporary virtual environment
python3 -m venv temp_env

# Activate the virtual environment
source temp_env/bin/activate 

pip install ruff==0.1.8

python3 _nx_parallel/update_get_info.py
echo "updated"
echo "pip list"
pip list
echo "ruff version:"
ruff --version
echo "which ruff:"
which ruff
ruff format "_nx_parallel/temp__init__.py" --verbose
echo "formatted"

# Check if there's any difference between the original file and the formatted one
if diff -q "_nx_parallel/__init__.py" "_nx_parallel/temp__init__.py" >/dev/null; then
    echo "no changes"
    rm "_nx_parallel/temp__init__.py"
    echo "temp removed"
else
    echo "changes"
    mv "_nx_parallel/temp__init__.py" "_nx_parallel/__init__.py"
    echo "moved"
fi

echo "done"

deactivate

rm -rf temp_env
