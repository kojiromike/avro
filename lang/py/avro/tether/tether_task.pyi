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
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import collections
from typing import Any, Dict, Optional, Sequence, Union, cast

import avro.protocol
import avro.schema
import avro.tether.tether_task

TaskTypeType = collections.namedtuple("TaskType", ("MAP", "REDUCE"))
TaskType = TaskTypeType(MAP=None, REDUCE=None)
inputProtocol = cast(avro.protocol.Protocol, None)
outputProtocol = cast(avro.protocol.Protocol, None)


class Collector:

    def __init__(self,
                 scheme: Union[str, avro.schema.Schema],
                 outputClient: str) -> None:
        ...

    def collect(self, record: Dict[str, str], partition: Optional[str]) -> None:
        ...


def keys_are_equal(rec1: Dict[str, Any], rec2: Dict[str, Any], fkeys: Sequence[str]) -> bool:
    ...


class HTTPRequestor:
    def __init__(self, server: str, port: int, protocol: avro.protocol.Protocol) -> None:
        ...

    def request(self, message_name: str, request_datum: avro.types.AvroAny) -> avro.types.AvroAny:
        ...


class TetherTask(abc.ABC):
    inschema = None  # type: avro.schema.Schema
    midschema = None  # type: avro.schema.Schema
    outschema = None  # type: avro.schema.Schema

    def __init__(self,
                 inschema: str,
                 midschema: str,
                 outschema: str) -> None:
        ...

    def open(self, inputport: int, clientPort: Optional[int]) -> None:
        ...

    def configure(self,
                  taskType: TaskTypeType,
                  inSchemaText: str,
                  outSchemaText: str) -> None:
        ...

    def input(self, data: bytes, count: int) -> None:
        ...

    def complete(self) -> None:
        ...

    def status(self, message: str) -> None:
        ...
