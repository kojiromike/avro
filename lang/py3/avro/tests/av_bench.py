#!/usr/bin/env python3
# -*- mode: python -*-
# -*- coding: utf-8 -*-

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import random
import string
import sys
import time

import avro.datafile
import avro.io
import avro.schema

TYPES = ('A', 'CNAME',)
FILENAME = 'datafile.avr'


def GenerateRandomName():
    return ''.join(random.sample(string.ascii_lowercase, 15))


def GenerateRandomIP():
    return '%s.%s.%s.%s' % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def Write(nrecords):
    """Writes a data file with the specified number of random records.

    Args:
      nrecords: Number of records to write.
    """
    schema_s = """
  {
    "type": "record",
    "name": "Query",
    "fields" : [
      {"name": "query", "type": "string"},
      {"name": "response", "type": "string"},
      {"name": "type", "type": "string", "default": "A"}
    ]
  }
  """
    schema = avro.schema.parse(schema_s)
    writer = avro.io.DatumWriter(schema)

    with open(FILENAME, 'wb') as out:
        with avro.datafile.DataFileWriter(
            out, writer, schema,
            # codec='deflate'
        ) as data_writer:
            for _ in range(nrecords):
                response = GenerateRandomIP()
                query = GenerateRandomName()
                type = random.choice(TYPES)
                data_writer.append({
                    'query': query,
                    'response': response,
                    'type': type,
                })


def Read(expect_nrecords):
    """Reads the data file generated by Write()."""
    with open(FILENAME, 'rb') as f:
        reader = avro.io.DatumReader()
        with avro.datafile.DataFileReader(f, reader) as file_reader:
            nrecords = 0
            for record in file_reader:
                nrecords += 1
            assert (nrecords == expect_nrecords), (
                'Expecting %d records, got %d.' % (expected_nrecords, nrecords))


def Timing(f, *args):
    s = time.time()
    f(*args)
    e = time.time()
    return e - s


def Main(args):
    nrecords = int(args[1])
    print('Write %0.4f' % Timing(Write, nrecords))
    print('Read %0.4f' % Timing(Read, nrecords))


if __name__ == '__main__':
    log_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(filename)s:%(lineno)s : %(message)s')
    logging.root.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.DEBUG)
    logging.root.addHandler(console_handler)

    Main(sys.argv)
