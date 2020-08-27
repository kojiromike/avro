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

import contextlib
import unittest
from typing import Generator, Optional

import avro.datafile
import avro.schema

@contextlib.contextmanager
def writer(path: str,
           schema: Optional[avro.schema.Schema],
           codec: str,
           mode: str) -> Generator[avro.datafile.DataFileWriter, None, None]:
    ...


@contextlib.contextmanager
def reader(path: str, mode: str) -> Generator[avro.datafile.DataFileReader, None, None]:
    ...


class TestDataFile(unittest.TestCase):
    def tempfile(self) -> str:
        ...

    def test_append(self) -> None:
        ...

    def test_round_trip(self) -> None:
        ...

    def test_context_manager(self) -> None:
        ...

    def test_metadata(self) -> None:
        ...

    def test_empty_datafile(self) -> None:
        ...
