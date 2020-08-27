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

"""Support for inter-process calls."""

from __future__ import annotations

import abc
from typing import Any, BinaryIO, Dict

from avro.io import BinaryDecoder, BinaryEncoder
from avro.protocol import Protocol
from avro.schema import Schema
from avro.types import AvroAny

class BaseRequestor(abc.ABC):
    """Base class for the client side of a protocol interaction."""
    def __init__(self, local_protocol: Protocol, transceiver: HTTPTransceiver) -> None:
        ...
    def request(self, message_name: str, request_datum: AvroAny) -> AvroAny:
        ...

    def issue_request(self, call_request: bytes, message_name: str, request_datum: AvroAny) -> AvroAny:
        ...

    def read_call_response(self, message_name: str, decoder: BinaryDecoder) -> AvroAny:
        ...

class Requestor(BaseRequestor):
    ...

class Responder:
    def __init__(self, local_protocol: Protocol) -> None:
        ...
    @property
    def local_protocol(self) -> Protocol:
        ...
    @property
    def local_hash(self) -> bytes:
        ...
    @property
    def protocol_cache(self) -> Dict[bytes, Protocol]:
        ...
    def get_protocol_cache(self, hash: bytes) -> Protocol:
        ...
    def set_protocol_cache(self, hash: bytes, protocol: Protocol) -> None:
        ...
    def respond(self, call_request: bytes) -> bytes:
        ...
    def process_handshake(self, decoder: BinaryDecoder, encoder: BinaryEncoder) -> Protocol:
        ...
    def invoke(self, local_message: Protocol, request: Dict[str, str]) -> str:
        ...

    def read_request(self, writers_schema: Schema, readers_schema: Schema, decoder: BinaryDecoder) -> AvroAny:
        ...
    def write_response(self, writers_schema: Schema, response_datum: AvroAny, encoder: BinaryEncoder) -> None:
        ...
    def write_error(self, writers_schema: Schema, error_exception: BaseException, encoder: BinaryEncoder) -> None:
        ...

class FramedReader:
    def __init__(self, reader: BinaryIO) -> None:
        ...
    @property
    def reader(self) -> BinaryIO:
        ...
    def read_framed_message(self) -> bytes:
        ...
    def _read_buffer_length(self) -> int:
        ...

class FramedWriter:
    def __init__(self, writer: BinaryIO) -> None:
        ...
    @property
    def writer(self) -> BinaryIO:
        ...
    def write_framed_message(self, message: bytes) -> None:
        ...
    def write_buffer(self, chunk: bytes) -> None:
        ...
    def write_buffer_length(self, n: int) -> None:
        ...

class HTTPTransceiver:
    def __init__(self, host: str, port: int, req_resource: str='/') -> None:
        ...
    def transceive(self, request: bytes) -> bytes:
        ...
    def read_framed_message(self) -> bytes:
        ...
    def write_framed_message(self, message: bytes) -> None:
        ...
    def close(self) -> None:
        ...
