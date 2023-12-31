from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
from conan.tools.files import copy, rmdir, apply_conandata_patches, export_conandata_patches
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
        cmake_layout(self)

    def requirements(self):
        self.requires("libjpeg-turbo/2.1.5")
        self.requires("eigen/3.3.7")
        self.requires("flann/1.9.2@pcl-android/stable")
        self.requires("boost/1.82.0@pcl-android/stable")
        self.requires("pcl/1.13.0@pcl-android/stable")

    def source(self):
        git = Git(self)
        git.fetch_commit(
            "https://github.com/cwi-dis/cwipc",
            f"v{self.version}"
        )

        git.run("submodule update --init cwipc_codec")
        git.run("submodule update --init cwipc_util")

        apply_conandata_patches(self)

    def export_sources(self):
        export_conandata_patches(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        boost_libdir = self.dependencies["boost"].cpp_info.libdirs[0]
        boost_libraries = list([f.path for f in os.scandir(boost_libdir)])

        jpeg_libdir = self.dependencies["libjpeg-turbo"].cpp_info.libdirs[0]
        jpeg_libraries = list([f.path for f in os.scandir(jpeg_libdir)])

        cmake = CMake(self)
        cmake.configure({
            "CWIPC_VERSION": self.version,
            "ANDROID": "1",
            "BOOST_LIBRARIES": ";".join(boost_libraries),
            "JPEG_LIBRARIES": ";".join(jpeg_libraries)
        })

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
