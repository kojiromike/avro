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
Command-line tool

NOTE: The API for the command-line tool is experimental.
"""

import http.server
import sys
import warnings
from typing import BinaryIO, Dict, Sequence

import avro.ipc
import avro.protocol
import avro.types

class GenericResponder(avro.ipc.Responder):
    def __init__(self,
                 proto: avro.protocol.Protocol,
                 msg: avro.protocol.Protocol,
                 datum: avro.types.AvroAny) -> None:
        ...

    def invoke(self, message: avro.protocol.Protocol, request: Dict[str, str]) -> str:
        ...

class GenericHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        ...

def run_server(uri: str,
               proto: avro.protocol.Protocol,
               msg: str,
               datum: avro.types.AvroAny) -> None:
    ...

def send_message(uri: str,
                 proto: avro.protocol.Protocol,
                 msg: str,
                 datum: avro.types.AvroAny) -> None:
    ...

def file_or_stdin(f: str) -> BinaryIO:
    ...


def main(args: Sequence[str]=sys.argv) -> int:
    ...
