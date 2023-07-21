#!/bin/bash

set -e

if [ $# -lt 1 ]; then
  echo "USAGE: $0 armv7|armv8|x86|x86_64"
  exit 1
fi

ARCH=${1}

echo "Building libjepg-turbo..."
conan create conanfiles/libjpeg-turbo --profile android -s arch=$ARCH --build=missing

echo "Building cwipc..."
conan create conanfiles/cwipc --profile android -s arch=$ARCH --build=missing
