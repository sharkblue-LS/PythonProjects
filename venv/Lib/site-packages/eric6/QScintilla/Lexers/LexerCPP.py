# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a CPP lexer with some additional methods.
"""

from PyQt5.Qsci import QsciLexerCPP, QsciScintilla

from .SubstyledLexer import SubstyledLexer
import Preferences


class LexerCPP(SubstyledLexer, QsciLexerCPP):
    """
    Subclass to implement some additional lexer dependant methods.
    """
    def __init__(self, parent=None, caseInsensitiveKeywords=False):
        """
        Constructor
        
        @param parent parent widget of this lexer
        @param caseInsensitiveKeywords flag indicating keywords are case
            insensitive (boolean)
        """
        QsciLexerCPP.__init__(self, parent, caseInsensitiveKeywords)
        SubstyledLexer.__init__(self)
        
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
            self.tr("Primary keywords and identifiers"),
            self.tr("Secondary keywords and identifiers"),
            self.tr("Documentation comment keywords"),
            self.tr("Global classes and typedefs"),
            self.tr("Preprocessor definitions"),
            self.tr("Task marker and error marker keywords"),
        ]
        
        ##############################################################
        ## default sub-style definitions
        ##############################################################
        
        diffToSecondary = 0x40
        # This may need to be changed to be in line with Scintilla C++ lexer.
        
        # list of style numbers, that support sub-styling
        self.baseStyles = [11, 17, 11 + diffToSecondary, 17 + diffToSecondary]
        
        self.defaultSubStyles = {
            11: {
                0: {
                    "Description": self.tr("Additional Identifier"),
                    "Words": "std map string vector",
                    "Style": {
                        "fore": 0xEE00AA,
                    }
                },
            },
            17: {
                0: {
                    "Description": self.tr("Additional JavaDoc keyword"),
                    "Words": "check",
                    "Style": {
                        "fore": 0x00AAEE,
                    }
                },
            },
            11 + diffToSecondary: {
                0: {
                    "Description": self.tr("Inactive additional identifier"),
                    "Words": "std map string vector",
                    "Style": {
                        "fore": 0xBB6666,
                    }
                },
            },
            17 + diffToSecondary: {
                0: {
                    "Description": self.tr(
                        "Inactive additional JavaDoc keyword"),
                    "Words": "check",
                    "Style": {
                        "fore": 0x6699AA,
                    }
                },
            },
        }

    def initProperties(self):
        """
        Public slot to initialize the properties.
        """
        self.setFoldComments(Preferences.getEditor("CppFoldComment"))
        self.setFoldPreprocessor(Preferences.getEditor("CppFoldPreprocessor"))
        self.setFoldAtElse(Preferences.getEditor("CppFoldAtElse"))
        indentStyle = 0
        if Preferences.getEditor("CppIndentOpeningBrace"):
            indentStyle |= QsciScintilla.AiOpening
        if Preferences.getEditor("CppIndentClosingBrace"):
            indentStyle |= QsciScintilla.AiClosing
        self.setAutoIndentStyle(indentStyle)
        self.setFoldCompact(Preferences.getEditor("AllFoldCompact"))
        try:
            self.setDollarsAllowed(Preferences.getEditor("CppDollarsAllowed"))
        except AttributeError:
            pass
        try:
            self.setStylePreprocessor(
                Preferences.getEditor("CppStylePreprocessor"))
        except AttributeError:
            pass
        try:
            self.setHighlightTripleQuotedStrings(
                Preferences.getEditor("CppHighlightTripleQuotedStrings"))
        except AttributeError:
            pass
        try:
            self.setHighlightHashQuotedStrings(
                Preferences.getEditor("CppHighlightHashQuotedStrings"))
        except AttributeError:
            pass
        try:
            self.setHighlightBackQuotedStrings(
                Preferences.getEditor("CppHighlightBackQuotedStrings"))
        except AttributeError:
            pass
        try:
            self.setHighlightEscapeSequences(
                Preferences.getEditor("CppHighlightEscapeSequences"))
        except AttributeError:
            pass
        try:
            self.setVerbatimStringEscapeSequencesAllowed(
                Preferences.getEditor(
                    "CppVerbatimStringEscapeSequencesAllowed"))
        except AttributeError:
            pass
    
    def autoCompletionWordSeparators(self):
        """
        Public method to return the list of separators for autocompletion.
        
        @return list of separators (list of strings)
        """
        return ['::', '->', '.']
    
    def isCommentStyle(self, style):
        """
        Public method to check, if a style is a comment style.
        
        @param style style to check (integer)
        @return flag indicating a comment style (boolean)
        """
        return style in [QsciLexerCPP.Comment,
                         QsciLexerCPP.CommentDoc,
                         QsciLexerCPP.CommentLine,
                         QsciLexerCPP.CommentLineDoc]
    
    def isStringStyle(self, style):
        """
        Public method to check, if a style is a string style.
        
        @param style style to check (integer)
        @return flag indicating a string style (boolean)
        """
        return style in [QsciLexerCPP.DoubleQuotedString,
                         QsciLexerCPP.SingleQuotedString,
                         QsciLexerCPP.UnclosedString,
                         QsciLexerCPP.VerbatimString]
    
    def defaultKeywords(self, kwSet):
        """
        Public method to get the default keywords.
        
        @param kwSet number of the keyword set (integer)
        @return string giving the keywords (string) or None
        """
        return QsciLexerCPP.keywords(self, kwSet)
    
    def maximumKeywordSet(self):
        """
        Public method to get the maximum keyword set.
        
        @return maximum keyword set (integer)
        """
        return 4
