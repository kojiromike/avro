#!/usr/bin/env python

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

"""unittest for a python tethered map-reduce job"""

from __future__ import absolute_import, division, print_function

import os
import shutil
import subprocess
import sys
import tempfile
import unittest

import avro
import avro.datafile
import avro.io
import avro.schema
import avro.tether.tether_task_runner
import set_avro_test_path


class TestTetherWordCount(unittest.TestCase):
  def _write_lines(self,lines,fname):
    """
    Write the lines to an avro file named fname

    Parameters
    --------------------------------------------------------
    lines - list of strings to write
    fname - the name of the file to write to.
    """
    with file(fname,'w') as hf:
      inschema="""{"type":"string"}"""
      writer = avro.datafile.DataFileWriter(hf, avro.io.DatumWriter(inschema), writers_schema=avro.schema.parse(inschema))
      for datum in lines:
        writer.append(datum)

      writer.close()




  def _count_words(self,lines):
    """Return a dictionary counting the words in lines
    """
    counts={}

    for line in lines:
      words=line.split()

      for w in words:
        if not(w.strip() in counts):
          counts[w.strip()]=0

        counts[w.strip()]=counts[w.strip()]+1

    return counts

  def test1(self):
    """
    Run a tethered map-reduce job.

    Assumptions: 1) bash is available in /bin/bash
    """
    proc=None
    exfile = None

    try:


      # TODO we use the tempfile module to generate random names
      # for the files
      base_dir = "/tmp/test_tether_word_count"
      if os.path.exists(base_dir):
        shutil.rmtree(base_dir)

      inpath = os.path.join(base_dir, "in")
      infile=os.path.join(inpath, "lines.avro")
      lines=["the quick brown fox jumps over the lazy dog",
             "the cow jumps over the moon",
             "the rain in spain falls mainly on the plains"]

      if not os.path.isdir(inpath):
        os.makedirs(inpath)
      self._write_lines(lines,infile)

      true_counts=self._count_words(lines)

      if not(os.path.exists(infile)):
        self.fail("Missing the input file {0}".format(infile))


      # The schema for the output of the mapper and reducer
      oschema="""
{"type":"record",
 "name":"Pair","namespace":"org.apache.avro.mapred","fields":[
     {"name":"key","type":"string"},
     {"name":"value","type":"long","order":"ignore"}
 ]
}
"""

      # write the schema to a temporary file
      osfile=tempfile.NamedTemporaryFile(mode='w',suffix=".avsc",prefix="wordcount",delete=False)
      outschema=osfile.name
      osfile.write(oschema)
      osfile.close()

      if not(os.path.exists(outschema)):
        self.fail("Missing the schema file")

      outpath = os.path.join(base_dir, "out")
      # Ensure avro and tests are on the PYTHONPATH.
      avro_path = os.path.dirname(avro.__file__)
      test_path = os.path.dirname(__file__)
      python_path = (os.pathsep).join([avro_path, test_path])
      jarpath = os.path.abspath("@TOPDIR@/../java/tools/target/avro-tools-@AVRO_VERSION@.jar")
      args = ("java", "-jar", jarpath, "tether",
              "--in", inpath,
              "--out", outpath,
              "--outschema", outschema,
              "--protocol", "http",
              "--program", "python",
              "--exec_args", "-m avro.tether.tether_task_runner "
                             "word_count_task.WordCountTask")

      print("Command:\n\t{0}".format(" ".join(args)))
      proc = subprocess.Popen(args, env={"PYTHONPATH": python_path})


      proc.wait()

      # read the output
      with file(os.path.join(outpath,"part-00000.avro")) as hf:
        reader = avro.datafile.DataFileReader(hf, avro.io.DatumReader())
        for record in reader:
          self.assertEqual(record["value"],true_counts[record["key"]])

        reader.close()

    except Exception as e:
      raise
    finally:
      # close the process
      if proc is not None and proc.returncode is None:
        proc.kill()
      if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
      if exfile is not None and os.path.exists(exfile):
        os.remove(exfile)

if __name__== "__main__":
  unittest.main()
