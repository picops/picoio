import io

import pyarrow.csv as pacsv
import pyarrow.parquet as pq

from libcpp.memory cimport shared_ptr
from pyarrow._csv cimport ConvertOptions, ReadOptions
from pyarrow._fs cimport FileSystem
from pyarrow.includes.libarrow_fs cimport CFileSystem
from pyarrow.lib cimport Table


cpdef bint pa_file_exists(object fs, str file_path) except *:
    cdef shared_ptr[CFileSystem] c_fs
    
    if not isinstance(fs, FileSystem):
        raise TypeError("fs must be a pyarrow.fs.FileSystem instance")
        
    c_fs = (<FileSystem>fs).unwrap()
    
    try:
        result = c_fs.get().GetFileInfo(file_path.encode('utf8'))
        if not result.ok():
            return False
        return True
    except Exception as e:
        if "NO_SUCH_KEY" in str(e) or "NoSuchKey" in str(e):
            return False
        raise RuntimeError(f"Error checking file existence: {e}")


cpdef Table read_csv_bytes(
    bytes content,
    ReadOptions read_options = None,
    ConvertOptions convert_options = None,
):
    bytes_io = io.BytesIO(content)
    
    if read_options is None:
        read_options = ReadOptions()
    if convert_options is None:
        convert_options = ConvertOptions()

    return pacsv.read_csv(
        bytes_io,
        read_options=read_options,
        convert_options=convert_options
    )

cpdef void pa_write_parquet_table(
    Table table,
    str path,
    object filesystem = None,
    str compression = None,
):
    pq.write_table(
            table,
            path,
            filesystem=filesystem,
            compression=compression
        )