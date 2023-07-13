#
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get, copy, patch
from conan.tools.build import check_min_cppstd
from conan.tools.scm import Version
from conan.tools.microsoft import is_msvc_static_runtime
import functools
import os
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.layout import basic_layout
from conan.tools.files import get

required_conan_version = ">=1.59.0"

#REMOVE_FOR_CCI BEGIN
# This recipe contains sections that will not be approved by Conan Center Index reviewers.
# All code between the BEGIN/END comments should be removed before submitting this recipe to CCI
#
# Options:
#   branch_version - Default: False.  Set to True to have recipe use the supplied version as a branch/tag/release name 
#                    to pull source from the client-cpp repo, instead of the usual static entry in the conandata.yml list.
#                    Once the specified version has been built to the local cache, it can be consumed 
#                    by other projects using that same name as the version
#
#                    Examples: 
#                    Build from the 1.4.0 release tag in client-cpp:
#                    conan create recipe/all opentdf-client/1.4.0@ --build=opentdf-client --build=missing -o opentdf-client:branch_version=True
#                    Consume from cache:
#                    self.requires("opentdf-client/1.4.0@")
#
#                    Build from the PLAT-1234-my-changes branch in client-cpp:
#                    conan create recipe/all opentdf-client/PLAT-1234-my-changes@ --build=opentdf-client --build=missing -o opentdf-client:branch_version=True
#                    Consume from cache:
#                    self.requires("opentdf-client/PLAT-1234-changes@")
#REMOVE_FOR_CCI END

class OpenTDFConan(ConanFile):
    name = "opentdf-client"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.virtru.com"
    topics = ("opentdf", "opentdf-client", "tdf", "virtru")
    description = "openTDF core c++ client library for creating and accessing TDF protected data"
    license = "BSD-3-Clause-Clear"
    package_type = "library"
    generators = "CMakeToolchain", "CMakeDeps"
    settings = "os", "arch", "compiler", "build_type"
    options = {"fPIC": [True, False], "shared": [True, False]}
    default_options = {"fPIC": True, "shared": True}
    #REMOVE_FOR_CCI BEGIN
    options = {"fPIC": [True, False], "shared": [True, False], "branch_version": [True, False]}
    default_options = {"fPIC": True, "shared": True, "branch_version": False}
    #REMOVE_FOR_CCI END

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    @property
    def _minimum_cpp_standard(self):
        return 17

    @property
    def _minimum_compilers_version(self):
        return {
            "Visual Studio": "17" if Version(self.version) < "1.1.5" else "15",
            "msvc": "193" if Version(self.version) < "1.1.5" else "191",
            "gcc": "7.5.0",
            "clang": "12",
            "apple-clang": "12.0.0",
        }

    #REMOVE_FOR_CCI BEGIN
    @property
    def is_branch_version(self):
        try:
            return self.options.branch_version
        except:
            return self.info.options.branch_version
    #REMOVE_FOR_CCI END

    def layout(self):
        #basic_layout(self, src_folder=self._source_subfolder)
        cmake_layout(self)

    def export_sources(self):
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)
        for data in self.conan_data.get("patches", {}).get(self.version, []):
            copy(self, data["patch_file"], self.recipe_folder, self.export_sources_folder)

    def validate(self):
        # check minimum cpp standard supported by compiler
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._minimum_cpp_standard)
        # check minimum version of compiler
        min_version = self._minimum_compilers_version.get(str(self.settings.compiler))
        if not min_version:
            self.output.warn(f'{self.name} recipe lacks information about the {self.settings.compiler} compiler support.')
        else:
            if Version(self.settings.compiler.version) < min_version:
                raise ConanInvalidConfiguration(f'{self.name} requires {self.settings.compiler} {self.settings.compiler.version} but found {min_version}')
        # Disallow MT and MTd
        if is_msvc_static_runtime(self):
            raise ConanInvalidConfiguration(f'{self.name} can not be built with MT or MTd at this time')

    def requirements(self):
        self.requires("openssl/1.1.1s")
        self.requires("ms-gsl/2.1.0")
        self.requires("nlohmann_json/3.11.1")
        self.requires("jwt-cpp/0.4.0")
        # Use magic_enum after 1.3.10
        if Version(self.version) > "1.3.10":
            self.requires("magic_enum/0.8.2")
        # Use newer boost+libxml2 after 1.3.6
        if Version(self.version) <= "1.3.6":
            self.requires("boost/1.79.0")
            self.requires("libxml2/2.9.14")
        else:
            self.requires("boost/1.81.0")
            self.requires("libxml2/2.10.3")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
        if self.options.shared:
            del self.options.fPIC

    def source(self):
    #REMOVE_FOR_CCI BEGIN
        if self.is_branch_version:
            #self.output.warn("Building branch_version = {}".format(self.version))
            self.run("git clone https://github.com/opentdf/client-cpp.git --depth 1 --branch " + self.version + " " + self._source_subfolder)
        else:
    #REMOVE_FOR_CCI END
            get(**self.conan_data["sources"][self.version], destination=self._source_subfolder, strip_root=True)

    def _patch_sources(self):
        for data in self.conan_data.get("patches", {}).get(self.version, []):
            patch(self, **data)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "*", dst=os.path.join(self.package_folder, "lib"), src=os.path.join(os.path.join(self._source_subfolder,"tdf-lib-cpp"), "lib"), keep_path=False)
        copy(self, "*", dst=os.path.join(self.package_folder, "include"), src=os.path.join(os.path.join(self._source_subfolder,"tdf-lib-cpp"), "include"), keep_path=False)
        copy(self, "LICENSE", dst=os.path.join(self.package_folder, "licenses"), src=self._source_subfolder, ignore_case=True, keep_path=False)

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "opentdf-client")
        self.cpp_info.set_property("cmake_target_name", "opentdf-client::opentdf-client")
        self.cpp_info.set_property("pkg_config_name", "opentdf-client")

        self.cpp_info.libdirs=[os.path.join(os.path.join(self._source_subfolder,"tdf-lib-cpp"), "lib")]
        self.cpp_info.includedirs=[os.path.join(os.path.join(self._source_subfolder,"tdf-lib-cpp"), "include")]

        if self.options.shared:
            self.cpp_info.components["libopentdf"].libs = ["opentdf"]
        else:
            self.cpp_info.components["libopentdf"].libs = ["opentdf_static"]

        self.cpp_info.components["libopentdf"].set_property("cmake_target_name", "opentdf-client::opentdf-client")
        self.cpp_info.components["libopentdf"].names["cmake_find_package"] = "opentdf-client"
        self.cpp_info.components["libopentdf"].names["cmake_find_package_multi"] = "opentdf-client"
        self.cpp_info.components["libopentdf"].names["pkg_config"] = "opentdf-client"
        self.cpp_info.components["libopentdf"].requires = ["openssl::openssl", "boost::boost", "ms-gsl::ms-gsl", "libxml2::libxml2", "jwt-cpp::jwt-cpp", "nlohmann_json::nlohmann_json", "magic_enum::magic_enum"]
