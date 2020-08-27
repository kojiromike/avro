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

"""
Contains Codecs for Python Avro.

Note that the word "codecs" means "compression/decompression algorithms" in the
Avro world (https://avro.apache.org/docs/current/spec.html#Object+Container+Files),
so don't confuse it with the Python's "codecs", which is a package mainly for
converting charsets (https://docs.python.org/3/library/codecs.html).
"""

import abc
from typing import List

import avro.io

class Codec(abc.ABC):
    """Abstract base class for all Avro codec classes."""

    def compress(self, data: bytes) -> bytes:
        ...

    def decompress(self, readers_decoder: avro.io.BinaryDecoder) -> avro.io.BinaryDecoder:
        ...


class SnappyCodec(Codec):

    def check_crc32(self, bytes_: bytes, checksum: bytes) -> None:
        ...


def get_codec(codec_name: str) -> Codec:
    ...


def supported_codec_names() -> List[str]:
    ...
