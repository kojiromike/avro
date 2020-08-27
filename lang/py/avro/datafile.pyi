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

from types import TracebackType
from typing import *

from avro.io import BinaryDecoder, BinaryEncoder, DatumReader, DatumWriter
from avro.schema import Schema
from avro.types import AvroAny

VALID_CODECS = ()  # type: Sequence[str]


class _DataFile:
    def __exit__(self, type: Type[BaseException], value: BaseException, traceback: TracebackType) -> None:
        ...
    def get_meta(self, key: str) -> bytes:
        ...
    def set_meta(self, key: str, val: bytes) -> None:
        ...
    @property
    def sync_marker(self) -> int:
        ...
    @property
    def meta(self) -> Dict[str, bytes]:
        ...
    @property
    def codec(self) -> str:
        ...
    @codec.setter
    def codec(self, value: str) -> None:
        ...
    @property
    def schema(self) -> Schema:
        ...
    @schema.setter
    def schema(self, value: Schema) -> None:
        ...


class DataFileWriter(_DataFile):
    def __init__(self, writer: BinaryIO, datum_writer: DatumWriter, writers_schema: Optional[Schema], codec: str) -> None:
        ...
    def __enter__(self) -> "DataFileWriter":
        ...
    @property
    def writer(self) -> BinaryIO:
        ...
    @property
    def encoder(self) -> BinaryEncoder:
        ...
    @property
    def datum_writer(self) -> DatumWriter:
        ...
    @property
    def buffer_writer(self) -> BinaryIO:
        ...
    @property
    def buffer_encoder(self) -> BinaryEncoder:
        ...
    def _write_header(self) -> None:
        ...
    def _write_block(self) -> None:
        ...
    def append(self, datum: AvroAny) -> None:
        ...
    def sync(self) -> int:
        ...
    def flush(self) -> None:
        ...
    def close(self) -> None:
        ...

class DataFileReader(_DataFile):
    def __init__(self, reader: BinaryIO, datum_reader: DatumReader) -> None:
        ...
    def __iter__(self) -> "DataFileReader":
        ...
    def __enter__(self) -> "DataFileReader":
        ...
    @property
    def reader(self) -> BinaryIO:
        ...
    @property
    def raw_decoder(self) -> BinaryDecoder:
        ...
    @property
    def datum_decoder(self) -> BinaryDecoder:
        ...
    @property
    def datum_reader(self) -> DatumReader:
        ...
    @property
    def file_length(self) -> int:
        ...
    def determine_file_length(self) -> int:
        ...
    def is_EOF(self) -> bool:
        ...
    def _read_header(self) -> None:
        ...
    def _read_block_header(self) -> None:
        ...
    def _skip_sync(self) -> bool:
        ...
    def __next__(self) -> AvroAny:
        ...
    def close(self) -> None:
        ...

def generate_sixteen_random_bytes() -> bytes:
    ...
