#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile
from conans.errors import ConanException


class TestPackageConan(ConanFile):

    def test(self):
        self.run("candle")
        self.run("heat")
        self.run("lit")
        wix_env = os.getenv("WIX")
        self.output.info("WIX environment variable: %s" % wix_env)
        if len(wix_env) <= 0:
            raise ConanException("WIX environment variable is not defined")
