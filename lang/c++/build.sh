#!/bin/sh

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e # exit on error

usage() {
  echo "Usage: $0 {lint|test|dist|clean|install|doc}"
  exit 1
}

[ $# -gt 0 ] || usage

if [ -s VERSION.txt ]; then
  read -r VERSION < VERSION.txt
else
  read -r VERSION < ../../share/VERSION.txt
fi

BUILD=../../build
AVRO_CPP=avro-cpp-$VERSION
AVRO_DOC=avro-doc-$VERSION
BUILD_DIR=../../build
BUILD_CPP=$BUILD/$AVRO_CPP
DIST_DIR=../../dist/$AVRO_CPP
DOC_CPP=$BUILD/$AVRO_DOC/api/cpp
DIST_DIR=../../dist/cpp
TARFILE=../dist/cpp/$AVRO_CPP.tar.gz

do_doc() {
  doxygen
  [ -d doc ] || exit
  mkdir -p "$DOC_CPP"
  cp -R doc/* "$DOC_CPP"
}

do_dist() {
  rm -rf "${BUILD_CPP:?}/"
  mkdir -p "$BUILD_CPP"
  cp -r api AUTHORS build.sh CMakeLists.txt ChangeLog LICENSE NOTICE impl \
            jsonschemas NEWS parser README scripts test examples ../../share/VERSION.txt \
            "$BUILD_CPP"
  find "$BUILD_CPP" -name '.svn' -exec rm -rf {} +
  mkdir -p $DIST_DIR
  (cd "$BUILD_DIR" && tar cvzf "$TARFILE" "$AVRO_CPP" && cp "$TARFILE" "$AVRO_CPP")
  [ -f "$DIST_FILE" ] || exit
}

lint() {
  echo 'This is a stub where someone can provide linting.'
}
test_() {
  (
    cd build
    cmake -G "Unix Makefiles" -D CMAKE_BUILD_TYPE=Debug -D AVRO_ADD_PROTECTOR_FLAGS=1 ..
    make
  )
  ./build/buffertest
  ./build/unittest
  ./build/CodecTests
  ./build/CompilerTests
  ./build/StreamTests
  ./build/SpecificTests
  ./build/AvrogencppTests
  ./build/DataFileTests
  ./build/SchemaTests
}

xcode_test() {
  mkdir -p build.xcode
  (
    cd build.xcode
    cmake -G Xcode ..
    xcodebuild -configuration Release
    ctest -C Release
  )
}

dist() {
  (
    cd build
    cmake -G "Unix Makefiles" -D CMAKE_BUILD_TYPE=Release ..
  )
  do_dist
  do_doc
}

clean() {
  (
    cd build
    make clean
  )
  rm -rf doc test.avro test?.df test_skip.df
}

install() {
  (
    cd build
    cmake -G "Unix Makefiles" -D CMAKE_BUILD_TYPE=Release ..
    make install
  )
}

main() {
  (mkdir -p build; cd build; cmake -G "Unix Makefiles" ..)
  for target; do
    case "$target" in
      lint) lint;;
      test) test_;;
      xcode-test) xcode_test;;
      dist) dist;;
      doc) do_doc;;
      clean) clean;;
      install) install;;
      *) usage;;
    esac
  done
}

main "$@"
