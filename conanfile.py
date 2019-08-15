#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class CryptoPPConan(ConanFile):
    name = "cryptopp"
    version = "8.2.0"
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
    exports_sources = ["CMakeLists.txt", "CMakeLists.original.txt", "cryptopp-config.cmake"]
    exports = "LICENSE.md"
    _source_subfolder = "source_subfolder"

    def source(self):
        archive_file = 'CRYPTOPP_%s' % self.version.replace('.', '_')
        sha256 = "e3bcd48a62739ad179ad8064b523346abb53767bcbefc01fe37303412292343e"
        tools.get("{}/archive/{}.tar.gz".format(self.homepage, archive_file), sha256=sha256)
        os.rename("cryptopp-%s" % archive_file, self._source_subfolder)
        shutil.move("CMakeLists.original.txt", os.path.join(self._source_subfolder, "CMakeLists.txt"))
        shutil.move("cryptopp-config.cmake", os.path.join(self._source_subfolder, "cryptopp-config.cmake"))
        if self.settings.os == 'Android' and 'ANDROID_NDK_HOME' in os.environ:
            shutil.copyfile(os.environ['ANDROID_NDK_HOME'] + '/sources/android/cpufeatures/cpu-features.h', os.path.join(self._source_subfolder, "cpu-features.h"))

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
        if self.settings.os == 'Android':
            cmake.definitions["CRYPTOPP_NATIVE_ARCH"] = True
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
