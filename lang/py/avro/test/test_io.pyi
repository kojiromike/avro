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
from typing import BinaryIO, Optional

import avro.io
import avro.schema

def avro_hexlify(reader: avro.io.DatumReader) -> bytes:
    ...

def write_datum(datum: avro.types.AvroAny, writers_schema: avro.schema.Schema) -> None:
    ...

def read_datum(buffer: BinaryIO, writers_schema: avro.schema.Schema, readers_schema: Optional[avro.schema.Schema]=None) -> avro.types.AvroAny:
    ...

def check_binary_encoding(number_type: int) -> int:
    ...

def check_skip_number(number_type: int) -> int:
    ...


class TestIO(unittest.TestCase):
    def test_validate(self) -> None:
        ...

    def test_round_trip(self) -> None:
        ...

    def test_binary_int_encoding(self) -> None:
        ...

    def test_binary_long_encoding(self) -> None:
        ...

    def test_skip_int(self) -> None:
        ...

    def test_skip_long(self) -> None:
        ...

    def test_schema_promotion(self) -> None:
        ...

    def test_unknown_symbol(self) -> None:
        ...

    def test_default_value(self) -> None:
        ...

    def test_no_default_value(self) -> None:
        ...

    def test_projection(self) -> None:
        ...

    def test_field_order(self) -> None:
        ...

    def test_type_exception(self) -> None:
        ...
