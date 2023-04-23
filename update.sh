#!/usr/bin/env sh

set -eu
cd "$(dirname "$0")"

git submodule update --init --recursive
rm -r gpt4allj/lib
cp -r gptj.cpp/lib gpt4allj
