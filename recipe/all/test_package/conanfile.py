from conan import ConanFile
from conan.tools.build import cross_building
import os
from conan.tools.scm import Version
from conan import __version__ as conan_version

if conan_version < Version("2.0.0"):
    from conans import CMake
else:
    from conan.tools.layout import basic_layout
    from conan.tools.files import get

class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    if conan_version < Version("2.0.0"):
        generators = "cmake", "cmake_find_package_multi"
    else:
        generators = "CMakeToolchain", "CMakeDeps"

    if conan_version < Version("2.0.0"):
        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

    else:
        def requirements(self):
            self.requires(self.tested_reference_str)

    def test(self):
        if not cross_building(self):
            if conan_version < Version("2.0.0"):
                bin_path = os.path.join("bin", "test_package")
                self.run(bin_path, run_environment=True)
            else:
                bin_path = os.path.join(self.cpp.build.bindir, "test_package")
                self.run(bin_path, env="test")
