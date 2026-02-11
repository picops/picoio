import os
import subprocess

import numpy as np
import pyarrow
import pybind11
from picobuild import get_cython_build_dir, Extension, find_packages, setup, cythonize


def _arrow_system_lib_dirs():
    """If system Arrow (arrow-devel) is installed, return its library dirs for the linker."""
    try:
        out = subprocess.run(
            ["pkg-config", "--libs-only-L", "arrow"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if out.returncode != 0 or not out.stdout:
            return []
        # -L/path -> /path
        return [p.strip().removeprefix("-L") for p in out.stdout.strip().split() if p.startswith("-L")]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []


# PyArrow wheel bundles Arrow C++ libs; ensure linker can find them (package dir + lib/ subdir).
# When arrow-devel is installed (e.g. on host), add system Arrow lib dirs so -larrow is found.
_arrow_lib_dirs = list(pyarrow.get_library_dirs())
_arrow_pkg = os.path.dirname(pyarrow.__file__)
if _arrow_pkg not in _arrow_lib_dirs:
    _arrow_lib_dirs.append(_arrow_pkg)
_arrow_lib = os.path.join(_arrow_pkg, "lib")
if os.path.isdir(_arrow_lib) and _arrow_lib not in _arrow_lib_dirs:
    _arrow_lib_dirs.append(_arrow_lib)
for d in _arrow_system_lib_dirs():
    if d and d not in _arrow_lib_dirs:
        _arrow_lib_dirs.append(d)

# In manylinux/cibuildwheel the linker often needs LIBRARY_PATH to find pyarrow-bundled libs.
if _arrow_lib_dirs:
    _existing = os.environ.get("LIBRARY_PATH", "")
    os.environ["LIBRARY_PATH"] = os.pathsep.join(_arrow_lib_dirs) + (
        (os.pathsep + _existing) if _existing else ""
    )

# C extensions
c_extensions = []

_cython_opts = {
    "extra_compile_args": [
        "-O3",
        "-march=native",
        "-Wno-unused-function",
        "-Wno-unused-variable",
    ],
    "language": "c++",
}
_cython_directives = {
    "language_level": 3,
    "boundscheck": False,
    "wraparound": False,
    "cdivision": True,
    "infer_types": True,
    "nonecheck": False,
    "initializedcheck": False,
}

# Only arrow.pyx links against Arrow C++; others must not to avoid manylinux linker errors.
_arrow_extra_link_args = [f"-L{d}" for d in _arrow_lib_dirs]
cythonized_extensions = cythonize(
    [
        Extension(
            "picoio.arrow",
            ["src/picoio/arrow.pyx"],
            **_cython_opts,
            libraries=pyarrow.get_libraries(),
            library_dirs=_arrow_lib_dirs,
            extra_link_args=_arrow_extra_link_args,
            include_dirs=[pyarrow.get_include()] + [np.get_include()],
        ),
        Extension(
            "picoio.json",
            ["src/picoio/json.pyx"],
            **_cython_opts,
        ),
        Extension(
            "picoio.toml",
            ["src/picoio/toml.pyx"],
            **_cython_opts,
        ),
        Extension(
            "picoio._experimental.flist",
            ["src/picoio/_experimental/flist.pyx"],
            **_cython_opts,
        ),
    ],
    compiler_directives=_cython_directives,
    build_dir=get_cython_build_dir(),
)

# Pybind extensions
pybind_extensions = [
    Extension(
        "picoio.zip",
        sources=["src/picoio/zip.cpp"],
        include_dirs=[pybind11.get_include()],
        libraries=["zip"],  # This is libzip, libzip.h not libzip.hpp
        language="c++",
        extra_compile_args=[
            "-O3",
            "-march=native",
            "-Wno-unused-function",
            "-Wno-unused-variable",
        ],
    )
]

# Build
if __name__ == "__main__":
    setup(
        packages=find_packages(where="src", include=["picoio", "picoio.*", "picoio._experimental"]),
        package_dir={"": "src"},
        package_data={"picoio": ["**/*.pxd", "**/*.pxi"]},
        ext_modules=c_extensions + cythonized_extensions + pybind_extensions,
    )
