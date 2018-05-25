#!/usr/bin/env python

"""Practice with Avro

I want to define a valid Avro schema that can itself serialize
and unserialize to a valid Avro schema.

Schema Declaration

A Schema is represented in JSON by one of:

    A JSON string, naming a defined type.
    A JSON object, of the form:

    {"type": "typeName" ...attributes...}

    where typeName is either a primitive or derived type name, as defined below. Attributes not defined in this document are permitted as metadata, but must not affect the format of serialized data.
    A JSON array, representing a union of embedded types.
"""

from json import dumps
from io import BytesIO
from pprint import pprint
from typing import Any, List

from avro.io import DatumReader, BinaryDecoder, DatumWriter, BinaryEncoder
from avro.schema import Parse as parse, PRIMITIVE_TYPES

# Initially, an avro schema is a union of three types: string, mapping and union.
SCHEMA: List[Any] = []

# A JSON string, naming a defined type.
# Only the primitive types are known at the root.
# So it's not just a string, it's an enum of primitive types.
VALID_PRIMITIVES_ENUM = {
    "type": "enum",
    "name": "valid_primitives_enum",
    "namespace": "avro",
    "doc": "A choice of valid avro type names.",
    "symbols": tuple(PRIMITIVE_TYPES),
}
SCHEMA.append(VALID_PRIMITIVES_ENUM)

# A JSON object, of the form: {"type": "typeName" ...attributes...}
# First, we'll repeat the primitive types in this form.
VALID_PRIMITIVES_RECORD = {
    "type": "record",
    "name": "valid_primitives_record",
    "namespace": "avro",
    "fields": [{"name": "type", "type": "valid_primitives_enum"}]
}
SCHEMA.append(VALID_PRIMITIVES_RECORD)

# Then we'll add the complex types
VALID_FIXED_TYPE_TYPE = {
    "type": "enum",
    "name": "fixed_type",
    "namespace": "avro",
    "doc": "The avro fixed data type",
    "symbols": tuple(["fixed"])
}
"""
Fixed

Fixed uses the type name "fixed" and supports two attributes:

    name: a string naming this fixed (required).
    namespace, a string that qualifies the name;
    aliases: a JSON array of strings, providing alternate names for this enum (optional).
    size: an integer, specifying the number of bytes per value (required).

For example, 16-byte quantity may be declared with:

{"type": "fixed", "size": 16, "name": "md5"}
"""
NAMESPACE_TYPE = ["null", "string"]
ALIASES_TYPE = ["null"] # or array of strings
VALID_FIXED_TYPE_RECORD = {
    "type": "record",
    "name": "valid_fixed_record",
    "namespace": "avro",
    "fields": [
        {"name": "type", "type": VALID_FIXED_TYPE_TYPE},
        {"name": "name", "type": "string"},
        {"name": "namespace", "type": NAMESPACE_TYPE},
        {"name": "aliases", "type": ALIASES_TYPE},
        {"name": "size", "type": "int"}
    ]
}
SCHEMA.append(VALID_FIXED_TYPE_RECORD)

# NAMED_TYPES = frozenset([
#   FIXED,
#   ENUM,
#   RECORD,
#   ERROR,
# ])

# VALID_TYPES = frozenset.union(
#   PRIMITIVE_TYPES,
#   NAMED_TYPES,
#   [
#     ARRAY,
#     MAP,
#     UNION,
#     REQUEST,
#     ERROR_UNION,
#   ],
# )

# A JSON array, representing a union of embedded types
METASCHEMA = parse(dumps(SCHEMA))


# # A Schema is represented in JSON by one of:
# SCHEMA: List = []
# SCHEMA.append("string") # A JSON string, naming a defined type.
# SCHEMA.append("mapping") # A JSON object, of the form `{"type": "typeName", ...attributes...}`

print("schema looks like")
print(dumps(METASCHEMA.to_json(), indent=2))
print()

def _avro_test_objects(schema):
    """Regenerate avro test objects"""
    writer = DatumWriter(schema)
    reader = DatumReader(schema)
    storage = BytesIO()
    encoder = BinaryEncoder(storage)
    decoder = BinaryDecoder(storage)
    return writer, reader, storage, encoder, decoder

def test_bare_primitives():
    """Test that we can encode and decode bare primitive types."""
    writer, reader, storage, encoder, decoder = _avro_test_objects(METASCHEMA)
    result = set([])
    for name in PRIMITIVE_TYPES:
        writer.write(name, encoder)
    storage.seek(0)
    while True:
        try:
            result.add(reader.read(decoder))
        except AssertionError:
            break
    assert result
    assert result == PRIMITIVE_TYPES

def test_dict_primitives():
    """Test that primitives encoded as dict types can be decoded."""
    writer, reader, storage, encoder, decoder = _avro_test_objects(METASCHEMA)
    result = set([])
    for name in PRIMITIVE_TYPES:
        writer.write({"type": name}, encoder)
    storage.seek(0)
    result = set([])
    while True:
        try:
            datum = reader.read(decoder)
            result.add(datum["type"])
        except AssertionError:
            break
    assert result
    assert result == PRIMITIVE_TYPES

def test_fixed():
    """Test that a fixed type type can be encoded and decoded."""
    writer, reader, storage, encoder, decoder = _avro_test_objects(METASCHEMA)
    result = set([])
    writer.write({"type": "fixed", "name": "test", "size": 12}, encoder)
    storage.seek(0)
    datum = reader.read(decoder)
    assert datum.pop("type") == "fixed"
    assert datum.pop("name") == "test"
    assert datum.pop("size") == 12
    assert not datum.pop("namespace")
    assert not datum.pop("aliases")
    assert not datum


# WRITER.write(METASCHEMA.to_json(), ENCODER)
