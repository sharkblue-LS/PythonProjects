#
# Jasy - Web Tooling Framework
# Copyright 2010-2012 Zynga Inc.
# Copyright 2013-2014 Sebastian Werner
#

"""
**Jasy - Web Tooling Framework**

Jasy is a powerful Python3-based tooling framework.
It makes it easy to manage heavy web projects.
Its main goal is to offer an API which could be used by developers to write their custom build/deployment scripts.
"""

from __future__ import unicode_literals

__version__ = "1.5-beta6"
__author__ = "Sebastian Werner <info@sebastian-werner.net>"

import os.path
datadir = os.path.join(os.path.dirname(__file__), "data")

def info():
    """
    Prints information about Jasy to the console.
    """

    import jasy.core.Console as Console

    print("Jasy %s is a powerful web tooling framework" % __version__)
    print("Visit %s for details." % Console.colorize("https://github.com/sebastian-software/jasy", "underline"))
    print()


class UserError(Exception):
    """
    Standard Jasy error class raised whenever something happens which the system understands (somehow excepected)
    """
    pass
