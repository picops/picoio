#!/usr/bin/env bash
# Runs inside manylinux/musllinux before each wheel build. Same deps as install-deps.sh.
# Requires --no-isolation in pyproject.toml.
set -e

# install-deps.sh: build-essential, cmake, libzip-dev, libzmq3-dev, pybind11-dev, Arrow (→ pyarrow pip)
if command -v dnf &>/dev/null; then
  dnf install -y gcc-c++ cmake libzip-devel zeromq-devel
  dnf install -y pybind11-devel 2>/dev/null || true
elif command -v yum &>/dev/null; then
  yum install -y gcc-c++ cmake libzip-devel zeromq-devel
  yum install -y pybind11-devel 2>/dev/null || true
elif command -v apk &>/dev/null; then
  apk add --no-cache build-base cmake libzip-dev libzmq-dev
  apk add --no-cache pybind11-dev 2>/dev/null || true
fi

# Arrow + build deps from pyproject (Arrow C++ = pyarrow wheel; create_library_symlinks so -larrow works)
pip install -q setuptools wheel Cython numpy pyarrow pybind11 "picobuild==0.0.5b1"
python -c "import pyarrow; pyarrow.create_library_symlinks()" 2>/dev/null || true
ARROW_LIB=$(python -c "import pyarrow, os; d=os.path.join(os.path.dirname(pyarrow.__file__), 'lib'); print(d if os.path.isdir(d) else os.path.dirname(pyarrow.__file__))")
export LIBRARY_PATH="${ARROW_LIB}${LIBRARY_PATH:+:${LIBRARY_PATH}}"
