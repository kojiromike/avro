#!/bin/sh

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ===========================================================================
# Shell functions that can be used in this script or exported by using
# . build.sh

change_java_version() {
  jdk=$1
  if [ "$jdk" -ge 0 ] && [ -d "/usr/local/openjdk-$jdk" ]; then
    export JAVA_HOME=/usr/local/openjdk-$jdk
    export PATH=$JAVA_HOME/bin:$PATH
    echo "----------------------"
    echo "Java version switched:"
  else
    echo "Using the current Java version:"
  fi
  echo "  JAVA_HOME=$JAVA_HOME"
  echo "  PATH=$PATH"
  java -version
}

# Stop here if sourcing for functions
case "$0" in
  *sh) return;;
esac

# ===========================================================================

set -xe
cd "${0%/*}"

usage() {
  echo "Usage: $0 {lint|test|dist|sign|clean|veryclean|docker [--args \"docker-args\"]|rat|githooks|docker-test}"
  exit 1
}

_run_in() (
  d="$1"
  shift
  cd "$d" && exec "$@"
)

lint() {
  for lang_dir in lang/*; do
    _run_in "$lang_dir" ./build.sh lint
  done
}

test_() {
  # run lang-specific tests
  _run_in lang/java ./build.sh test

  # create interop test data
  mkdir -p build/interop/data
  _run_in lang/java/avro mvn -B -P interop-data-generate generate-resources

  # install java artifacts required by other builds and interop tests
  mvn -B install -DskipTests
  _run_in lang/py ./build.sh lint test
  _run_in lang/py3 ./build.sh lint test
  _run_in lang/c ./build.sh test
  _run_in lang/c++ ./build.sh test
  _run_in lang/csharp ./build.sh test
  _run_in lang/js ./build.sh lint test
  _run_in lang/ruby ./build.sh lint test
  _run_in lang/php ./build.sh test
  _run_in lang/perl ./build.sh lint test

  _run_in lang/py ./build.sh interop-data-generate
  _run_in lang/py3 python3 setup.py generate_interop_data \
    --schema-file=../../share/test/schemas/interop.avsc \
    --output-path=../../build/interop/data
  _run_in lang/c ./build.sh interop-data-generate
  # _run_in lang/c++ make interop-data-generate
  _run_in lang/csharp ./build.sh interop-data-generate
  _run_in lang/js ./build.sh interop-data-generate
  _run_in lang/ruby rake generate_interop
  _run_in lang/php ./build.sh interop-data-generate
  _run_in lang/perl ./build.sh interop-data-generate

  # run interop data tests
  _run_in lang/java/ipc mvn -B test -P interop-data-test
  _run_in lang/py ./build.sh interop-data-test
  _run_in lang/py3 python3 setup.py test --test-suite avro.tests.test_datafile_interop.TestDataFileInterop
  _run_in lang/c ./build.sh interop-data-test
  # _run_in lang/c++ make interop-data-test
  _run_in lang/csharp ./build.sh interop-data-test
  _run_in lang/js ./build.sh interop-data-test
  _run_in lang/ruby rake interop
  _run_in lang/php ./build.sh test-interop
  _run_in lang/perl ./build.sh interop-data-test

  # java needs to package the jars for the interop rpc tests
  _run_in lang/java/tools mvn -B package -DskipTests

  # run interop rpc test
  ./share/test/interop/bin/test_rpc_interop.sh
}

dist() {
  # build source tarball
  mkdir -p build

  SRC_DIR=avro-src-$VERSION
  DOC_DIR=avro-doc-$VERSION

  rm -rf "build/$SRC_DIR"
  if [ -d .svn ]; then
    svn export --force . "build/$SRC_DIR"
  elif [ -d .git ]; then
    mkdir -p "build/$SRC_DIR"
    git archive HEAD | tar -xC "build/$SRC_DIR"
  else
    echo 'Not SVN and not GIT .. cannot continue' >&2
    exit 255
  fi

  # runs RAT on artifacts
  mvn -N -P rat antrun:run verify

  mkdir -p dist
  tar -czC build -f "../dist/${SRC_DIR}.tar.gz" "$SRC_DIR"

  # build lang-specific artifacts
  _run_in lang/java ./build.sh dist
  _run_in lang/java mvn install -pl tools -am -DskipTests
  _run_in lang/java/trevni/doc mvn site
  mvn -N -P copy-artifacts antrun:run

  _run_in lang/py ./build.sh dist
  _run_in lang/py3 ./build.sh dist
  _run_in lang/c ./build.sh dist
  _run_in lang/c++ ./build.sh dist
  _run_in lang/csharp ./build.sh dist
  _run_in lang/js ./build.sh dist
  _run_in lang/ruby ./build.sh dist
  _run_in lang/php ./build.sh dist

  mkdir -p dist/perl
  _run_in lang/perl ./build.sh dist
  cp "lang/perl/Avro-$VERSION.tar.gz" dist/perl/

  # build docs
  _run_in doc ant
  # add LICENSE and NOTICE for docs
  mkdir -p "build/$DOC_DIR"
  cp doc/LICENSE "build/$DOC_DIR"
  cp doc/NOTICE "build/$DOC_DIR"
  _run_in build tar czf "../dist/avro-doc-$VERSION.tar.gz" "$DOC_DIR"

  cp DIST_README.txt dist/README.txt
}

sign() {
  set +x
  printf 'Enter password: '
  stty -echo
  read -r password
  stty echo

  for file in dist/* dist/*/*; do
    case "${file##.*}" in
      md5|sha1|sha512|sha256|asc|txt) :;;
      *) _run_in "${file%/*}" shasum -a 512 "${file##*/}" > "$file.sha512"
         gpg --passphrase "$password" --armor --output "$file.asc" --detach-sig "$file"
         ;;
     esac
  done
  set -x
}
clean() {
  for lang in lang/*/; do
    _run_in "$lang" ./build.sh clean
  done
  _run_in doc ant clean
  mvn -B clean
  rm -rf build \
         dist \
         lang/java/*/userlogs/ \
         lang/java/*/dependency-reduced-pom.xml
}

veryclean() {
  clean
  rm -rf lang/c++/build \
         lang/csharp/src/apache/ipc.test/bin/ \
         lang/csharp/src/apache/ipc.test/obj \
         lang/js/node_modules \
         lang/perl/inc/ \
         lang/py/lib/ivy-2.2.0.jar \
         lang/ruby/.gem/ \
         lang/ruby/Gemfile.lock
}

docker_() {
  case "$1" in
    --args*) DOCKER_XTRA_ARGS=$2
             shift 2;;
  esac
  if [ "$(uname -s)" = Linux ]; then
    USER_NAME=${SUDO_USER:=$USER}
    USER_ID=$(id -u "$USER_NAME")
    GROUP_ID=$(id -g "$USER_NAME")
  else # boot2docker uid and gid
    USER_NAME=$USER
    USER_ID=1000
    GROUP_ID=50
  fi
  {
    cat share/docker/Dockerfile
    grep -vF 'FROM avro-build-ci' share/docker/DockerfileLocal
    echo "ENV HOME /home/$USER_NAME"
    echo "RUN getent group $GROUP_ID || groupadd -g $GROUP_ID $USER_NAME"
    echo "RUN getent passwd $USER_ID || useradd -g $GROUP_ID -u $USER_ID -k /root -m $USER_NAME"
  } > Dockerfile
  tar -cf- lang/ruby/Gemfile Dockerfile | docker build -t "avro-build-$USER_NAME" -
  rm Dockerfile
  # By mapping the .m2 directory you can do an mvn install from
  # within the container and use the result on your normal
  # system.  And this also is a significant speedup in subsequent
  # builds because the dependencies are downloaded only once.
  #
  # On OSX, it's highly suggested to set an env variable of:
  # export DOCKER_MOUNT_FLAG=":delegated"
  # Using :delegated will drop the "mvn install" time from over 30 minutes
  # down to under 10.  However, editing files from OSX may take a few
  # extra second before the changes are available within the docker container.

  # shellcheck disable=SC2086
  docker run --rm -t -i \
             --env "JAVA=${JAVA:-8}" \
             -v "${PWD}:/home/${USER_NAME}/avro${DOCKER_MOUNT_FLAG}" \
             -w "/home/${USER_NAME}/avro" \
             -v "${HOME}/.m2:/home/${USER_NAME}/.m2${DOCKER_MOUNT_FLAG}" \
             -v "${HOME}/.gnupg:/home/${USER_NAME}/.gnupg" \
             -u "$USER_NAME" \
             ${DOCKER_XTRA_ARGS} \
             "avro-build-${USER_NAME}" bash
}

rat() {
  mvn test -Dmaven.main.skip=true -Dmaven.test.skip=true -DskipTests=true -P rat -pl :avro-toplevel
}

githooks() {
  echo "Installing AVRO git hooks."
  for hook in share/githooks/*; do
    cp "$hook" .git/hooks
    chmod +x ".git/hooks/${hook##*/}"
  done
}

