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

"""Test the schema parsing logic."""

import json
import unittest
import warnings
from typing import Callable, Collection, Dict, List, Optional

import avro.errors
import avro.schema

class TestSchema:
    def __init__(self, data: str, name: str='', comment: str='', warnings: Optional[str]=None) -> None:
        ...

    def parse(self) -> avro.schema.Schema:
        ...

    def __str__(self) -> str:
        ...


class TestMisc(unittest.TestCase):
    def test_correct_recursive_extraction(self) -> None:
        ...

    def test_name_is_none(self) -> None:
        ...

    def test_name_not_empty_string(self) -> None:
        ...

    def test_name_space_specified(self) -> None:
        ...

    def test_fullname_space_specified(self) -> None:
        ...

    def test_name_default_specified(self) -> None:
        ...

    def test_fullname_default_specified(self) -> None:
        ...

    def test_fullname_space_default_specified(self) -> None:
        ...

    def test_name_space_default_specified(self) -> None:
        ...
    def test_equal_names(self) -> None:
        ...
    def test_invalid_name(self) -> None:
        ...
    def test_null_namespace(self) -> None:
        ...
    def test_exception_is_not_swallowed_on_parse_error(self) -> None:
        ...
    def test_decimal_valid_type(self) -> None:
        ...

    def test_fixed_decimal_valid_max_precision(self) -> None:
        ...

    def test_fixed_decimal_invalid_max_precision(self) -> None:
        ...

    def test_parse_invalid_symbol(self) -> None:
        ...

class SchemaParseTestCase(unittest.TestCase):
    def __init__(self, test_schema: TestSchema) -> None:
        ...

    def parse_valid(self) -> None:
        ...

    def parse_invalid(self) -> None:
        ...

class RoundTripParseTestCase(unittest.TestCase):
    def __init__(self, test_schema: TestSchema) -> None:
        ...

    def parse_round_trip(self) -> None:
        ...


class DocAttributesTestCase(unittest.TestCase):
    def __init__(self, test_schema: TestSchema) -> None:
        ...

    def check_doc_attributes(self) -> None:
        ...

class OtherAttributesTestCase(unittest.TestCase):
    def __init__(self, test_schema: TestSchema) -> None:
        ...

    def _check_props(self, props: Dict[str, str]) -> None:
        ...

    def check_attributes(self) -> None:
        ...


def load_tests(loader: unittest.TestLoader, default_tests: Collection[Callable[[], None]], pattern: Optional[str]) -> unittest.TestSuite:
    ...
