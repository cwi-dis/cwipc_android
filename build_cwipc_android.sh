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

echo "Copying compiled artifacts..."
conan list 'cwipc#:*' |sed 's/ //g' > package_info.txt

package_name=`cat package_info.txt |head -n3 |tail -n1`
revision_id=`cat package_info.txt |head -n5 |tail -n1 |sed 's/(.*)//'`
package_id=`cat package_info.txt |head -n7 |tail -n1`

package_folder=`conan cache path ${package_name}#${revision_id}:${package_id}`

if [ -d "dist/${ARCH}" ]; then
    echo "Deleting outdated dist directory..."
    rm -r dist/${ARCH}
fi

mkdir -p dist/${ARCH}/lib dist/${ARCH}/include
cp ${package_folder}/lib/*.so dist/${ARCH}/lib
cp -r ${package_folder}/include/* dist/${ARCH}/include

rm package_info.txt

echo "DONE!"
