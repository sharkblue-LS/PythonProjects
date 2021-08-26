# -*- coding: utf-8 -*-

# Copyright (c) 2009 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Class implementing a specialized application class.
"""

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication

QCoreApplication.setAttribute(
    Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
QCoreApplication.setAttribute(
    Qt.ApplicationAttribute.AA_ShareOpenGLContexts, True)


class E5Application(QApplication):
    """
    Eric application class with an object registry.
    """
    def __init__(self, argv):
        """
        Constructor
        
        @param argv command line arguments
        @type list
        """
        super(E5Application, self).__init__(argv)
        
        QCoreApplication.setAttribute(
            Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings, True)
        QCoreApplication.setAttribute(
            Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        self.__objectRegistry = {}
        self.__pluginObjectRegistry = {}
    
    def registerObject(self, name, objectRef):
        """
        Public method to register an object in the object registry.
        
        @param name name of the object
        @type str
        @param objectRef reference to the object
        @type any
        @exception KeyError raised when the given name is already in use
        """
        if name in self.__objectRegistry:
            raise KeyError('Object "{0}" already registered.'.format(name))
        else:
            self.__objectRegistry[name] = objectRef
    
    def getObject(self, name):
        """
        Public method to get a reference to a registered object.
        
        @param name name of the object
        @type str
        @return reference to the registered object
        @rtype any
        @exception KeyError raised when the given name is not known
        """
        if name in self.__objectRegistry:
            return self.__objectRegistry[name]
        else:
            raise KeyError('Object "{0}" is not registered.'.format(name))
    
    def registerPluginObject(self, name, objectRef, pluginType=None):
        """
        Public method to register a plugin object in the object registry.
        
        @param name name of the plugin object
        @type str
        @param objectRef reference to the plugin object
        @type any
        @param pluginType type of the plugin object
        @type str
        @exception KeyError raised when the given name is already in use
        """
        if name in self.__pluginObjectRegistry:
            raise KeyError(
                'Pluginobject "{0}" already registered.'.format(name))
        else:
            self.__pluginObjectRegistry[name] = (objectRef, pluginType)
    
    def unregisterPluginObject(self, name):
        """
        Public method to unregister a plugin object in the object registry.
        
        @param name name of the plugin object
        @type str
        """
        if name in self.__pluginObjectRegistry:
            del self.__pluginObjectRegistry[name]
    
    def getPluginObject(self, name):
        """
        Public method to get a reference to a registered plugin object.
        
        @param name name of the plugin object
        @type str
        @return reference to the registered plugin object
        @rtype any
        @exception KeyError raised when the given name is not known
        """
        if name in self.__pluginObjectRegistry:
            return self.__pluginObjectRegistry[name][0]
        else:
            raise KeyError(
                'Pluginobject "{0}" is not registered.'.format(name))
    
    def getPluginObjects(self):
        """
        Public method to get a list of (name, reference) pairs of all
        registered plugin objects.
        
        @return list of (name, reference) pairs
        @rtype list of (str, any)
        """
        objects = []
        for name in self.__pluginObjectRegistry:
            objects.append((name, self.__pluginObjectRegistry[name][0]))
        return objects
    
    def getPluginObjectType(self, name):
        """
        Public method to get the type of a registered plugin object.
        
        @param name name of the plugin object
        @type str
        @return type of the plugin object
        @rtype str
        @exception KeyError raised when the given name is not known
        """
        if name in self.__pluginObjectRegistry:
            return self.__pluginObjectRegistry[name][1]
        else:
            raise KeyError(
                'Pluginobject "{0}" is not registered.'.format(name))
    
    def usesDarkPalette(self):
        """
        Public method to check, if the application uses a palette with a dark
        background.
        
        @return flag indicating the use of a palette with a dark background
        @rtype bool
        """
        palette = self.palette()
        lightness = palette.color(QPalette.ColorRole.Window).lightness()
        return lightness <= 128

e5App = QCoreApplication.instance
