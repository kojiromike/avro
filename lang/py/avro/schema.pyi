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

from abc import ABC
from datetime import datetime
from typing import Collection, Dict, List, Optional, Sequence

from avro.types import AvroAny

def validate_basename(basename: str) -> None:
    ...


def _is_timezone_aware_datetime(dt: datetime) -> bool:
    ...


class Schema(ABC):

    def __init__(self, type: str, other_props: Optional[Dict[str, str]]) -> None:
        ...

    @property
    def props(self) -> Dict[str, str]:
        ...

    @property
    def other_props(self) -> Dict[str, str]:
        ...

    def check_props(self, other: str, props: Dict[str, str]) -> bool:
        ...

    def match(self, writer: "Schema") -> bool:
        ...

    def get_prop(self, key: str) -> str:
        ...

    def set_prop(self, key: str, value: str) -> None:
        ...

    def __str__(self) -> str:
        ...

    def to_json(self, names: "Names") -> str:
        ...

    def __eq__(self, other: object) -> bool:
        ...


class Name:

    def __init__(self, name_attr: str, space_attr: str, default_space: str) -> None:
        ...

    def _validate_fullname(self, fullname: str) -> None:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    @property
    def fullname(self) -> str:
        ...

    @property
    def space(self) -> Optional[str]:
        ...

    def get_space(self) -> Optional[str]:
        ...


class Names:

    def __init__(self, default_namespace: Optional[str]) -> None:
        ...

    def has_name(self, name_attr: str, space_attr: str) -> bool:
        ...

    def get_name(self, name_attr: str, space_attr: str) -> Optional[str]:
        ...

    def prune_namespace(self, properties: Dict[str, str]) -> Dict[str, str]:
        ...

    def add_name(self, name_attr: str, space_attr: str, new_schema: Schema) -> Name:
        ...

class NamedSchema(Schema):
    """Named Schemas specified in NAMED_TYPES."""
    _fullname = None  # type: str

    def __init__(self,
                 type_: str,
                 name: str,
                 namespace: Optional[str]=None,
                 names: Optional[Names]=None,
                 other_props: Optional[Dict[str, str]]=None) -> None:
        ...

    def name_ref(self, names: Names) -> str:
        ...

    @property
    def name(self) -> str:
        return self.get_prop('name')

    @property
    def namespace(self) -> str:
        return self.get_prop('namespace')

    @property
    def fullname(self) -> str:
        return self._fullname


class LogicalSchema:
    def __init__(self, logical_type: str) -> None:
        ...


class DecimalLogicalSchema(LogicalSchema):
    def __init__(self, precision: int, scale: int=0, max_precision: int=0) -> None:
        ...

    @property
    def precision(self) -> int:
        ...

    @property
    def scale(self) -> int:
        ...


class Field:
    def __init__(self,
                 type_: str,
                 name: str,
                 has_default: bool,
                 default: AvroAny=None,
                 order: Optional[str]=None,
                 names: Optional[Names]=None,
                 doc: Optional[str]=None,
                 other_props: Optional[Dict[str, str]]=None) -> None:
        ...

    @property
    def default(self) -> AvroAny:
        ...

    @property
    def has_default(self) -> bool:
        ...

    @property
    def order(self) -> str:
        ...

    @property
    def doc(self) -> str:
        ...

    @property
    def props(self) -> Dict[str, str]:
        ...

    @property
    def other_props(self) -> Dict[str, str]:
        ...

    def get_prop(self, key: str) -> str:
        ...

    def set_prop(self, key: str, value: str) -> None:
        ...

    def __str__(self) -> str:
        ...

    def to_json(self, names: Optional[Names]=None) -> str:
        ...

    def __eq__(self, other: object) -> bool:
        ...


class PrimitiveSchema(Schema):
    def __init__(self, type_: str, other_props: Optional[Dict[str, str]]=None) -> None:
        ...


class BytesDecimalSchema(PrimitiveSchema, DecimalLogicalSchema):
    def __init__(self,
                 precision: int,
                 scale: int=0,
                 other_props: Optional[Dict[str, str]]=None) -> None:
        ...


