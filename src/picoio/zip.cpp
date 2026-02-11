#include "zip.hpp"
#include <zip.h>
#include <stdexcept>
#include <cstring>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>


namespace py = pybind11;
std::vector<ZipFile> extract_zip(const uint8_t* data, size_t size) {
    zip_source_t *src = zip_source_buffer_create(data, size, 0, nullptr);
    if (src == nullptr) {
        throw std::runtime_error("Failed to create zip source");
    }
    
    zip_t *z = zip_open_from_source(src, 0, nullptr);
    if (z == nullptr) {
        zip_source_free(src);
        throw std::runtime_error("Failed to open ZIP");
    }
    
    std::vector<ZipFile> files;
    zip_int64_t num_files = zip_get_num_entries(z, 0);
    files.reserve(num_files);
    
    for (zip_int64_t i = 0; i < num_files; ++i) {
        zip_stat_t st;
        if (zip_stat_index(z, i, 0, &st) < 0) {
            continue;
        }
        
        std::string filename(st.name);
        if (filename.back() == '/') {
            continue; // Skip directories
        }
        
        zip_file_t *zf = zip_fopen_index(z, i, 0);
        if (zf == nullptr) {
            continue;
        }
        
        std::vector<uint8_t> content(st.size);
        zip_int64_t bytes_read = zip_fread(zf, content.data(), st.size);
        zip_fclose(zf);
        
        if (bytes_read != static_cast<zip_int64_t>(st.size)) {
            continue;
        }
        
        files.push_back({std::move(filename), std::move(content)});
    }
    
    zip_close(z);
    return files;
}


PYBIND11_MODULE(zip, m) {
    py::class_<ZipFile>(m, "ZipFile")
        .def(py::init<>())
        .def_readwrite("filename", &ZipFile::filename)
        .def_readwrite("data", &ZipFile::data)
        .def("get_data_as_bytes", [](const ZipFile& self) -> py::bytes {
            return py::bytes(reinterpret_cast<const char*>(self.data.data()), self.data.size());
        }, "Get data as Python bytes object (slower but readable)");
    
    m.def("extract_zip", [](py::bytes py_data) {
        const char* data = PyBytes_AsString(py_data.ptr());
        size_t size = PyBytes_Size(py_data.ptr());
        return extract_zip(reinterpret_cast<const uint8_t*>(data), size);
    }, py::arg("data"));
}