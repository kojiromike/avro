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

set -e

cd "${0%/*}"

dist_dir="../../dist/php"
build_dir="pkg"
read -r version < ../../share/VERSION.txt
libname="avro-php-$version"
lib_dir="$build_dir/$libname"
tarball="$libname.tar.bz2"

test_tmp_dir="test/tmp"

clean() {
  rm -rf "$test_tmp_dir" "$build_dir"
}

dist() {
  mkdir -p "$build_dir/$libname" "$lib_dir/examples"
  cp -pr lib "$lib_dir"
  cp -pr examples/*.php "$lib_dir/examples"
  cp README.txt LICENSE NOTICE "$lib_dir"
  cd "$build_dir"
  tar -cjf "$tarball" "$libname"
  mkdir -p "../$dist_dir"
  cp "$tarball" "../$dist_dir"
}

interop_data_generate() {
  php test/generate_interop_data.php
}

interop_data_test() {
  phpunit test/InterOpTest.php
}

lint() {
  echo 'This is a stub where someone can provide linting.'
}

test_() {
  phpunit -v test/AllTests.php

  # Check backward compatibility with PHP 5.x if both PHP 5.6 and PHPUnit 5.7 are installed.
  # TODO: remove this check when we drop PHP 5.x support in the future
  if command -v php5.6 > /dev/null && phpunit --version | grep -q 'PHPUnit 5.7'; then
    echo 'Checking backward compatibility with PHP 5.x'
    php5.6 "$(command -v phpunit)" -v test/AllTests.php
  fi
}

usage() {
  echo "Usage: $0 {interop-data-generate|test-interop|lint|test|dist|clean}" >&2
  exit 1
}

main() {
  for target; do
    case "$target" in
      interop-data-generate) interop_data_generate;;
      interop-data-test|test-interop) interop_data_test;;
      lint) lint;;
      test) test_;;
      dist) dist;;
      clean) clean;;
      *) usage;;
    esac
  done
}

main "$@"
