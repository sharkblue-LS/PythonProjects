# -*- coding: utf-8 -*-

# Copyright (c) 2007 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a Povray lexer with some additional methods.
"""

from PyQt5.Qsci import QsciLexerPOV

from .Lexer import Lexer
import Preferences


class LexerPOV(Lexer, QsciLexerPOV):
    """
    Subclass to implement some additional lexer dependant methods.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent parent widget of this lexer
        """
        QsciLexerPOV.__init__(self, parent)
        Lexer.__init__(self)
        
        self.commentString = "//"
        self.streamCommentString = {
            'start': '/* ',
            'end': ' */'
        }
        self.boxCommentString = {
            'start': '/* ',
            'middle': ' * ',
            'end': ' */'
        }
        
        self.keywordSetDescriptions = [
            self.tr("Language directives"),
            self.tr("Objects & CSG & Appearance"),
            self.tr("Types & Modifiers & Items"),
            self.tr("Predefined Identifiers"),
            self.tr("Predefined Functions"),
            self.tr("User defined 1"),
            self.tr("User defined 2"),
            self.tr("User defined 3"),
        ]
    
    def initProperties(self):
        """
        Public slot to initialize the properties.
        """
        self.setFoldComments(Preferences.getEditor("PovFoldComment"))
        self.setFoldDirectives(Preferences.getEditor("PovFoldDirectives"))
        self.setFoldCompact(Preferences.getEditor("AllFoldCompact"))
    
    def isCommentStyle(self, style):
        """
        Public method to check, if a style is a comment style.
        
        @param style style to check (integer)
        @return flag indicating a comment style (boolean)
        """
        return style in [QsciLexerPOV.Comment,
                         QsciLexerPOV.CommentLine]
    
    def isStringStyle(self, style):
        """
        Public method to check, if a style is a string style.
        
        @param style style to check (integer)
        @return flag indicating a string style (boolean)
        """
        return style in [QsciLexerPOV.String,
                         QsciLexerPOV.UnclosedString]
    
    def defaultKeywords(self, kwSet):
        """
        Public method to get the default keywords.
        
        @param kwSet number of the keyword set (integer)
        @return string giving the keywords (string) or None
        """
        return QsciLexerPOV.keywords(self, kwSet)
