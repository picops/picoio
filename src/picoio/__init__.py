"""CPython file I/O utilities: Arrow (Parquet/CSV), JSON, TOML, and ZIP."""

from .arrow import pa_file_exists, pa_write_parquet_table, read_csv_bytes
from .json import read_json, write_json
from .toml import read_toml, write_toml
from .zip import ZipFile, extract_zip

__all__: tuple[str, ...] = (
    # Arrow
    "read_csv_bytes",
    "pa_write_parquet_table",
    "pa_file_exists",
    # TOML
    "read_toml",
    "write_toml",
    # JSON
    "read_json",
    "write_json",
    # ZIP
    "ZipFile",
    "extract_zip",
)
