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
    author = "Bincrafters <bincrafters@gmail.com>"
    description = "Crypto++ Library is a free C++ class library of cryptographic schemes."
    topics = ("conan", "cryptopp", "crypto", "cryptographic", "security")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, 'fPIC': True}
    generators = "cmake"
    exports_sources = ["CMakeLists.txt", "CMakeLists.original.txt", "a0f91aeb2587.patch", "cryptopp-config.cmake"]
    exports = "LICENSE.md"
    _source_subfolder = "source_subfolder"

    def source(self):
        archive_file = 'CRYPTOPP_%s' % self.version.replace('.', '_')
        sha256 = "3ee97903882b5f58c88b6f9d2ce50fd1000be95479180c7b4681cd3f4c1c7629"
        tools.get("{}/archive/{}.tar.gz".format(self.homepage, archive_file), sha256=sha256)
        os.rename("cryptopp-%s" % archive_file, self._source_subfolder)
        shutil.move("CMakeLists.original.txt", os.path.join(self._source_subfolder, "CMakeLists.txt"))
        tools.patch(patch_file="a0f91aeb2587.patch", base_path=self._source_subfolder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def _configure_cmake(self):
        cmake = CMake(self)
        if self.settings.os == "Windows":
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = self.options.shared
        cmake.definitions["BUILD_STATIC"] = not self.options.shared
        cmake.definitions["BUILD_SHARED"] = self.options.shared
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["BUILD_DOCUMENTATION"] = False
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="License.txt", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
