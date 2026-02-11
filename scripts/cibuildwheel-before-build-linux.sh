#!/usr/bin/env bash
# Runs inside manylinux/musllinux container before each wheel build.
# Mirrors system deps from scripts/install-deps.sh (libzip, zeromq, etc.).
# Arrow + all required expansions (parquet, dataset, etc.) come from the pyarrow wheel.
# Use with CIBW_BUILD_FRONTEND_ARGS="--no-isolation".
set -e

# --- System libs (match install-deps.sh: libzip, zeromq; compiler/cmake are in image) ---
# manylinux: RHEL/CentOS → dnf/yum; musllinux: Alpine → apk
if command -v dnf &>/dev/null; then
  dnf install -y libzip-devel zeromq-devel || yum install -y libzip-devel zeromq-devel
elif command -v apk &>/dev/null; then
  apk add --no-cache libzip-dev libzmq-dev
fi

# --- Python build deps (pyarrow wheel = Arrow + parquet/dataset/etc. like install-deps.sh) ---
pip install -q setuptools wheel Cython numpy pyarrow pybind11 "picobuild==0.0.5b1"

# --- Linker: find Arrow C++ libs from pyarrow wheel (same role as libarrow-dev in install-deps.sh) ---
ARROW_LIB=$(python -c "import pyarrow, os; d=os.path.join(os.path.dirname(pyarrow.__file__), 'lib'); print(d if os.path.isdir(d) else os.path.dirname(pyarrow.__file__))")
export LIBRARY_PATH="${ARROW_LIB}${LIBRARY_PATH:+:${LIBRARY_PATH}}"
