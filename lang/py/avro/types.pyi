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
Types that Avro knows about.

Python doesn't support recursive types, so we emulate it
with an arbitrarily deep nested type. This only gets evaluated
during type checking, not during run time.

Avro should eventually support more flexible python duck typing.
But at the time type hints are being added, it does not.
We keep a strict list of types that avro really "understands",
so that we can keep our typing straight as we make it better.
"""

from typing import *

AvroAny = Union[None, bytes, float, int, str,
        Dict[str, Union[None, bytes, float, int, str]],
        List[Union[None, bytes, float, int, str]]]
