#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class CryptoPPConan(ConanFile):
    name = "cryptopp"
    version = "7.0.0"
    url = "https://github.com/bincrafters/conan-cryptopp"
    homepage = "https://github.com/weidai11/cryptopp"
    license = "BSL-1.0"
    description = "Crypto++ Library is a free C++ class library of cryptographic schemes."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    generators = "cmake"
    exports_sources = ["CMakeLists.txt", "CMakeLists.original.txt"]
    exports = "LICENSE.md"
    source_subfolder = "source_subfolder"

    def source(self):
        archive_file = 'CRYPTOPP_7_0_0'
        url = 'https://github.com/weidai11/cryptopp/archive/%s.tar.gz' % archive_file
        tools.get(url)
        os.rename("cryptopp-%s" % archive_file, self.source_subfolder)
        shutil.move("CMakeLists.original.txt", os.path.join(self.source_subfolder, "CMakeLists.txt"))

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure_cmake(self):
        cmake = CMake(self)
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        else:
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = self.options.shared
        cmake.definitions["BUILD_STATIC"] = not self.options.shared
        cmake.definitions["BUILD_SHARED"] = self.options.shared
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["BUILD_DOCUMENTATION"] = False
        cmake.configure()
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="License.txt", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
