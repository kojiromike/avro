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

"""
Provide the code necessary for packaging and installing avro-python.

https://pypi.org/project/avro/
"""


from __future__ import absolute_import, division, print_function

import distutils.errors
import glob
import os
import subprocess

import setuptools


_HERE = os.path.dirname(os.path.abspath(__file__))
_AVRO_DIR = os.path.join(_HERE, 'src', 'avro')
_VERSION_FILE_NAME = 'VERSION.txt'

def _is_distribution():
    """Tests whether setup.py is invoked from a distribution.

    Returns:
        True if setup.py runs from a distribution.
        False otherwise, ie. if setup.py runs from a version control work tree.
    """
    # If a file PKG-INFO exists as a sibling of setup.py,
    # assume we are running as source distribution:
    return os.path.exists(os.path.join(_HERE, 'PKG-INFO'))


def _generate_package_data():
    """Generate package data.

    This data will already exist in a distribution package,
    so this function only runs for local version control work tree.
    """
    distutils.log.info('Generating package data')

    # Avro top-level source directory:
    root_dir = os.path.dirname(os.path.dirname(_HERE))

    # Create a PEP440 compliant version file.
    version_file_path = os.path.join(root_dir, 'share', _VERSION_FILE_NAME)
    with open(version_file_path) as vin:
        version = vin.read().replace('-', '+')
    with open(os.path.join(_AVRO_DIR, _VERSION_FILE_NAME), 'w') as vout:
        vout.write(version)

    # Copy necessary resources files:
    avsc_files = (
        (('schemas', 'org', 'apache', 'avro', 'ipc', 'HandshakeRequest.avsc'), ('',)),
        (('schemas', 'org', 'apache', 'avro', 'ipc', 'HandshakeResponse.avsc'), ('',)),
        (('test', 'schemas', 'interop.avsc'), ('..', '..', 'test')),
    )

    for src, dst in avsc_files:
        src = os.path.join(root_dir, 'share', *src)
        dst = os.path.join(_AVRO_DIR, *dst)
        distutils.file_util.copy_file(src, dst)

    # Make the avro-tools jar available for tests.
    raw_version = _get_raw_version()
    jar_path = os.path.join(root_dir, 'lang', 'java', 'tools', 'target',
                            'avro-tools-{}.jar'.format(raw_version))
    distutils.file_util.copy_file(jar_path, 'test')


def _get_raw_version():
  curdir = os.getcwd()
  version_file = ("VERSION.txt" if os.path.isfile("VERSION.txt")
    else os.path.join(curdir[:curdir.index("lang/py")], "share/VERSION.txt"))
  with open(version_file) as verfile:
    return verfile.read().strip()

def _get_version():
  """To follow the naming convention defined by PEP 440
  in the case that the version is like 'x.y.z-SNAPSHOT'"""
  return _get_raw_version().lower().replace("-", "+")


class LintCommand(setuptools.Command):
    """Run pycodestyle on all your modules"""
    description = __doc__
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # setuptools does not seem to make pycodestyle available
        # in the pythonpath, so we do it ourselves.
        try:
            env = {'PYTHONPATH': next(glob.iglob('.eggs/pycodestyle-*.egg'))}
        except StopIteration:
            env = None  # pycodestyle is already installed
        p = subprocess.Popen(['python', '-m', 'pycodestyle', '.'], close_fds=True, env=env)
        if p.wait():
            raise distutils.errors.DistutilsError("pycodestyle exited with a nonzero exit code.")

def main():
  if not _is_distribution():
    _generate_package_data()

  setuptools.setup(
    name = 'avro',
    version = _get_version(),
    packages = ['avro'],
    package_dir = {'': 'src'},
    scripts = ["./scripts/avro"],
    setup_requires = [
      'isort',
      'pycodestyle',
    ],
    cmdclass={
      "lint": LintCommand,
    },

    package_data={'avro': ['LICENSE', 'NOTICE']},

    # metadata for upload to PyPI
    author = 'Apache Avro',
    author_email = 'dev@avro.apache.org',
    description = 'Avro is a serialization and RPC framework.',
    license = 'Apache License 2.0',
    keywords = 'avro serialization rpc',
    url = 'https://avro.apache.org/',
    extras_require = {
      'snappy': ['python-snappy'],
      'zstandard': ['zstandard'],
    },
  )

if __name__ == '__main__':
  main()
