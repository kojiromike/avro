#!/usr/bin/env python

"""Practice with Avro

I want to define a valid Avro schema that can itself serialize
and unserialize to a valid Avro schema.
"""

from json import dumps
from io import BytesIO
from typing import Any, List

from avro.io import AvroTypeException, DatumReader, BinaryDecoder, DatumWriter, BinaryEncoder
from avro.schema import Parse as parse, PRIMITIVE_TYPES

TEST_CASES = {
    "string": {"type": "string"},
    "record": {"type": "record",
               "name": "LongList",
               "aliases": ["LinkedLongs"],
               "fields" : [{"name": "value", "type": "long"},
                           {"name": "next", "type": ["null", "LongList"]}]},
    "enum": {"type": "enum",
             "name": "Suit",
             "symbols" : ["SPADES", "HEARTS", "DIAMONDS", "CLUBS"]},
    "array": {"type": "array", "items": "string"},
    "map": {"type": "map", "values": "long"},
    "fixed": {"type": "fixed", "size": 16, "name": "md5"},
    "union": ["string", "long"]
}

def _avro_test_objects(schema):
    """Regenerate avro test objects"""
    writer = DatumWriter(schema)
    reader = DatumReader(schema)
    storage = BytesIO()
    encoder = BinaryEncoder(storage)
    decoder = BinaryDecoder(storage)
    return writer, reader, storage, encoder, decoder

def _parse_metaschema():
    with open("metaschema.avsc") as metaschema_file:
        metaschema = metaschema_file.read()
    return parse(metaschema)

def test_parse_metaschema():
    """Test that avro can load the metaschema at all."""
    _parse_metaschema()

def test_empty_schema_invalid():
    """Test that an empty schema is not allowed."""
    metaschema = _parse_metaschema()
    writer, _, _, encoder, _ = _avro_test_objects(metaschema)
    try:
        writer.write(None, encoder)
        assert False, "Expected AvroTypeException when writing invalid data"
    except AvroTypeException:
        pass

def test_primitive_type_strings():
    """Test that a schema consisting of a lone string that is a valid primitive type is valid."""
    metaschema = _parse_metaschema()
    writer, _, _, encoder, _ = _avro_test_objects(metaschema)
    for name in PRIMITIVE_TYPES:
        writer.write(name, encoder)

def test_cases():
    """Test the examples given in the avro documentation."""
    metaschema = _parse_metaschema()
    writer, _, _, encoder, _ = _avro_test_objects(metaschema)
    for name, example in TEST_CASES.items():
        writer.write(example, encoder)
