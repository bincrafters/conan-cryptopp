from conans import ConanFile, CMake
from conans import tools
import os


class CryptoPPConan(ConanFile):
    name = "cryptopp"
    version = "5.6.5"
    url = "https://github.com/bincrafters/conan-cryptopp"
    description = "Crypto++ Library is a free C++ class library of cryptographic schemes."
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    license = "https://github.com/weidai11/cryptopp/blob/master/License.txt"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, 'fPIC': True}
    exports_sources = ["CMakeLists.txt", "a0f91aeb2587.patch"]
    _source_subfolder = "sources"

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        zipname = 'CRYPTOPP_5_6_5.tar.gz'
        tools.get('https://github.com/weidai11/cryptopp/archive/%s' % zipname)
        os.rename("cryptopp-CRYPTOPP_5_6_5", self._source_subfolder)
        tools.patch(patch_file="a0f91aeb2587.patch", base_path=self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        if self.settings.os == "Windows":
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = self.options.shared
        cmake.definitions["BUILD_STATIC"] = not self.options.shared
        cmake.definitions["BUILD_SHARED"] = self.options.shared
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["BUILD_DOCUMENTATION"] = False
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy(pattern="License*", dst="licenses", src=self._source_subfolder, ignore_case=True, keep_path=False)
        self.copy(pattern="*.h", dst="include/cryptopp", src=".", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=".", keep_path=False, symlinks=True)
        self.copy(pattern="*.dll", dst="bin", src=".", keep_path=False)
        if self.settings.build_type == "Debug":
            self.copy(pattern="*.pdb", dst="bin", src=".", keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=".", keep_path=False, symlinks=True)
        self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=".", keep_path=False)

    def package_info(self):
        if str(self.settings.compiler) != "Visual Studio":
            self.cpp_info.libs = ["cryptopp"]
        else:
            if self.options.shared:
                self.cpp_info.libs = ["cryptopp-shared"]
            else:
                self.cpp_info.libs = ["cryptopp-static"]
