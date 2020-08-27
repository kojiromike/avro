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

"""Protocol implementation."""

from typing import Dict, List, Optional, Sequence, Union

import avro.schema

class Protocol:
    """An application protocol."""

    def _parse_types(self, types: Sequence[str], type_names: avro.schema.Names) -> List[avro.schema.Schema]:
        ...

    def _parse_messages(self, messages: List[ Message], names: List[str]) -> Dict[str, Message]:
        ...

    def __init__(self,
                 name: str,
                 namespace: Optional[str]=None,
                 types: Optional[List[str]]=None,
                 messages: Optional[List[bytes]]=None) -> None:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def namespace(self) -> str:
        ...

    @property
    def fullname(self) -> str:
        ...

    @property
    def types(self) -> List[str]:
        ...

    @property
    def types_dict(self) -> Dict[str, str]:
        ...

    @property
    def messages(self) -> bytes:
        ...

    @property
    def md5(self) -> bytes:
        ...

    @property
    def props(self) -> Dict[str, str]:
        ...

    def get_prop(self, key: str) -> str:
        ...

    def set_prop(self, key: str, value: str) -> None:
        ...

    def to_json(self) -> Dict[str, Union[str, Dict[str, str]]]:
        ...

    def __str__(self) -> str:
        ...

    def __eq__(self, that: object) -> bool:
        ...


class Message:
    def _parse_request(self, request: str, names: avro.schema.Names) -> avro.schema.RecordSchema:
        ...

    def _parse_response(self, response: Dict[str, str], names: avro.schema.Names) -> avro.schema.Schema:
        ...

    def _parse_errors(self, errors: List[str], names: avro.schema.Names) -> None:
        ...

    def __init__(self, name: avro.schema.Name, request: bytes, response: bytes,
                 errors: Optional[List[str]]=None,
                 names: Optional[avro.schema.Names]=None) -> None:
        ...

    @property
    def name(self) -> avro.schema.Name:
        ...

    @property
    def request(self) -> str:
        ...

    @property
    def response(self) -> str:
        ...

    @property
    def errors(self) -> str:
        ...

    @property
    def props(self) -> Dict[str, str]:
        ...

    def get_prop(self, key: str) -> str:
        ...

    def set_prop(self, key: str, value: str) -> None:
        ...

    def __str__(self) -> str:
        ...

    def to_json(self, names: Optional[avro.schema.Names]=None) -> Dict[str, Union[str, Dict[str, str]]]:
        ...

    def __eq__(self, that: object) -> bool:
        ...


def make_avpr_object(json_data: str) -> Protocol:
    ...


def parse(json_string: str) -> Protocol:
    ...
