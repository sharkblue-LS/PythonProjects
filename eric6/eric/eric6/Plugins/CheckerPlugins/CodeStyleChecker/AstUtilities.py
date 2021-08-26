# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing some utility and compatibility functions for working with
the ast module.
"""

import sys
import ast

if sys.version_info >= (3, 8, 0):
    # functions for Python >= 3.8
    
    import numbers
    
    def isNumber(node):
        """
        Function to check that a node is a number.
        
        @param node reference to the node to check
        @type ast.AST
        @return flag indicating a number
        @rtype bool
        """
        return (
            isinstance(node, ast.Constant) and
            isinstance(node.value, numbers.Number)
        )
    
    def isString(node):
        """
        Function to check that a node is a string.
        
        @param node reference to the node to check
        @type ast.AST
        @return flag indicating a string
        @rtype bool
        """
        return (
            isinstance(node, ast.Constant) and
            isinstance(node.value, str)
        )
    
    def isBytes(node):
        """
        Function to check that a node is a bytes.
        
        @param node reference to the node to check
        @type ast.AST
        @return flag indicating a bytes
        @rtype bool
        """
        return (
            isinstance(node, ast.Constant) and
            isinstance(node.value, bytes)
        )
    
    def isBaseString(node):
        """
        Function to check that a node is a bytes or string.
        
        @param node reference to the node to check
        @type ast.AST
        @return flag indicating a bytes or string
        @rtype bool
        """
        return (
            isinstance(node, ast.Constant) and
            isinstance(node.value, (bytes, str))
        )
    
    def isNameConstant(node):
        """
        Function to check that a node is a name constant.
        
        @param node reference to the node to check
        @type ast.AST
        @return flag indicating a name constant
        @rtype bool
        """
        return (
            isinstance(node, ast.Constant) and
            not isinstance(node.value, (bytes, str, numbers.Number))
        )
    
    def getValue(node):
        """
        Function to extract the value of a node.
        
        @param node reference to the node to extract the value from
        @type ast.Constant
        @return value of the node
        @rtype any
        @exception TypeError raised to indicate an unsupported type
        """
        if isinstance(node, ast.Constant):
            return node.value
        else:
            raise TypeError("Illegal node type passed.")

else:
    # functions for Python < 3.8
    
    def isNumber(node):
        """
        Function to check that a node is a number.
        
        @param node reference to the node to check
        @type ast.AST
        @return flag indicating a number
        @rtype bool
        """
        return isinstance(node, ast.Num)
    
    def isString(node):
        """
        Function to check that a node is a string.
        
        @param node reference to the node to check
        @type ast.AST
        @return flag indicating a string
        @rtype bool
        """
        return isinstance(node, ast.Str)
    
    def isBytes(node):
        """
        Function to check that a node is a bytes.
        
        @param node reference to the node to check
        @type ast.AST
        @return flag indicating a bytes
        @rtype bool
        """
        return isinstance(node, ast.Bytes)
    
    def isBaseString(node):
        """
        Function to check that a node is a bytes or string.
        
        @param node reference to the node to check
        @type ast.AST
        @return flag indicating a bytes or string
        @rtype bool
        """
        return isinstance(node, (ast.Str, ast.Bytes))
    
    def isNameConstant(node):
        """
        Function to check that a node is a name constant.
        
        @param node reference to the node to check
        @type ast.AST
        @return flag indicating a name constant
        @rtype bool
        """
        return isinstance(node, ast.NameConstant)
    
    def getValue(node):
        """
        Function to extract the value of a node.
        
        @param node reference to the node to extract the value from
        @type one of ast.Num, ast.Str, ast.Bytes or ast.NameConstant
        @return value of the node
        @rtype one of str, bytes, int
        @exception TypeError raised to indicate an unsupported type
        """
        if isinstance(node, ast.Num):
            return node.n
        
        elif isinstance(node, ast.Str):
            return node.s
        
        elif isinstance(node, ast.Bytes):
            return node.s
        
        elif isinstance(node, ast.NameConstant):
            return node.value
        
        else:
            raise TypeError("Illegal node type passed.")
