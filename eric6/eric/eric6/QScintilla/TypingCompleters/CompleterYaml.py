# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a typing completer for Python.
"""

import re

from PyQt5.Qsci import QsciScintilla

from .CompleterBase import CompleterBase

import Preferences


class CompleterYaml(CompleterBase):
    """
    Class implementing typing completer for Python.
    """
    def __init__(self, editor, parent=None):
        """
        Constructor
        
        @param editor reference to the editor object
        @type QScintilla.Editor
        @param parent reference to the parent object
        @type QObject
        """
        super(CompleterYaml, self).__init__(editor, parent)
        
        self.readSettings()
    
    def readSettings(self):
        """
        Public slot called to reread the configuration parameters.
        """
        self.setEnabled(
            Preferences.getEditorTyping("Yaml/EnabledTypingAids"))
        self.__insertClosingBrace = Preferences.getEditorTyping(
            "Yaml/InsertClosingBrace")
        self.__skipBrace = Preferences.getEditorTyping(
            "Yaml/SkipBrace")
        self.__insertQuote = Preferences.getEditorTyping(
            "Yaml/InsertQuote")
        self.__autoIndentation = Preferences.getEditorTyping(
            "Yaml/AutoIndentation")
        self.__colonDetection = Preferences.getEditorTyping(
            "Yaml/ColonDetection")
        self.__insertBlankDash = Preferences.getEditorTyping(
            "Yaml/InsertBlankDash")
        self.__insertBlankColon = Preferences.getEditorTyping(
            "Yaml/InsertBlankColon")
        self.__insertBlankQuestion = Preferences.getEditorTyping(
            "Yaml/InsertBlankQuestion")
        self.__insertBlankComma = Preferences.getEditorTyping(
            "Yaml/InsertBlankComma")
    
    def charAdded(self, charNumber):
        """
        Public slot called to handle the user entering a character.
        
        @param charNumber value of the character entered
        @type int
        """
        char = chr(charNumber)
        if char not in ['{', '}', '[', ']', "'", '"', '-', ':', '?', ',',
                        '\n']:
            return  # take the short route
        
        line, col = self.editor.getCursorPosition()
        
        if self.__inComment(line, col):
            return
        
        # open curly brace
        # insert closing brace
        if char == '{':
            if self.__insertClosingBrace:
                self.editor.insert('}')
        
        # open bracket
        # insert closing bracket
        elif char == '[':
            if self.__insertClosingBrace:
                self.editor.insert(']')
        
        # closing parenthesis
        # skip matching closing parenthesis
        elif char in ['}', ']']:
            txt = self.editor.text(line)
            if col < len(txt) and char == txt[col]:
                if self.__skipBrace:
                    self.editor.setSelection(line, col, line, col + 1)
                    self.editor.removeSelectedText()
        
        # dash
        # insert blank
        elif char == '-':
            if self.__insertBlankDash:
                self.editor.insert(' ')
                self.editor.setCursorPosition(line, col + 1)
        
        # colon
        # 1. skip colon if not last character
        # 2. insert blank if last character
        elif char == ':':
            text = self.editor.text(line)
            if col < len(text) and char == text[col]:
                if self.__colonDetection:
                    self.editor.setSelection(line, col, line, col + 1)
                    self.editor.removeSelectedText()
            elif self.__insertBlankColon:
                if col == len(text.rstrip()):
                    self.editor.insert(' ')
                    self.editor.setCursorPosition(line, col + 1)
        
        # question mark
        # insert blank
        elif char == '?':
            if self.__insertBlankQuestion:
                self.editor.insert(' ')
                self.editor.setCursorPosition(line, col + 1)
        
        # comma
        # insert blank
        elif char == ',':
            if self.__insertBlankComma:
                self.editor.insert(' ')
                self.editor.setCursorPosition(line, col + 1)
        
        # double quote
        # insert double quote
        elif char == '"':
            if self.__insertQuote:
                self.editor.insert('"')
        
        # quote
        # insert quote
        elif char == "'":
            if self.__insertQuote:
                self.editor.insert("'")
        
        # new line
        # indent after line ending with ':'
        elif char == '\n':
            if self.__autoIndentation:
                txt = self.editor.text(line - 1)
                match = re.search(
                    "(?:\||\|-|\|\+|>|>-|>\+|-|:)(\s*)\r?\n",
                    # __IGNORE_WARNING_W605__
                    txt)
                if match is not None:
                    startBlanks = match.start(1)
                    endBlanks = match.end(1)
                    if startBlanks != -1 and startBlanks != endBlanks:
                        # previous line ends with whitespace, e.g. caused by
                        # blank insertion above
                        self.editor.setSelection(line - 1, startBlanks,
                                                 line - 1, endBlanks)
                        self.editor.removeSelectedText()
                    
                    self.editor.indent(line)
                    self.editor.setCursorPosition(line, 0)
                    self.editor.editorCommand(QsciScintilla.SCI_VCHOME)
    
    def __inComment(self, line, col):
        """
        Private method to check, if the cursor is inside a comment.
        
        @param line current line
        @type int
        @param col current position within line
        @type int
        @return flag indicating, if the cursor is inside a comment
        @rtype bool
        """
        txt = self.editor.text(line)
        if col == len(txt):
            col -= 1
        while col >= 0:
            if txt[col] == "#":
                return True
            col -= 1
        return False
