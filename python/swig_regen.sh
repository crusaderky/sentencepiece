#!/usr/bin/bash
# Before running this script, you need to `mamba install swig`.

set -o errexit
cd "$(dirname "$0")"
swig -c++ -python -I../src src/sentencepiece/sentencepiece.i
mv src/sentencepiece/sentencepiece.py src/sentencepiece/__init__.py
