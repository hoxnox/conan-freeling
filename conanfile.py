import os
from conans import CMake, tools
from nxtools import NxConanFile
from glob import glob

class FreelingConan(NxConanFile):
    name = "FreeLing"
    version = "4.1"
    fullname = "%s-%s" % (name, version)
    license = "http://www.gnu.org/licenses/agpl-3.0.html"
    author = "Lluis Padro"
    url = "https://github.com/hoxnox/conan-freeling"
    description = "FreeLing is a C++ library providing language analysis functionalities (morphological analysis, named entity detection, PoS-tagging, parsing, Word Sense Disambiguation, Semantic Role Labelling, etc.) for a variety of languages (English, Spanish, Portuguese, Italian, French, German, Russian, Catalan, Galician, Croatian, Slovene, among others)."
    topics = ("nlp", "language", "text processing")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    build_policy = "missing"
    requires = ("boost/1.66.0@hoxnox/stable",
                "icu/64.2@hoxnox/stable",
                "zlib/1.2.11@hoxnox/stable")

    def config(self):
        self.options["boost"].icu = True

    def do_source(self):
        tarball_name = "%s.tar.gz" % self.fullname
        self.retrieve("ccb3322db6851075c9419bb5e472aa6b2e32cc7e9fa01981cff49ea3b212247e",
                [
                    "vendor://TALP-UPC/FreeLing/%s.tar.gz" % self.fullname,
                    "https://github.com/TALP-UPC/FreeLing/releases/download/%s/%s"
                        % (self.version, tarball_name)
                ], tarball_name)
        tools.untargz(tarball_name)
        os.unlink(tarball_name)

    def do_build(self):
        cmake = CMake(self)
        for file in sorted(glob("patch/[0-9]*.patch")):
            self.output.info("Applying patch '{file}'".format(file=file))
            tools.patch(base_path=self.fullname, patch_file=file, strip=0)
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = self.staging_dir
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["BOOST_ROOT"] = self.deps_cpp_info["boost"].rootpath
        cmake.definitions["ZLIB_ROOT"] = self.deps_cpp_info["zlib"].rootpath
        cmake.definitions["ICU_ROOT"] = self.deps_cpp_info["icu"].rootpath
        cmake.verbose = True
        self.output.info("cmake  cmd: %s" % cmake.command_line)
        cmake.configure(source_folder=self.fullname)
        cmake.build(target="install")
        self.copy(dst="lib", src=staging_lib)

    def do_package_info(self):
        self.cpp_info.libs = ["freeling", "foma", "treeler"]
        # TODO: other data stuff here
