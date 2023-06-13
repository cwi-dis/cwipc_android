from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.env import VirtualBuildEnv
from conan.tools.files import copy, get, replace_in_file, rm, rmdir
from conan.tools.microsoft import is_msvc, is_msvc_static_runtime
from conan.tools.scm import Git
import os

required_conan_version = ">=1.53.0"


class CWIPCConan(ConanFile):
    name = "cwipc"
    description = "CWI point cloud software suite"
    license = "MIT"
    url = "https://github.com/cwi-dis/cwipc"
    settings = "os", "arch", "compiler", "build_type"
    version = "7.4.3"

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        self.requires("libjpeg-turbo/2.1.5")
        self.requires("pcl/1.13.0")

    def source(self):
        git = Git(self)
        git.fetch_commit(
            "https://github.com/cwi-dis/cwipc",
            f"v{self.version}"
        )

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE.md", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        # remove unneeded directories
        rmdir(self, os.path.join(self.package_folder, "share"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "doc"))

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_module_file_name", "CWIPC")
        self.cpp_info.set_property("cmake_file_name", "cwipc")
