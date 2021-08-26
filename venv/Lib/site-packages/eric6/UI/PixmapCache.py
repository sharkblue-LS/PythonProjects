# -*- coding: utf-8 -*-

# Copyright (c) 2004 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a pixmap cache for icons.
"""

import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon, QPainter


class PixmapCache(object):
    """
    Class implementing a pixmap cache for icons.
    """
    SupportedExtensions = [".svgz", ".svg", ".png"]
    
    def __init__(self):
        """
        Constructor
        """
        self.pixmapCache = {}
        self.searchPath = []

    def getPixmap(self, key, size=None):
        """
        Public method to retrieve a pixmap.

        @param key name of the wanted pixmap
        @type str
        @param size requested size
        @type QSize
        @return the requested pixmap
        @rtype QPixmap
        """
        if key:
            basename, ext = os.path.splitext(key)
            if size and not size.isEmpty():
                key = "{0}_{1}_{2}".format(
                    basename, size.width(), size.height())
            else:
                key = basename
            
            try:
                return self.pixmapCache[key]
            except KeyError:
                pm = QPixmap()
                for extension in self.SupportedExtensions:
                    filename = basename + extension
                    if not os.path.isabs(filename):
                        for path in self.searchPath:
                            pm = QPixmap(path + "/" + filename)
                            if not pm.isNull():
                                break
                    else:
                        pm = QPixmap(filename)
                    if not pm.isNull():
                        if size and not size.isEmpty():
                            pm = pm.scaled(size)
                        break
                else:
                    pm = QPixmap()
                
                self.pixmapCache[key] = pm
                return self.pixmapCache[key]
        
        return QPixmap()

    def addSearchPath(self, path):
        """
        Public method to add a path to the search path.
        
        @param path path to add
        @type str
        """
        if path not in self.searchPath:
            self.searchPath.append(path)
    
    def removeSearchPath(self, path):
        """
        Public method to remove a path from the search path.
        
        @param path path to remove
        @type str
        """
        if path in self.searchPath:
            self.searchPath.remove(path)

pixCache = PixmapCache()


def getPixmap(key, size=None, cache=pixCache):
    """
    Module function to retrieve a pixmap.

    @param key name of the wanted pixmap
    @type str
    @param size requested size
    @type QSize
    @param cache reference to the pixmap cache object
    @type PixmapCache
    @return the requested pixmap
    @rtype QPixmap
    """
    return cache.getPixmap(key, size=size)


def getIcon(key, size=None, cache=pixCache):
    """
    Module function to retrieve an icon.

    @param key name of the wanted pixmap
    @type str
    @param size requested size
    @type QSize
    @param cache reference to the pixmap cache object
    @type PixmapCache
    @return the requested icon
    @rtype QIcon
    """
    return QIcon(cache.getPixmap(key, size=size))


def getSymlinkIcon(key, size=None, cache=pixCache):
    """
    Module function to retrieve a symbolic link icon.

    @param key name of the wanted pixmap
    @type str
    @param size requested size
    @type QSize
    @param cache reference to the pixmap cache object
    @type PixmapCache
    @return the requested icon
    @rtype QIcon
    """
    pix1 = QPixmap(cache.getPixmap(key, size=size))
    pix2 = cache.getPixmap("symlink")
    painter = QPainter(pix1)
    painter.drawPixmap(0, 10, pix2)
    painter.end()
    return QIcon(pix1)


def getCombinedIcon(keys, size=None, cache=pixCache):
    """
    Module function to retrieve a symbolic link icon.

    @param keys list of names of icons
    @type list of str
    @param size requested size of individual icons
    @type QSize
    @param cache reference to the pixmap cache object
    @type PixmapCache
    @return the requested icon
    @rtype QIcon
    """
    height = width = 0
    pixmaps = []
    for key in keys:
        pix = cache.getPixmap(key, size=size)
        if not pix.isNull():
            height = max(height, pix.height())
            width = max(width, pix.width())
            pixmaps.append(pix)
    if pixmaps:
        pix = QPixmap(len(pixmaps) * width, height)
        pix.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pix)
        x = 0
        for pixmap in pixmaps:
            painter.drawPixmap(x, 0, pixmap.scaled(QSize(width, height)))
            x += width
        painter.end()
        icon = QIcon(pix)
    else:
        icon = QIcon()
    return icon


def addSearchPath(path, cache=pixCache):
    """
    Module function to add a path to the search path.

    @param path path to add
    @type str
    @param cache reference to the pixmap cache object
    @type PixmapCache
    """
    cache.addSearchPath(path)


def removeSearchPath(path, cache=pixCache):
    """
    Public method to remove a path from the search path.
    
    @param path path to remove
    @type str
    @param cache reference to the pixmap cache object
    @type PixmapCache
    """
    cache.removeSearchPath(path)
