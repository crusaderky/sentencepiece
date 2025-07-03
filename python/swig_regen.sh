#!/usr/bin/bash
# Before running this script, you need to `mamba install swig`.

set -o errexit
cd "$(dirname "$0")"
swig -c++ -python -threads -I../src src/sentencepiece/sentencepiece.i
