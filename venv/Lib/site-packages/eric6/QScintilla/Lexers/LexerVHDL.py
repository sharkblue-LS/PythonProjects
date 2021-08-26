# -*- coding: utf-8 -*-

# Copyright (c) 2007 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a VHDL lexer with some additional methods.
"""

from PyQt5.Qsci import QsciLexerVHDL

from .Lexer import Lexer
import Preferences


class LexerVHDL(Lexer, QsciLexerVHDL):
    """
    Subclass to implement some additional lexer dependant methods.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent parent widget of this lexer
        """
        QsciLexerVHDL.__init__(self, parent)
        Lexer.__init__(self)
        
        self.commentString = "--"
        
        self.keywordSetDescriptions = [
            self.tr("Keywords"),
            self.tr("Operators"),
            self.tr("Attributes"),
            self.tr("Standard Functions"),
            self.tr("Standard Packages"),
            self.tr("Standard Types"),
            self.tr("User defined"),
        ]
    
    def initProperties(self):
        """
        Public slot to initialize the properties.
        """
        self.setFoldComments(Preferences.getEditor("VHDLFoldComment"))
        self.setFoldAtElse(Preferences.getEditor("VHDLFoldAtElse"))
        self.setFoldAtBegin(Preferences.getEditor("VHDLFoldAtBegin"))
        self.setFoldAtParenthesis(
            Preferences.getEditor("VHDLFoldAtParenthesis"))
        self.setFoldCompact(Preferences.getEditor("AllFoldCompact"))
    
    def isCommentStyle(self, style):
        """
        Public method to check, if a style is a comment style.
        
        @param style style to check (integer)
        @return flag indicating a comment style (boolean)
        """
        return style in [QsciLexerVHDL.Comment,
                         QsciLexerVHDL.CommentLine]
    
    def isStringStyle(self, style):
        """
        Public method to check, if a style is a string style.
        
        @param style style to check (integer)
        @return flag indicating a string style (boolean)
        """
        return style in [QsciLexerVHDL.String,
                         QsciLexerVHDL.UnclosedString]
    
    def defaultKeywords(self, kwSet):
        """
        Public method to get the default keywords.
        
        @param kwSet number of the keyword set (integer)
        @return string giving the keywords (string) or None
        """
        return QsciLexerVHDL.keywords(self, kwSet)
    
    def maximumKeywordSet(self):
        """
        Public method to get the maximum keyword set.
        
        @return maximum keyword set (integer)
        """
        return 7
