# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the editor outline model.
"""

import os

from PyQt5.QtCore import QCoreApplication, QModelIndex

from UI.BrowserModel import (
    BrowserModel, BrowserItem, BrowserClassItem, BrowserCodingItem,
    BrowserGlobalsItem, BrowserImportsItem, BrowserImportItem,
    BrowserClassAttributesItem, BrowserMethodItem
)

import Preferences


class EditorOutlineModel(BrowserModel):
    """
    Class implementing the editor outline model.
    """
    SupportedLanguages = (
        "IDL", "JavaScript", "Protocol", "Python3", "MicroPython", "Cython",
        "Ruby",
    )
    
    def __init__(self, editor, populate=True):
        """
        Constructor
        
        @param editor reference to the editor containing the source text
        @type Editor
        @param populate flag indicating to populate the outline
        @type bool
        """
        super(EditorOutlineModel, self).__init__(nopopulate=True)
        
        self.__editor = editor
        
        self.__populated = False
        
        rootData = QCoreApplication.translate("EditorOutlineModel", "Name")
        self.rootItem = BrowserItem(None, rootData)
        
        if populate:
            self.__populateModel()
    
    def __populateModel(self, repopulate=False):
        """
        Private slot to populate the model.
        
        @param repopulate flag indicating a repopulation
        @type bool
        """
        self.__filename = self.__editor.getFileName()
        self.__module = os.path.basename(self.__filename)
        
        language = self.__editor.getLanguage()
        if language in EditorOutlineModel.SupportedLanguages:
            if language == "IDL":
                from Utilities.ClassBrowsers import idlclbr
                dictionary = idlclbr.scan(
                    self.__editor.text(), self.__filename, self.__module)
                idlclbr._modules.clear()
            elif language == "Protocol":
                from Utilities.ClassBrowsers import protoclbr
                dictionary = protoclbr.scan(
                    self.__editor.text(), self.__filename, self.__module)
                protoclbr._modules.clear()
            elif language == "Ruby":
                from Utilities.ClassBrowsers import rbclbr
                dictionary = rbclbr.scan(
                    self.__editor.text(), self.__filename, self.__module)
                rbclbr._modules.clear()
            elif language == "JavaScript":
                from Utilities.ClassBrowsers import jsclbr
                dictionary = jsclbr.scan(
                    self.__editor.text(), self.__filename, self.__module)
                jsclbr._modules.clear()
            elif language in ("Python3", "MicroPython", "Cython"):
                from Utilities.ClassBrowsers import pyclbr
                dictionary = pyclbr.scan(
                    self.__editor.text(), self.__filename, self.__module)
                pyclbr._modules.clear()
            
            keys = list(dictionary.keys())
            if len(keys) > 0:
                parentItem = self.rootItem
                
                if repopulate:
                    last = len(keys) - 1
                    if (
                        "@@Coding@@" in keys and
                        not Preferences.getEditor("SourceOutlineShowCoding")
                    ):
                        last -= 1
                    self.beginInsertRows(QModelIndex(), 0, last)
                
                for key in keys:
                    if key.startswith("@@"):
                        # special treatment done later
                        continue
                    cl = dictionary[key]
                    try:
                        if cl.module == self.__module:
                            node = BrowserClassItem(
                                parentItem, cl, self.__filename)
                            self._addItem(node, parentItem)
                    except AttributeError:
                        pass
                if (
                    "@@Coding@@" in keys and
                    Preferences.getEditor("SourceOutlineShowCoding")
                ):
                    node = BrowserCodingItem(
                        parentItem,
                        QCoreApplication.translate(
                            "EditorOutlineModel", "Coding: {0}")
                        .format(dictionary["@@Coding@@"].coding),
                        dictionary["@@Coding@@"].linenumber)
                    self._addItem(node, parentItem)
                if "@@Globals@@" in keys:
                    node = BrowserGlobalsItem(
                        parentItem,
                        dictionary["@@Globals@@"].globals,
                        QCoreApplication.translate(
                            "EditorOutlineModel", "Globals"))
                    self._addItem(node, parentItem)
                if "@@Import@@" in keys or "@@ImportFrom@@" in keys:
                    node = BrowserImportsItem(
                        parentItem,
                        QCoreApplication.translate(
                            "EditorOutlineModel", "Imports"))
                    self._addItem(node, parentItem)
                    if "@@Import@@" in keys:
                        for importedModule in (
                            dictionary["@@Import@@"].getImports().values()
                        ):
                            m_node = BrowserImportItem(
                                node,
                                importedModule.importedModuleName,
                                importedModule.file,
                                importedModule.linenos)
                            self._addItem(m_node, node)
                            for importedName, linenos in (
                                importedModule.importedNames.items()
                            ):
                                mn_node = BrowserImportItem(
                                    m_node,
                                    importedName,
                                    importedModule.file,
                                    linenos,
                                    isModule=False)
                                self._addItem(mn_node, m_node)
                if repopulate:
                    self.endInsertRows()
            
            self.__populated = True
        else:
            self.clear()
            self.__populated = False
    
    def isPopulated(self):
        """
        Public method to check, if the model is populated.
        
        @return flag indicating a populated model
        @rtype bool
        """
        return self.__populated
    
    def repopulate(self):
        """
        Public slot to repopulate the model.
        """
        self.clear()
        self.__populateModel(repopulate=True)
    
    def editor(self):
        """
        Public method to retrieve a reference to the editor.
        
        @return reference to the editor
        @rtype Editor
        """
        return self.__editor
    
    def fileName(self):
        """
        Public method to retrieve the file name of the editor.
        
        @return file name of the editor
        @rtype str
        """
        return self.__filename
    
    def itemIndexByLine(self, lineno):
        """
        Public method to find an item's index given a line number.
        
        @param lineno one based line number of the item
        @type int
        @return index of the item found
        @rtype QModelIndex
        """
        def findItem(lineno, parent):
            """
            Function to iteratively search for an item containing the given
            line.
            
            @param lineno one based line number of the item
            @type int
            @param parent reference to the parent item
            @type BrowserItem
            @return found item or None
            @rtype BrowserItem
            """
            if not parent.isPopulated():
                if parent.isLazyPopulated():
                    self.populateItem(parent)
                else:
                    return None
            for child in parent.children():
                if isinstance(child, BrowserClassAttributesItem):
                    itm = findItem(lineno, child)
                    if itm is not None:
                        return itm
                elif isinstance(child, (BrowserClassItem, BrowserMethodItem)):
                    start, end = child.boundaries()
                    if end == -1:
                        end = 1000000   # assume end of file
                    if start <= lineno <= end:
                        itm = findItem(lineno, child)
                        if itm is not None:
                            return itm
                        else:
                            return child
                elif hasattr(child, "linenos"):
                    if lineno in child.linenos():
                        return child
                elif hasattr(child, "lineno"):
                    if lineno == child.lineno():
                        return child
            else:
                return None
        
        if self.__populated:
            for rootChild in self.rootItem.children():
                itm = None
                if isinstance(rootChild, BrowserClassItem):
                    start, end = rootChild.boundaries()
                    if end == -1:
                        end = 1000000   # assume end of file
                    if start <= lineno <= end:
                        itm = findItem(lineno, rootChild)
                        if itm is None:
                            itm = rootChild
                elif isinstance(rootChild,
                                (BrowserImportsItem, BrowserGlobalsItem)):
                    itm = findItem(lineno, rootChild)
                elif (
                    isinstance(rootChild, BrowserCodingItem) and
                    lineno == rootChild.lineno()
                ):
                    itm = rootChild
                if itm is not None:
                    return self.createIndex(itm.row(), 0, itm)
            else:
                return QModelIndex()
        
        return QModelIndex()
