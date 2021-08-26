# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class to generate the output of the hg diff command.
"""

import os

from PyQt5.QtCore import pyqtSignal, QObject

from E5Gui.E5OverrideCursor import E5OverrideCursor


class HgDiffGenerator(QObject):
    """
    Class implementing the generation of output of the hg diff command.
    
    @signal finished() emitted when all processes have finished
    """
    finished = pyqtSignal()
    
    def __init__(self, vcs, parent=None):
        """
        Constructor
        
        @param vcs reference to the vcs object
        @param parent parent widget (QWidget)
        """
        super(HgDiffGenerator, self).__init__(parent)
        
        self.vcs = vcs
        
        self.__hgClient = self.vcs.getClient()
    
    def stopProcess(self):
        """
        Public slot to stop the diff process.
        """
        if self.__hgClient.isExecuting():
            self.__hgClient.cancel()
    
    def __getVersionArg(self, version):
        """
        Private method to get a hg revision argument for the given revision.
        
        @param version revision (integer or string)
        @return version argument (string)
        """
        if version == "WORKING":
            return None
        else:
            return str(version).strip()
    
    def start(self, fn, versions=None, bundle=None, qdiff=False):
        """
        Public slot to start the hg diff command.
        
        @param fn filename to be diffed (string)
        @param versions list of versions to be diffed (list of up to
            2 strings or None)
        @param bundle name of a bundle file (string)
        @param qdiff flag indicating qdiff command shall be used (boolean)
        @return flag indicating a successful start of the diff command
            (boolean)
        """
        if qdiff:
            args = self.vcs.initCommand("qdiff")
        else:
            args = self.vcs.initCommand("diff")
            
            if self.vcs.hasSubrepositories():
                args.append("--subrepos")
            
            if bundle:
                args.append('--repository')
                args.append(bundle)
            elif (
                self.vcs.bundleFile and
                os.path.exists(self.vcs.bundleFile)
            ):
                args.append('--repository')
                args.append(self.vcs.bundleFile)
            
            if versions is not None:
                rev1 = self.__getVersionArg(versions[0])
                rev2 = None
                if len(versions) == 2:
                    rev2 = self.__getVersionArg(versions[1])
                
                if rev1 is not None or rev2 is not None:
                    if self.vcs.version >= (5, 7, 0):
                        if rev1 is not None:
                            args += ["--from", rev1]
                        if rev2 is not None:
                            args += ["--to", rev2]
                    else:
                        args.append('-r')
                        if rev1 is not None and rev2 is not None:
                            args.append('{0}:{1}'.format(rev1, rev2))
                        elif rev2 is None:
                            args.append(rev1)
                        elif rev1 is None:
                            args.append(':{0}'.format(rev2))
        
        if fn:
            if isinstance(fn, list):
                self.vcs.addArguments(args, fn)
            else:
                args.append(fn)
        
        self.__oldFile = ""
        self.__oldFileLine = -1
        self.__fileSeparators = []
        self.__output = []
        self.__errors = []
        
        with E5OverrideCursor():
            out, err = self.__hgClient.runcommand(args)
            
            if err:
                self.__errors = err.splitlines(True)
            
            if out:
                self.__output = out.splitlines(True)
                for lineno, line in enumerate(self.__output):
                    if line.startswith(("--- ", "+++ ")):
                        self.__processFileLine(lineno, line)
                    if self.__hgClient.wasCanceled():
                        break
        
        self.__finish()
        
        return True
    
    def __finish(self):
        """
        Private slot called when the process finished or the user pressed
        the button.
        """
        self.finished.emit()
    
    def getResult(self):
        """
        Public method to return the result data.
        
        @return tuple of lists of string containing lines of the diff, the
            list of errors and a list of tuples of filenames and the line
            into the diff output.
        """
        return (self.__output, self.__errors, self.__fileSeparators)
    
    def __extractFileName(self, line):
        """
        Private method to extract the file name out of a file separator line.
        
        @param line line to be processed (string)
        @return extracted file name (string)
        """
        f = line.split(None, 1)[1]
        f = f.rsplit(None, 6)[0]
        if f == "/dev/null":
            f = "__NULL__"
        else:
            f = f.split("/", 1)[1]
        return f
    
    def __processFileLine(self, lineno, line):
        """
        Private slot to process a line giving the old/new file.
        
        @param lineno line number of line to be processed
        @type int
        @param line line to be processed
        @type str
        """
        if line.startswith('---'):
            self.__oldFileLine = lineno
            self.__oldFile = self.__extractFileName(line)
        else:
            newFile = self.__extractFileName(line)
            if self.__oldFile == "__NULL__":
                self.__fileSeparators.append(
                    (newFile, newFile, self.__oldFileLine))
            else:
                self.__fileSeparators.append(
                    (self.__oldFile, newFile, self.__oldFileLine))
