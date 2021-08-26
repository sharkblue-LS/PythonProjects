# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing some common utility functions for the Git package.
"""

import os

from PyQt5.QtCore import QProcessEnvironment

import Utilities


def getConfigPath():
    """
    Public function to get the filename of the config file.
    
    @return filename of the config file (string)
    """
    if Utilities.isWindowsPlatform():
        userprofile = os.environ["USERPROFILE"]
        return os.path.join(userprofile, ".gitconfig")
    else:
        homedir = Utilities.getHomeDir()
        return os.path.join(homedir, ".gitconfig")


def prepareProcess(proc, language=""):
    """
    Public function to prepare the given process.
    
    @param proc reference to the process to be prepared (QProcess)
    @param language language to be set (string)
    """
    env = QProcessEnvironment.systemEnvironment()
    
    # set the language for the process
    if language:
        env.insert("LANGUAGE", language)
    
    proc.setProcessEnvironment(env)
