#!/usr/bin/env python3
# -*- mode: python -*-
# -*- coding: utf-8 -*-

##
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from typing import Dict, Generator, Mapping, Sequence, Union

def looney_records() -> Generator[Dict[str, str], None, None]:
    ...


def gen_avro(filename: str) -> None:
    ...


def _tempfile() -> str:
    ...


class TestCat(unittest.TestCase):
    avro_file = None  # type: str

    def _run(self, *args: str) -> Union[str, Sequence[str]]:
        ...

    def test_print(self) -> None:
        ...

    def test_filter(self) -> None:
        ...

    def test_skip(self) -> None:
        ...

    def test_csv(self) -> None:
        ...


    def test_csv_header(self) -> None:
        ...

    def test_print_schema(self) -> None:
        ...

    def test_help(self) -> None:
        ...

    def test_json_pretty(self) -> None:
        ...

    def test_version(self) -> None:
        ...

    def test_files(self) -> None:
        ...

    def test_fields(self) -> None:
        ...


class TestWrite(unittest.TestCase):
    def _run(self, *args: str, **kw: str) -> None:
        ...

    def load_avro(self, filename: str) -> None:
        ...

    def test_version(self) -> None:
        ...

    def format_check(self, format: str, filename: str) -> None:
        ...

    def test_write_json(self) -> None:
        ...

    def test_write_csv(self) -> None:
        ...

    def test_outfile(self) -> None:
        ...

    def test_multi_file(self) -> None:
        ...

    def test_stdin(self) -> None:
        ...
