#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil
from conans import ConanFile, CMake, tools


class WixtoolsetInstallerConan(ConanFile):
    name = "wixtoolset_installer"
    version = "3.11.1"
    description = "WIX installer binaries for use in recipes"
    topics = ("conan", "wix", "wixtoolset_installer")
    url = "https://github.com/bincrafters/conan-wixtoolset_installer"
    homepage = "https://github.com/wixtoolset/wix3"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MS-RL"
    exports = ["LICENSE.md"]
    settings = "os_build", "arch_build"

    def build(self):
        if not tools.os_info.is_windows:
            raise ConanException("WIX is only available on windows")

        short_version = "".join(self.version.split(".")[:2])
        source_url = "{}/releases/download/wix{}rtm/wix{}-binaries.zip".format(self.homepage, self.version.replace(".",""), short_version)
        self.output.info("Download {}".format(source_url))
        tools.get(source_url)

        # move files to create the structure from the offical setup
        bin_folder = os.path.join(self.build_folder, "bin")
        os.makedirs(bin_folder)
        for name in os.listdir(self.build_folder):
            afn = os.path.join(self.build_folder ,name)
            if os.path.isfile(afn) and name.lower() != "license.txt":
                shutil.move(afn, os.path.join(bin_folder , name))
        shutil.move(os.path.join(self.build_folder, "x86"), bin_folder)
        os.rename("sdk", "SDK")

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src="")
        self.copy(pattern="*", dst="", src="", keep_path=True)

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.env_info.WIX = self.package_folder