docker_test() {
  tar -cf- share/docker/Dockerfile \
           lang/ruby/Gemfile |
    docker build -t avro-test -f share/docker/Dockerfile -
  docker run --rm -v "${PWD}:/avro/" --env "JAVA=${JAVA:-8}" avro-test /avro/share/docker/run-tests.sh
}

main() {
  read -r VERSION < share/VERSION.txt
  [ $# -ge 0 ] || usage

  while [ -n "$1" ]; do
    target="$1"
    shift

    # Change the JDK from the default for all targets that will eventually require Java (or maven).
    # This only occurs when the JAVA environment variable is set and a Java environment exists in
    # the "standard" location (defined by the openjdk docker images).  This will typically occur in CI
    # builds.  In all other cases, the Java version is taken from the current installation for the user.
    case "$target" in
      lint|test|dist|clean|veryclean|rat) change_java_version "$JAVA";;
    esac

    case "$target" in
      lint) lint;;
      test) test_;;
      dist) dist;;
      sign) sign;;
      clean) clean;;
      veryclean) veryclean;;
      docker) docker_ "$@";;
      rat) rat;;
      githooks) githooks;;
      docker-test) docker_test;;
      --args*) :;;  # Ignore outside of docker_
      *) usage;;
    esac
  done
}

main "$@"
