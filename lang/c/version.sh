#!/bin/sh
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

# This script is used to generate version numbers for autotools
#
# The top-level main version is collected from the top-level build.xml
#
# The information for libtool is maintained manually since
# the public API for the C library can change independent of the project
#
# Do each of these steps in order and libtool will do the right thing
# (1) If there are changes to libavro:
#         libavro_micro_version++
#         libavro_interface_age++
#         libavro_binary_age++
# (2) If any functions have been added:
#         libavro_interface_age = 0
# (3) If backwards compatibility has been broken:
#         libavro_binary_age = 0
#         libavro_interface_age = 0
#
libavro_micro_version=23
libavro_interface_age=0
libavro_binary_age=0

# IGNORE EVERYTHING ELSE FROM HERE DOWN.........
if [ $# != 1 ]; then
  echo "USAGE: $0 CMD"
  echo "  where CMD is one of: project, libtool, libcurrent, librevision, libage"
  exit 1
fi

# https://www.sourceware.org/autobook/autobook/autobook_91.html
# 'Current' is the most recent interface number that this library implements
libcurrent=$(( libavro_micro_version - libavro_interface_age ))
# The implementation number of the 'current' interface
librevision=$libavro_interface_age
# The difference between the newest and oldest interfaces that this library implements
# In other words, the library implements all the interface numbers in the range from
# number 'current - age' to current
libage=$(( libavro_binary_age - libavro_interface_age ))

case "$1" in
  project)
    project_ver="undef"
    if [ -f VERSION.txt ]; then
      version_file=VERSION.txt
    elif [ -f ../../share/VERSION.txt ]; then
      version_file=../../share/VERSION.txt
    else
      echo 'VERSION.txt not found' >&2
    fi
    read -r project_ver < "$version_file"
    printf "%s" "$project_ver"
    ;;
  libtool)
    # useful for the -version-info flag for libtool
    printf "%d:%d:%d" $libcurrent $librevision $libage
    ;;
  libcurrent)
    printf "%d" "$libcurrent"
    ;;
  librevision)
    printf "%d" "$librevision"
    ;;
  libage)
    printf "%d" "$libage"
    ;;
esac
