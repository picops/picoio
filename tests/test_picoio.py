"""Basic pytest tests for picoio: JSON, TOML, Arrow, ZIP."""

import io
import zipfile

import pytest

import picoio


def test_read_json_write_json_roundtrip(tmp_path):
    path = tmp_path / "out.json"
    data = {"a": 1, "b": [2, 3], "s": "hello"}
    picoio.write_json(str(path), data)
    assert picoio.read_json(str(path)) == data


def test_read_json_missing_file():
    with pytest.raises(FileNotFoundError):
        picoio.read_json("/nonexistent/file.json")


def test_read_toml_write_toml_roundtrip(tmp_path):
    path = tmp_path / "out.toml"
    data = {"title": "test", "count": 42, "items": [1, 2]}
    picoio.write_toml(str(path), data)
    assert picoio.read_toml(str(path)) == data


def test_read_toml_missing_file():
    with pytest.raises(FileNotFoundError):
        picoio.read_toml("/nonexistent/file.toml")


def test_read_csv_bytes():
    content = b"a,b,c\n1,2,3\n4,5,6"
    table = picoio.read_csv_bytes(content)
    assert table.num_rows == 2
    assert table.column_names == ["a", "b", "c"]


def test_pa_file_exists(tmp_path):
    import pyarrow.fs as pafs

    (tmp_path / "here.txt").write_text("x")
    local_fs = pafs.LocalFileSystem()
    assert picoio.pa_file_exists(local_fs, str(tmp_path / "here.txt")) is True


def test_pa_write_parquet_table(tmp_path):
    import pyarrow as pa

    table = pa.table({"x": [1, 2, 3], "y": ["a", "b", "c"]})
    path = tmp_path / "out.parquet"
    picoio.pa_write_parquet_table(table, str(path))
    assert path.exists()
    back = pa.parquet.read_table(str(path))
    assert back.equals(table)


def test_extract_zip_and_zipfile():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("hello.txt", b"hello world")
        zf.writestr("nested/other.txt", b"other")
    zip_bytes = buf.getvalue()

    entries = picoio.extract_zip(zip_bytes)
    assert len(entries) == 2
    names = {e.filename for e in entries}
    assert "hello.txt" in names
    assert "nested/other.txt" in names

    for e in entries:
        if e.filename == "hello.txt":
            assert e.get_data_as_bytes() == b"hello world"
        elif e.filename == "nested/other.txt":
            assert e.get_data_as_bytes() == b"other"


def test_picoio_all_exports():
    expected = {
        "read_csv_bytes",
        "pa_write_parquet_table",
        "pa_file_exists",
        "read_toml",
        "write_toml",
        "read_json",
        "write_json",
        "ZipFile",
        "extract_zip",
    }
    for name in expected:
        assert hasattr(picoio, name), f"picoio.{name} should be exported"
