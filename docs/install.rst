Install
=======

With uv (recommended):

.. code-block:: bash

   uv add picoio

With pip:

.. code-block:: bash

   pip install picoio

Requirements: Python >= 3.13. For building from source, system libraries may be
needed (e.g. ``libzip-dev`` on Debian/Ubuntu for the ZIP extension).

Build from source (Cython + pybind11 extensions):

.. code-block:: bash

   uv sync --extra dev
   uv pip install -e .
