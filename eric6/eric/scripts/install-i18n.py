#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2004 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#
# This is the install script for eric's translation files.

"""
Installation script for the eric IDE translation files.
"""

import sys
import os
import shutil
import glob

try:
    from eric6config import getConfig
except ImportError:
    print("The eric IDE doesn't seem to be installed. Aborting.")
    sys.exit(1)
except SyntaxError:
    # an incomplete or old config file was found
    print("The eric IDE seems to be installed incompletely. Aborting.")
    sys.exit(1)
    

def getConfigDir():
    """
    Global function to get the name of the directory storing the config data.
    
    @return directory name of the config dir (string)
    """
    cdn = ".eric6"
    
    hp = os.path.join(os.path.expanduser("~"), cdn)
    if not os.path.exists(hp):
        os.mkdir(hp)
    return hp
    
# Define the globals.
progName = None
configDir = getConfigDir()
privateInstall = False


def usage(rcode=2):
    """
    Display a usage message and exit.

    @param rcode return code passed back to the calling process (integer)
    """
    global progName, configDir

    print()
    print("Usage:")
    print("    {0} [-hp]".format(progName))
    print("where:")
    print("    -h        display this help message")
    print("    -p        install into the private area ({0})".format(
        configDir))

    sys.exit(rcode)


def installTranslations():
    """
    Install the translation files into the right place.
    """
    global privateInstall, configDir
    
    if privateInstall:
        targetDir = configDir
    else:
        targetDir = getConfig('ericTranslationsDir')
    
    try:
        for fn in glob.glob(os.path.join('eric', 'eric6', 'i18n', '*.qm')):
            shutil.copy2(fn, targetDir)
            os.chmod(os.path.join(targetDir, os.path.basename(fn)), 0o644)
    except OSError as msg:
        sys.stderr.write(
            'OSError: {0}\nTry install-i18n as root.\n'.format(msg))
    except OSError as msg:
        sys.stderr.write(
            'OSError: {0}\nTry install-i18n with admin rights.\n'.format(msg))
    

def main(argv):
    """
    The main function of the script.

    @param argv list of command line arguments (list of strings)
    """
    import getopt

    # Parse the command line.
    global progName, privateInstall
    progName = os.path.basename(argv[0])

    try:
        optlist, args = getopt.getopt(argv[1:], "hp")
    except getopt.GetoptError:
        usage()

    global platBinDir
    
    for opt, _arg in optlist:
        if opt == "-h":
            usage(0)
        elif opt == "-p":
            privateInstall = 1
        
    installTranslations()

if __name__ == "__main__":
    try:
        main(sys.argv)
    except SystemExit:
        raise
    except Exception:
        print("""An internal error occured.  Please report all the output of"""
              """ the program,\nincluding the following traceback, to"""
              """ eric-bugs@eric-ide.python-projects.org.\n""")
        raise

#
# eflag: noqa = M801
