#!/usr/bin/env bash

set -euo pipefail
trap clean EXIT

clean() {
    rm -r dist *.egg-info || true
}

clean
python3 setup.py sdist
twine upload dist/*
