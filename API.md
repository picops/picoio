# picoio API

CPython file I/O utilities: Arrow (Parquet/CSV), JSON, TOML, and ZIP.

---

## Arrow

### `pa_file_exists(fs, file_path) -> bool`

Check whether a file exists on a PyArrow filesystem.

- **fs** (`pyarrow.fs.FileSystem`) – The filesystem to query.
- **file_path** (`str`) – Path to the file.
- **Returns:** `True` if the file exists, `False` otherwise.
- **Raises:** `TypeError` if `fs` is not a `pyarrow.fs.FileSystem`. May raise `RuntimeError` on other filesystem errors.

---

### `pa_write_parquet_table(table, path, filesystem=None, compression=None) -> None`

Write a PyArrow table to a Parquet file.

- **table** (`pyarrow.Table`) – Table to write.
- **path** (`str`) – Output path.
- **filesystem** (`pyarrow.fs.FileSystem | None`) – Optional filesystem; default uses local.
- **compression** (`str | None`) – Optional compression (e.g. `"snappy"`, `"gzip"`).

---

### `read_csv_bytes(content, read_options=None, convert_options=None) -> pyarrow.Table`

Parse CSV from raw bytes into a PyArrow table.

- **content** (`bytes`) – CSV data.
- **read_options** (`pyarrow.csv.ReadOptions | None`) – Optional read options.
- **convert_options** (`pyarrow.csv.ConvertOptions | None`) – Optional convert options.
- **Returns:** `pyarrow.Table` built from the CSV.

---

## JSON

### `read_json(file_path) -> dict[str, Any]`

Read a JSON file into a dictionary.

- **file_path** (`str`) – Path to the JSON file.
- **Returns:** Parsed JSON as a dict.
- **Raises:** `FileNotFoundError` if the file cannot be opened.

---

### `write_json(file_path, data) -> None`

Write a dictionary to a JSON file.

- **file_path** (`str`) – Path where to write the file.
- **data** (`dict[str, Any]`) – Data to serialize as JSON.

---

## TOML

### `read_toml(file_path) -> dict[str, Any]`

Read a TOML file into a dictionary.

- **file_path** (`str`) – Path to the TOML file.
- **Returns:** Parsed TOML as a dict.
- **Raises:** `FileNotFoundError` if the file cannot be opened.

---

### `write_toml(file_path, data) -> None`

Write a dictionary to a TOML file.

- **file_path** (`str`) – Path where to write the file.
- **data** (`dict[str, Any]`) – Data to serialize as TOML.
- **Raises:** `IOError` if the file cannot be opened for writing.

---

## ZIP

### `ZipFile`

Represents a single file entry from an extracted ZIP archive.

| Attribute | Type   | Description                    |
|----------|--------|--------------------------------|
| `filename` | `str` | Entry path/name in the archive |
| `data`   | `list[int]` | Raw file bytes (as list of ints for speed) |

**Methods**

- **`get_data_as_bytes() -> bytes`** – Return the entry contents as a `bytes` object.

---

### `extract_zip(data) -> list[ZipFile]`

Parse a ZIP archive from raw bytes and return its file entries.

- **data** (`bytes`) – Full ZIP archive bytes.
- **Returns:** List of `ZipFile` entries (one per file in the archive).

---

## Experimental: `picoio._experimental.flist`

Line-based file readers (API may change).

### `BaseListFileReader`

Base class for reading a file as a list of lines.

**Constructor:** `BaseListFileReader(file_path, strip_lines=True, skip_empty_lines=True, encoding="utf-8", comment_prefix=None, max_line_length=8192)`

- **file_path** – Path to the file.
- **strip_lines** – Strip leading/trailing whitespace from each line.
- **skip_empty_lines** – Omit empty lines from the list.
- **encoding** – Text encoding.
- **comment_prefix** – If set, lines starting with this prefix are treated as comments and skipped.
- **max_line_length** – Maximum line length to read.

**Methods / support**

- **`clear()`** – Clear cached lines.
- **`read(force_reload=False)`** – *(Subclasses only.)* Load or reload lines.
- **`__len__`** – Number of lines.
- **`__getitem__(index)`** – Line at index, or slice of lines.
- **`__iter__`** – Iterate over lines.
- **`__bool__`** – True if there is at least one line.
- **`__repr__`** – String representation.

### `ListFileReader(BaseListFileReader)`

Reads the file with standard I/O. Use **`read(force_reload=False)`** to load or reload lines.

### `ListMMAPFileReader(BaseListFileReader)`

Reads the file via memory-mapped I/O. Use **`read(force_reload=False)`** to load or reload lines.
