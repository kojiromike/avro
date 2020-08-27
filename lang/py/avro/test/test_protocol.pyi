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

"""Test the protocol parsing logic."""

import unittest
from typing import Callable, Collection, Dict, Optional, Union

import avro.protocol

class TestProtocol:
    """A proxy for a protocol string that provides useful test metadata."""

    def __init__(self, data: Union[str, Dict[str, str]], name: str, comment: str) -> None:
        ...

    def parse(self) -> avro.protocol.Protocol:
        ...

    def __str__(self) -> str:
        ...



class TestMisc(unittest.TestCase):
    def test_inner_namespace_set(self) -> None:
        ...

    def test_inner_namespace_not_rendered(self) -> None:
        ...


class ProtocolParseTestCase(unittest.TestCase):
    """Enable generating parse test cases over all the valid and invalid example protocols."""

    def __init__(self, test_proto: avro.protocol.Protocol) -> None:
        ...

    def parse_valid(self) -> None:
        ...

    def parse_invalid(self) -> None:
        ...

class ErrorSchemaTestCase(unittest.TestCase):
    """Enable generating error schema test cases across all the valid test protocols."""

    def __init__(self, test_proto: TestProtocol) -> None:
        ...

    def check_error_schema_exists(self) -> None:
        ...


class RoundTripParseTestCase(unittest.TestCase):
    """Enable generating round-trip parse test cases over all the valid test protocols."""

    def __init__(self, test_proto: TestProtocol) -> None:
        ...

    def parse_round_trip(self) -> None:
        ...


def load_tests(loader: unittest.TestLoader,
               default_tests: Collection[Callable[[], None]],
               pattern: Optional[str]) -> unittest.TestSuite:
    ...
