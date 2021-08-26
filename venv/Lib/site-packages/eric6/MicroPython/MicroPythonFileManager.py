# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing some file system commands for MicroPython.
"""

import os
import stat
import shutil

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject

from .MicroPythonFileSystemUtilities import (
    mtime2string, mode2string, decoratedName, listdirStat
)


class MicroPythonFileManager(QObject):
    """
    Class implementing an interface to the device file system commands with
    some additional sugar.
    
    @signal longListFiles(result) emitted with a tuple of tuples containing the
        name, mode, size and time for each directory entry
    @signal currentDir(dirname) emitted to report the current directory of the
        device
    @signal currentDirChanged(dirname) emitted to report back a change of the
        current directory
    @signal getFileDone(deviceFile, localFile) emitted after the file was
        fetched from the connected device and written to the local file system
    @signal putFileDone(localFile, deviceFile) emitted after the file was
        copied to the connected device
    @signal deleteFileDone(deviceFile) emitted after the file has been deleted
        on the connected device
    @signal rsyncDone(localName, deviceName) emitted after the rsync operation
        has been completed
    @signal rsyncProgressMessage(msg) emitted to send a message about what
        rsync is doing
    @signal removeDirectoryDone() emitted after a directory has been deleted
    @signal createDirectoryDone() emitted after a directory was created
    @signal fsinfoDone(fsinfo) emitted after the file system information was
        obtained
    
    @signal error(exc) emitted with a failure message to indicate a failure
        during the most recent operation
    """
    longListFiles = pyqtSignal(tuple)
    currentDir = pyqtSignal(str)
    currentDirChanged = pyqtSignal(str)
    getFileDone = pyqtSignal(str, str)
    putFileDone = pyqtSignal(str, str)
    deleteFileDone = pyqtSignal(str)
    rsyncDone = pyqtSignal(str, str)
    rsyncProgressMessage = pyqtSignal(str)
    removeDirectoryDone = pyqtSignal()
    createDirectoryDone = pyqtSignal()
    fsinfoDone = pyqtSignal(tuple)
    
    error = pyqtSignal(str, str)
    
    def __init__(self, commandsInterface, parent=None):
        """
        Constructor
        
        @param commandsInterface reference to the commands interface object
        @type MicroPythonCommandsInterface
        @param parent reference to the parent object
        @type QObject
        """
        super(MicroPythonFileManager, self).__init__(parent)
        
        self.__commandsInterface = commandsInterface
    
    @pyqtSlot(str)
    def lls(self, dirname, showHidden=False):
        """
        Public slot to get a long listing of the given directory.
        
        @param dirname name of the directory to list
        @type str
        @param showHidden flag indicating to show hidden files as well
        @type bool
        """
        try:
            filesList = self.__commandsInterface.lls(
                dirname, showHidden=showHidden)
            result = [(decoratedName(name, mode),
                       mode2string(mode),
                       str(size),
                       mtime2string(mtime)) for
                      name, (mode, size, mtime) in filesList]
            self.longListFiles.emit(tuple(result))
        except Exception as exc:
            self.error.emit("lls", str(exc))
    
    @pyqtSlot()
    def pwd(self):
        """
        Public slot to get the current directory of the device.
        """
        try:
            pwd = self.__commandsInterface.pwd()
            self.currentDir.emit(pwd)
        except Exception as exc:
            self.error.emit("pwd", str(exc))
    
    @pyqtSlot(str)
    def cd(self, dirname):
        """
        Public slot to change the current directory of the device.
        
        @param dirname name of the desired current directory
        @type str
        """
        try:
            self.__commandsInterface.cd(dirname)
            self.currentDirChanged.emit(dirname)
        except Exception as exc:
            self.error.emit("cd", str(exc))
    
    @pyqtSlot(str)
    @pyqtSlot(str, str)
    def get(self, deviceFileName, hostFileName=""):
        """
        Public slot to get a file from the connected device.
        
        @param deviceFileName name of the file on the device
        @type str
        @param hostFileName name of the local file
        @type str
        """
        if hostFileName and os.path.isdir(hostFileName):
            # only a local directory was given
            hostFileName = os.path.join(hostFileName,
                                        os.path.basename(deviceFileName))
        try:
            self.__commandsInterface.get(deviceFileName, hostFileName)
            self.getFileDone.emit(deviceFileName, hostFileName)
        except Exception as exc:
            self.error.emit("get", str(exc))
    
    @pyqtSlot(str)
    @pyqtSlot(str, str)
    def put(self, hostFileName, deviceFileName=""):
        """
        Public slot to put a file onto the device.
        
        @param hostFileName name of the local file
        @type str
        @param deviceFileName name of the file on the connected device
        @type str
        """
        try:
            self.__commandsInterface.put(hostFileName, deviceFileName)
            self.putFileDone.emit(hostFileName, deviceFileName)
        except Exception as exc:
            self.error.emit("put", str(exc))
    
    @pyqtSlot(str)
    def delete(self, deviceFileName):
        """
        Public slot to delete a file on the device.
        
        @param deviceFileName name of the file on the connected device
        @type str
        """
        try:
            self.__commandsInterface.rm(deviceFileName)
            self.deleteFileDone.emit(deviceFileName)
        except Exception as exc:
            self.error.emit("delete", str(exc))
    
    def __rsync(self, hostDirectory, deviceDirectory, mirror=True,
                localDevice=False, indentLevel=0):
        """
        Private method to synchronize a local directory to the device.
        
        @param hostDirectory name of the local directory
        @type str
        @param deviceDirectory name of the directory on the device
        @type str
        @param mirror flag indicating to mirror the local directory to
            the device directory
        @type bool
        @param localDevice flag indicating device access via local file system
        @type bool
        @param indentLevel indentation level for progress messages
        @type int
        @return list of errors
        @rtype list of str
        """
        indent = 4 * "&nbsp;"
        errors = []
        
        if not os.path.isdir(hostDirectory):
            return [self.tr(
                "The given name '{0}' is not a directory or does not exist.")
                .format(hostDirectory)
            ]
        
        indentStr = indentLevel * indent
        self.rsyncProgressMessage.emit(
            self.tr("{1}Synchronizing <b>{0}</b>.")
            .format(deviceDirectory, indentStr)
        )
        
        doneMessage = self.tr("{1}Done synchronizing <b>{0}</b>.").format(
            deviceDirectory, indentStr)
        
        sourceDict = {}
        sourceFiles = listdirStat(hostDirectory)
        for name, nstat in sourceFiles:
            sourceDict[name] = nstat
        
        destinationDict = {}
        if localDevice:
            if not os.path.isdir(deviceDirectory):
                # simply copy destination to source
                shutil.copytree(hostDirectory, deviceDirectory)
                self.rsyncProgressMessage.emit(doneMessage)
                return errors
            else:
                destinationFiles = listdirStat(deviceDirectory)
                for name, nstat in destinationFiles:
                    destinationDict[name] = nstat
        else:
            try:
                destinationFiles = self.__commandsInterface.lls(
                    deviceDirectory, fullstat=True)
            except Exception as exc:
                return [str(exc)]
            if destinationFiles is None:
                # the destination directory does not exist
                try:
                    self.__commandsInterface.mkdir(deviceDirectory)
                except Exception as exc:
                    return [str(exc)]
            else:
                for name, nstat in destinationFiles:
                    destinationDict[name] = nstat
        
        destinationSet = set(destinationDict.keys())
        sourceSet = set(sourceDict.keys())
        toAdd = sourceSet - destinationSet                  # add to dev
        toDelete = destinationSet - sourceSet               # delete from dev
        toUpdate = destinationSet.intersection(sourceSet)   # update files
        indentStr = (indentLevel + 1) * indent
        
        if localDevice:
            for sourceBasename in toAdd:
                # name exists in source but not in device
                sourceFilename = os.path.join(hostDirectory, sourceBasename)
                destFilename = os.path.join(deviceDirectory, sourceBasename)
                self.rsyncProgressMessage.emit(
                    self.tr("{1}Adding <b>{0}</b>...")
                    .format(destFilename, indentStr))
                if os.path.isfile(sourceFilename):
                    shutil.copy2(sourceFilename, destFilename)
                elif os.path.isdir(sourceFilename):
                    # recurse
                    errs = self.__rsync(sourceFilename, destFilename,
                                        mirror=mirror, localDevice=localDevice,
                                        indentLevel=indentLevel + 1)
                    # just note issues but ignore them otherwise
                    errors.extend(errs)
            
            if mirror:
                for destBasename in toDelete:
                    # name exists in device but not local, delete
                    destFilename = os.path.join(deviceDirectory, destBasename)
                    if os.path.isdir(destFilename):
                        shutil.rmtree(destFilename, ignore_errors=True)
                    elif os.path.isfile(destFilename):
                        os.remove(destFilename)
            
            for sourceBasename in toUpdate:
                # names exist in both; do an update
                sourceStat = sourceDict[sourceBasename]
                destStat = destinationDict[sourceBasename]
                sourceFilename = os.path.join(hostDirectory, sourceBasename)
                destFilename = os.path.join(deviceDirectory, sourceBasename)
                destMode = destStat[0]
                if os.path.isdir(sourceFilename):
                    if os.path.isdir(destFilename):
                        # both are directories => recurs
                        errs = self.__rsync(sourceFilename, destFilename,
                                            mirror=mirror,
                                            localDevice=localDevice,
                                            indentLevel=indentLevel + 1)
                        # just note issues but ignore them otherwise
                        errors.extend(errs)
                    else:
                        self.rsyncProgressMessage.emit(
                            self.tr("Source <b>{0}</b> is a directory and"
                                    " destination <b>{1}</b> is a file."
                                    " Ignoring it.")
                            .format(sourceFilename, destFilename)
                        )
                else:
                    if os.path.isdir(destFilename):
                        self.rsyncProgressMessage.emit(
                            self.tr("Source <b>{0}</b> is a file and"
                                    " destination <b>{1}</b> is a directory."
                                    " Ignoring it.")
                            .format(sourceFilename, destFilename)
                        )
                    else:
                        if sourceStat[8] > destStat[8]:     # mtime
                            self.rsyncProgressMessage.emit(
                                self.tr("Updating <b>{0}</b>...")
                                .format(destFilename)
                            )
                        shutil.copy2(sourceFilename, destFilename)
        else:
            for sourceBasename in toAdd:
                # name exists in source but not in device
                sourceFilename = os.path.join(hostDirectory, sourceBasename)
                if deviceDirectory == "/":
                    destFilename = "/" + sourceBasename
                else:
                    destFilename = deviceDirectory + "/" + sourceBasename
                self.rsyncProgressMessage.emit(
                    self.tr("{1}Adding <b>{0}</b>...")
                    .format(destFilename, indentStr))
                if os.path.isfile(sourceFilename):
                    try:
                        self.__commandsInterface.put(sourceFilename,
                                                     destFilename)
                    except Exception as exc:
                        # just note issues but ignore them otherwise
                        errors.append(str(exc))
                elif os.path.isdir(sourceFilename):
                    # recurse
                    errs = self.__rsync(sourceFilename, destFilename,
                                        mirror=mirror,
                                        indentLevel=indentLevel + 1)
                    # just note issues but ignore them otherwise
                    errors.extend(errs)
        
            if mirror:
                for destBasename in toDelete:
                    # name exists in device but not local, delete
                    if deviceDirectory == "/":
                        destFilename = "/" + sourceBasename
                    else:
                        destFilename = deviceDirectory + "/" + destBasename
                    self.rsyncProgressMessage.emit(
                        self.tr("{1}Removing <b>{0}</b>...")
                        .format(destFilename, indentStr))
                    try:
                        self.__commandsInterface.rmrf(destFilename,
                                                      recursive=True,
                                                      force=True)
                    except Exception as exc:
                        # just note issues but ignore them otherwise
                        errors.append(str(exc))
            
            for sourceBasename in toUpdate:
                # names exist in both; do an update
                sourceStat = sourceDict[sourceBasename]
                destStat = destinationDict[sourceBasename]
                sourceFilename = os.path.join(hostDirectory, sourceBasename)
                if deviceDirectory == "/":
                    destFilename = "/" + sourceBasename
                else:
                    destFilename = deviceDirectory + "/" + sourceBasename
                destMode = destStat[0]
                if os.path.isdir(sourceFilename):
                    if stat.S_ISDIR(destMode):
                        # both are directories => recurs
                        errs = self.__rsync(sourceFilename, destFilename,
                                            mirror=mirror,
                                            indentLevel=indentLevel + 1)
                        # just note issues but ignore them otherwise
                        errors.extend(errs)
                    else:
                        self.rsyncProgressMessage.emit(
                            self.tr("Source <b>{0}</b> is a directory and"
                                    " destination <b>{1}</b> is a file."
                                    " Ignoring it.")
                            .format(sourceFilename, destFilename)
                        )
                else:
                    if stat.S_ISDIR(destMode):
                        self.rsyncProgressMessage.emit(
                            self.tr("Source <b>{0}</b> is a file and"
                                    " destination <b>{1}</b> is a directory."
                                    " Ignoring it.")
                            .format(sourceFilename, destFilename)
                        )
                    else:
                        if sourceStat[8] > destStat[8]:     # mtime
                            self.rsyncProgressMessage.emit(
                                self.tr("{1}Updating <b>{0}</b>...")
                                .format(destFilename, indentStr)
                            )
                            try:
                                self.__commandsInterface.put(sourceFilename,
                                                             destFilename)
                            except Exception as exc:
                                errors.append(str(exc))
        
        self.rsyncProgressMessage.emit(doneMessage)
        
        return errors
    
    @pyqtSlot(str, str)
    @pyqtSlot(str, str, bool)
    @pyqtSlot(str, str, bool, bool)
    def rsync(self, hostDirectory, deviceDirectory, mirror=True,
              localDevice=False):
        """
        Public slot to synchronize a local directory to the device.
        
        @param hostDirectory name of the local directory
        @type str
        @param deviceDirectory name of the directory on the device
        @type str
        @param mirror flag indicating to mirror the local directory to
            the device directory
        @type bool
        @param localDevice flag indicating device access via local file system
        @type bool
        """
        errors = self.__rsync(hostDirectory, deviceDirectory, mirror=mirror,
                              localDevice=localDevice)
        if errors:
            self.error.emit("rsync", "\n".join(errors))
        
        self.rsyncDone.emit(hostDirectory, deviceDirectory)
    
    @pyqtSlot(str)
    def mkdir(self, dirname):
        """
        Public slot to create a new directory.
        
        @param dirname name of the directory to create
        @type str
        """
        try:
            self.__commandsInterface.mkdir(dirname)
            self.createDirectoryDone.emit()
        except Exception as exc:
            self.error.emit("mkdir", str(exc))
    
    @pyqtSlot(str)
    @pyqtSlot(str, bool)
    def rmdir(self, dirname, recursive=False):
        """
        Public slot to (recursively) remove a directory.
        
        @param dirname name of the directory to be removed
        @type str
        @param recursive flag indicating a recursive removal
        @type bool
        """
        try:
            if recursive:
                self.__commandsInterface.rmrf(dirname, recursive=True,
                                              force=True)
            else:
                self.__commandsInterface.rmdir(dirname)
            self.removeDirectoryDone.emit()
        except Exception as exc:
            self.error.emit("rmdir", str(exc))
    
    def fileSystemInfo(self):
        """
        Public method to obtain information about the currently mounted file
        systems.
        """
        try:
            fsinfo = self.__commandsInterface.fileSystemInfo()
            self.fsinfoDone.emit(fsinfo)
        except Exception as exc:
            self.error.emit("fileSystemInfo", str(exc))
