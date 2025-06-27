#!/usr/bin/bash
# Before running this script, you need to `mamba install swig`.
# The -nogil flags requires swig 4.4.0 or later.

set -o errexit
cd "$(dirname "$0")"
swig -c++ -python -nogil -I../src src/sentencepiece/sentencepiece.i
