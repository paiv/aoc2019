#!/bin/bash
set -e

python3 -m venv .venv/aoc

. activate

pip install -U setuptools
pip install -U pip
pip install -r requirements.txt
