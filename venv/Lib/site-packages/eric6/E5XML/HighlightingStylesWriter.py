# -*- coding: utf-8 -*-

# Copyright (c) 2008 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the writer class for writing a highlighting styles XML
file.
"""

import time

from .XMLStreamWriterBase import XMLStreamWriterBase
from .Config import highlightingStylesFileFormatVersion

import Preferences


class HighlightingStylesWriter(XMLStreamWriterBase):
    """
    Class implementing the writer class for writing a highlighting styles XML
    file.
    """
    def __init__(self, device, lexers):
        """
        Constructor
        
        @param device reference to the I/O device to write to (QIODevice)
        @param lexers list of lexer objects for which to export the styles
        """
        XMLStreamWriterBase.__init__(self, device)
        
        self.lexers = lexers
        self.email = Preferences.getUser("Email")
    
    def writeXML(self):
        """
        Public method to write the XML to the file.
        """
        XMLStreamWriterBase.writeXML(self)
        
        self.writeDTD(
            '<!DOCTYPE HighlightingStyles SYSTEM'
            ' "HighlightingStyles-{0}.dtd">'.format(
                highlightingStylesFileFormatVersion))
        
        # add some generation comments
        self.writeComment(" Eric highlighting styles ")
        self.writeComment(
            " Saved: {0}".format(time.strftime('%Y-%m-%d, %H:%M:%S')))
        self.writeComment(" Author: {0} ".format(self.email))
        
        # add the main tag
        self.writeStartElement("HighlightingStyles")
        self.writeAttribute("version", highlightingStylesFileFormatVersion)
        
        for lexer in self.lexers:
            self.writeStartElement("Lexer")
            self.writeAttribute("name", lexer.language())
            for description, style, substyle in lexer.getStyles():
                self.writeStartElement("Style")
                self.writeAttribute("style", str(style))
                self.writeAttribute("substyle", str(substyle))
                self.writeAttribute("color",
                                    lexer.color(style, substyle).name())
                self.writeAttribute("paper",
                                    lexer.paper(style, substyle).name())
                self.writeAttribute("font",
                                    lexer.font(style, substyle).toString())
                self.writeAttribute("eolfill",
                                    str(lexer.eolFill(style, substyle)))
                self.writeStartElement("Description")
                self.writeCharacters(description)
                self.writeEndElement()      # Description
                if substyle >= 0:
                    self.writeStartElement("Words")
                    self.writeCharacters(lexer.words(style, substyle).strip())
                    self.writeEndElement()      # Words
                self.writeEndElement()      # Style
            self.writeEndElement()          # Lexer
        
        self.writeEndElement()              # HighlightingStyles
        self.writeEndDocument()
