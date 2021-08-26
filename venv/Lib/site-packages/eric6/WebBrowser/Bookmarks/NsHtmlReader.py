# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class to read Netscape HTML bookmark files.
"""

import re

from PyQt5.QtCore import QObject, QIODevice, QFile, QDateTime

from .BookmarkNode import BookmarkNode

import Utilities


class NsHtmlReader(QObject):
    """
    Class implementing a reader object for Netscape HTML bookmark files.
    """
    indentSize = 4
    
    def __init__(self):
        """
        Constructor
        """
        super(NsHtmlReader, self).__init__()
        
        self.__folderRx = re.compile("<DT><H3(.*?)>(.*?)</H3>", re.IGNORECASE)
        self.__endFolderRx = re.compile("</DL>", re.IGNORECASE)
        self.__bookmarkRx = re.compile("<DT><A(.*?)>(.*?)</A>", re.IGNORECASE)
        self.__descRx = re.compile("<DD>(.*)", re.IGNORECASE)
        self.__separatorRx = re.compile("<HR>", re.IGNORECASE)
        self.__urlRx = re.compile('HREF="(.*?)"', re.IGNORECASE)
        self.__addedRx = re.compile(r'ADD_DATE="(\d*?)"', re.IGNORECASE)
        self.__modifiedRx = re.compile(r'LAST_MODIFIED="(\d*?)"',
                                       re.IGNORECASE)
        self.__visitedRx = re.compile(r'LAST_VISIT="(\d*?)"', re.IGNORECASE)
        self.__foldedRx = re.compile("FOLDED", re.IGNORECASE)
    
    def read(self, fileNameOrDevice):
        """
        Public method to read a Netscape HTML bookmark file.
        
        @param fileNameOrDevice name of the file to read (string)
            or reference to the device to read (QIODevice)
        @return reference to the root node (BookmarkNode)
        """
        if isinstance(fileNameOrDevice, QIODevice):
            dev = fileNameOrDevice
        else:
            f = QFile(fileNameOrDevice)
            if not f.exists():
                return BookmarkNode(BookmarkNode.Root)
            f.open(QFile.ReadOnly)
            dev = f
        
        folders = []
        lastNode = None
        
        root = BookmarkNode(BookmarkNode.Root)
        folders.append(root)
        
        while not dev.atEnd():
            line = str(dev.readLine(), encoding="utf-8").rstrip()
            match = (
                self.__folderRx.search(line) or
                self.__endFolderRx.search(line) or
                self.__bookmarkRx.search(line) or
                self.__descRx.search(line) or
                self.__separatorRx.search(line)
            )
            if match is None:
                continue
            
            if match.re is self.__folderRx:
                # folder definition
                arguments = match.group(1)
                name = match.group(2)
                node = BookmarkNode(BookmarkNode.Folder, folders[-1])
                node.title = Utilities.html_udecode(name)
                node.expanded = self.__foldedRx.search(arguments) is None
                addedMatch = self.__addedRx.search(arguments)
                if addedMatch is not None:
                    node.added = QDateTime.fromTime_t(
                        int(addedMatch.group(1)))
                folders.append(node)
                lastNode = node
            
            elif match.re is self.__endFolderRx:
                # end of folder definition
                folders.pop()
            
            elif match.re is self.__bookmarkRx:
                # bookmark definition
                arguments = match.group(1)
                name = match.group(2)
                node = BookmarkNode(BookmarkNode.Bookmark, folders[-1])
                node.title = Utilities.html_udecode(name)
                match1 = self.__urlRx.search(arguments)
                if match1 is not None:
                    node.url = match1.group(1)
                match1 = self.__addedRx.search(arguments)
                if match1 is not None:
                    node.added = QDateTime.fromTime_t(
                        int(match1.group(1)))
                match1 = self.__modifiedRx.search(arguments)
                if match1 is not None:
                    node.modified = QDateTime.fromTime_t(
                        int(match1.group(1)))
                match1 = self.__visitedRx.search(arguments)
                if match1 is not None:
                    node.visited = QDateTime.fromTime_t(
                        int(match1.group(1)))
                lastNode = node
            
            elif match.re is self.__descRx:
                # description
                if lastNode:
                    lastNode.desc = Utilities.html_udecode(
                        match.group(1))
            
            elif match.re is self.__separatorRx:
                # separator definition
                BookmarkNode(BookmarkNode.Separator, folders[-1])
        
        return root