class FixedSchema(NamedSchema):
    def __init__(self,
                 name: str,
                 namespace: str,
                 size: int,
                 names: Optional[Names]=None,
                 other_props: Optional[Dict[str, str]]=None) -> None:
        ...

    @property
    def size(self) -> int:
        ...


class FixedDecimalSchema(FixedSchema, DecimalLogicalSchema):
    def __init__(self,
                 size: int,
                 name: str,
                 precision: int,
                 scale: int=0,
                 namespace: Optional[str]=None,
                 names: Optional[Names]=None,
                 other_props: Optional[Dict[str, str]]=None) -> None:
        ...


class EnumSchema(NamedSchema):
    def __init__(self,
                 name: str,
                 namespace: str,
                 symbols: Sequence[str],
                 names: Optional[Names]=None,
                 doc: Optional[str]=None,
                 other_props: Optional[Dict[str, str]]=None,
                 validate_enum_symbols: bool=True) -> None:
        ...

    @property
    def symbols(self) -> List[str]:
        ...

    @property
    def doc(self) -> str:
        ...


class ArraySchema(Schema):
    def __init__(self,
                 items: Sequence[Schema],
                 names: Optional[Names]=None,
                 other_props: Optional[Dict[str, str]]=None) -> None:
        ...

    @property
    def items(self) -> List[Schema]:
        ...


class MapSchema(Schema):
    def __init__(self,
                 values: Sequence[Schema],
                 names: Optional[Names]=None,
                 other_props: Optional[Dict[str, str]]=None) -> None:
        ...

    @property
    def values(self) -> List[Schema]:
        ...


class UnionSchema(Schema):

    def __init__(self,
                 schemas: Sequence[Schema],
                 names: Optional[Names]=None) -> None:
        ...

    @property
    def schemas(self) -> List[Schema]:
        ...


class ErrorUnionSchema(UnionSchema):
    ...


class RecordSchema(NamedSchema):
    @staticmethod
    def make_field_objects(field_data: Sequence[Field],
                           names: Names) -> List[Field]:
        ...

    def __init__(self,
                 name: str,
                 namespace: str,
                 fields: Collection[Field],
                 names: Optional[Names]=None,
                 schema_type: str='record',
                 doc: Optional[str]=None,
                 other_props: Optional[Dict[str, str]]=None) -> None:
        ...

    @property
    def fields(self) -> List[Field]:
        ...

    @property
    def doc(self) -> str:
        ...

    @property
    def fields_dict(self) -> Dict[str, Field]:
        ...


class DateSchema(LogicalSchema, PrimitiveSchema):
    def __init__(self, other_props: Optional[Dict[str, str]]=None) -> None:
        ...


class TimeMillisSchema(LogicalSchema, PrimitiveSchema):
    def __init__(self, other_props: Optional[Dict[str, str]]=None) -> None:
        ...


class TimeMicrosSchema(LogicalSchema, PrimitiveSchema):
    def __init__(self, other_props: Optional[Dict[str, str]]=None) -> None:
        ...


class TimestampMillisSchema(LogicalSchema, PrimitiveSchema):
    def __init__(self, other_props: Optional[Dict[str, str]]=None) -> None:
        ...


class TimestampMicrosSchema(LogicalSchema, PrimitiveSchema):
    def __init__(self, other_props: Optional[Dict[str, str]]=None) -> None:
        ...


def get_other_props(all_props: Dict[str, str],
                    reserved_props: Dict[str, str]) -> Dict[str, str]:
    ...


def make_bytes_decimal_schema(other_props: Dict[str, str]) -> BytesDecimalSchema:
    ...


def make_logical_schema(logical_type: str,
                        type_: str,
                        other_props: Dict[str, str]) -> Optional[LogicalSchema]:
    ...


def make_avsc_object(json_data: str,
                     names: Optional[Names]=None,
                     validate_enum_symbols: bool=True) -> Schema:
    ...


def parse(json_string: str,
          validate_enum_symbols: bool=True) -> Schema:
    ...
