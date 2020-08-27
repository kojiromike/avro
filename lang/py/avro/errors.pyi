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

from typing import Optional

import avro.schema
import avro.types

class AvroException(Exception):
    """The base class for exceptions in avro."""


class SchemaParseException(AvroException):
    """Raised when a schema failed to parse."""


class InvalidName(SchemaParseException):
    """User attempted to parse a schema with an invalid name."""


class AvroWarning(UserWarning):
    """Base class for warnings."""


class IgnoredLogicalType(AvroWarning):
    """Warnings for unknown or invalid logical types."""


class AvroTypeException(AvroException):
    def __init__(self,
                 expected_schema: avro.schema.Schema,
                 datum: avro.types.AvroAny) -> None:
        ...


class SchemaResolutionException(AvroException):
    def __init__(self,
                 fail_msg: str,
                 writers_schema: Optional[avro.schema.Schema]=None,
                 readers_schema: Optional[avro.schema.Schema]=None) -> None:
        ...


class DataFileException(AvroException):
    """Raised when there's a problem reading or writing file object containers."""


class AvroRemoteException(AvroException):
    """Raised when an error message is sent by an Avro requestor or responder."""


class ConnectionClosedException(AvroException):
    """Raised when attempting IPC on a closed connection."""


class ProtocolParseException(AvroException):
    """Raised when a protocol failed to parse."""


class UnsupportedCodec(NotImplementedError, AvroException):
    """Raised when the compression named cannot be used."""


class UsageError(RuntimeError, AvroException):
    """An exception raised when incorrect arguments were passed."""
