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

usage() {
  echo "Usage: $0 {clean|dist|interop-data-generate|interop-data-test|lint|test}"
  exit 1
}

clean() {
  git clean -xdf '*.avpr' \
                 '*.avsc' \
                 '*.egg-info' \
                 '*.py[co]' \
                 'VERSION.txt' \
                 '__pycache__' \
                 'avro/test/interop' \
                 'dist' \
                 'userlogs'
}

dist() {
  ./setup.py dist
}

interop_data_generate() {
  ./setup.py generate_interop_data
  cp -r avro/test/interop/data ../../build/interop
}

interop_data_test() {
  mkdir -p avro/test/interop ../../build/interop/data
  cp -r ../../build/interop/data avro/test/interop
  python -m unittest avro.test.test_datafile_interop
}

lint() {
  ./setup.py isort lint
}

test_() {
  tox
}

main() {
  [ "$1" ] || usage
  for target; do
    case "$target" in
      clean) clean;;
      dist) dist;;
      interop-data-generate) interop_data_generate;;
      interop-data-test) interop_data_test;;
      lint) lint;;
      test) test_;;
      *) usage;;
    esac
  done
}

main "$@"
