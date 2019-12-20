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
  echo "Usage: $0 {lint|test|dist|clean|interop-data-generate|interop-data-test}"
  exit 1
}

[ "$#" -gt 0 ] || usage


clean() {
  [ -f Makefile ] && make clean
  rm -rf Avro-*.tar.gz META.yml Makefile.old lang/perl/inc/
}

lint() {
  failures=0
  for i in $(find lib t xt -name '*.p[lm]' -or -name '*.t'); do
    perlcritic --verbose 1 "$i" || failures=$(( failures + 1 ))
  done
  if [ ${failures} -gt 0 ]; then
    return 1
  fi
}

test_() {
  perl ./Makefile.PL && make test
}

dist() {
  perl ./Makefile.PL && make dist
}

interop_data_generate() {
  perl -Ilib share/interop-data-generate
}

interop_data_test() {
  prove -Ilib xt/interop.t
}

main() {
  for target; do
    case "$target" in
      lint) lint;;
      test) test_;;
      dist) dist;;
      clean) clean;;
      interop-data-generate) interop_data_generate;;
      interop-data-test) interop_data_test;;
      *) usage;;
    esac
  done
}

main "$@"
