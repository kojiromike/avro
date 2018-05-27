#!/usr/bin/env python

"""Practice with Avro

I want to define a valid Avro schema that can itself serialize
and unserialize to a valid Avro schema.
"""

from json import dumps
from io import BytesIO
from typing import Any, List

from avro.io import DatumReader, BinaryDecoder, DatumWriter, BinaryEncoder
from avro.schema import Parse as parse, PRIMITIVE_TYPES

SCHEMA: List[Any] = []
SCHEMA_DOC = """
Schema Declaration

A Schema is represented in JSON by one of:

    A JSON string, naming a defined type.
    A JSON object, of the form:

        {"type": "typeName" ...attributes...}

        where typeName is either a primitive or derived type name, as defined below.
        Attributes not defined in this document are permitted as metadata, but must
        not affect the format of serialized data.

    A JSON array, representing a union of embedded types.
"""

# A JSON string, naming a defined type.

# Initially, an avro schema is a union of three types: string, mapping and union.

# A JSON string, naming a defined type.
# Only the primitive types are known at the root.
# So it's not just a string, it's an enum of primitive types.
VALID_PRIMITIVES_ENUM = {
    "type": "enum",
    "name": "primitives_type",
    "namespace": "avro",
    "doc": "A choice of valid avro type names.",
    "symbols": tuple(PRIMITIVE_TYPES),
}
SCHEMA.append(VALID_PRIMITIVES_ENUM)

# A JSON object, of the form: {"type": "typeName" ...attributes...}
# First, we'll repeat the primitive types in this form.
VALID_PRIMITIVES_RECORD = {
    "type": "record",
    "name": "primitives",
    "namespace": "avro",
    "fields": [{"name": "type", "type": "primitives_type"}]
}
SCHEMA.append(VALID_PRIMITIVES_RECORD)

# Then we add some compound types
ARRAYS_DOC = """
Arrays use the type name "array" and support a single attribute:

    items: the schema of the array's items.

For example, an array of strings is declared with:

{"type": "array", "items": "string"}
"""
ARRAY_TYPE = {
    "type": "enum",
    "name": "array_type",
    "namespace": "avro",
    "doc": "A string that can only be 'array'",
    "symbols": tuple(["array"])
}
PRIMITIVE_ARRAY_TYPE_RECORD = {
    "type": "record",
    "name": "array",
    "namespace": "avro",
    "fields": [
        {"name": "type", "type": ARRAY_TYPE},
        {"name": "items", "type": SCHEMA.copy()},
    ]
}


#   [
#     ARRAY,
#     MAP,
#     UNION,
#     REQUEST,
#     ERROR_UNION,
#   ],
# Then we'll add the complex types
FIXED_DOC = """
Fixed uses the type name "fixed" and supports two attributes:

    name: a string naming this fixed (required).
    namespace, a string that qualifies the name;
    aliases: a JSON array of strings, providing alternate names for this enum (optional).
    size: an integer, specifying the number of bytes per value (required).

For example, 16-byte quantity may be declared with:

{"type": "fixed", "size": 16, "name": "md5"}
"""
FIXED_TYPE = {
    "type": "enum",
    "name": "fixed_type",
    "namespace": "avro",
    "doc": "A string that can only be 'fixed'",
    "symbols": tuple(["fixed"])
}
NAMESPACE_TYPE = ["null", "string"]
ALIASES_TYPE = ["null"] # or array of strings
VALID_FIXED_TYPE_RECORD = {
    "type": "record",
    "name": "fixed",
    "namespace": "avro",
    "doc": FIXED_DOC.strip(),
    "fields": [
        {"name": "type", "type": FIXED_TYPE},
        {"name": "name", "type": "string"},
        {"name": "namespace", "type": NAMESPACE_TYPE},
        {"name": "aliases", "type": ALIASES_TYPE},
        {"name": "size", "type": "int"}
    ]
}
SCHEMA.append(VALID_FIXED_TYPE_RECORD)

ENUM_DOC = """
An enum is encoded by a int, representing the zero-based position of the symbol in the schema.

For example, consider the enum:

	      {"type": "enum", "name": "Foo", "symbols": ["A", "B", "C", "D"] }

This would be encoded by an int between zero and three, with zero indicating "A", and 3 indicating "D".
"""
ENUM_TYPE = {
    "type": "enum",
    "name": "enum_type",
    "namespace": "avro",
    "doc": "A string that can only be 'enum'",
    "symbols": tuple(["enum"])
}
VALID_ENUM_TYPE_RECORD = {
    "type": "record",
    "name": "enum",
    "namespace": "avro",
    "doc": "The enum type",
    "fields": [
        {"name": "type", "type": ENUM_TYPE},
        {"name": "name", "type": "string"},
        {"name": "namespace", "type": NAMESPACE_TYPE},
        {"name": "aliases", "type": ALIASES_TYPE},
        {"name": "symbols", "type": []}
    ]
}

# NAMED_TYPES = frozenset([
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
print(dumps(METASCHEMA.to_json()))
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
