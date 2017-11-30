from conans import ConanFile, ConfigureEnvironment, VisualStudioBuildEnvironment
from conans import tools
import os

class CryptoPPConan(ConanFile):
    name = "cryptopp"
    version = "5.6.5"
    url = "https://github.com/bincrafters/conan-cryptopp"
    description = "Crypto++ Library is a free C++ class library of cryptographic schemes."
    settings = "os", "compiler", "build_type", "arch"
    license = "Boost Software License 1.0"
    options = {"shared": [True, False]}
    default_options = "shared=True"

    def source(self):
        zipname = 'cryptopp565.zip'
        url = 'http://cryptopp.com/%s' % zipname
        sha256 = 'a75ef486fe3128008bbb201efee3dcdcffbe791120952910883b26337ec32c34'
        tools.download(url, zipname)
        tools.check_sha256(zipname, sha256)
        tools.unzip(zipname)
        os.unlink(zipname)

        bad_lines = (
            "msbuild /t:Build /p:Configuration=Debug;Platform=Win32 cryptlib.vcxproj",
            "msbuild /t:Build /p:Configuration=Debug;Platform=Win32 cryptest.vcxproj",
            "Win32\\output\\debug\\cryptest.exe mac_dll \"$(TargetPath)\"",
            "IF %ERRORLEVEL% EQU 0 (echo mac done &gt; \"$(OutDir)\"\\cryptopp.mac.done)")
        for line in bad_lines:
            tools.replace_in_file("cryptdll.vcxproj", search=line, replace="", strict=True)

    def makefile_build(self):
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        if self.options.shared:
            self.run('%s make dynamic' % env.command_line)
        else:
            self.run('%s make static' % env.command_line)
        if self.scope.build_tests:
            self.run('%s make test check' % env.command_line)

    def msvc_build(self):
        env = VisualStudioBuildEnvironment(self)
        with tools.environment_append(env.vars):
            vcvars = tools.vcvars_command(self.settings)

            build_command = tools.build_sln_command(self.settings, "cryptest.sln")
            build_command = build_command.replace("x86", "Win32")

            if self.options.shared:
                build_command = build_command.replace('%s' % self.settings.build_type,
                                                          '"DLL-Import %s"' % self.settings.build_type)
            self.output.info("Build command: %s" % build_command)
            self.run("%s && %s" % (vcvars, build_command))

    def build(self):
        if str(self.settings.os) != "Windows":
            return self.makefile_build()
        else:
            return self.msvc_build()

    def package(self):
        self.copy(pattern="*.h", dst="include/cryptopp", src=".")
        self.copy(pattern="*.so", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=".", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=".", keep_path=False)

    def package_info(self):
        if str(self.settings.compiler) != "Visual Studio":
            self.cpp_info.libs = ["cryptopp"]
        else:
            if self.options.shared:
                self.cpp_info.libs = ["cryptopp"]
            else:
                self.cpp_info.libs = ["cryptlib"]
