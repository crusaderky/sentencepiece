#!/usr/bin/bash
# Before running this script, you need to `pip install grpcio-tools`.

set -o errexit
set -x
cd "$(dirname "$0")"/..
OUT=python/src/sentencepiece
python -m grpc_tools.protoc \
    --proto_path=src \
    --pyi_out=$OUT \
    --python_out=$OUT \
    src/*.proto
