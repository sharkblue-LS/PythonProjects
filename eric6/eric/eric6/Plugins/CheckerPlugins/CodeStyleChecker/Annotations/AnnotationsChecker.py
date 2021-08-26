# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a checker for function type annotations.
"""

import sys
import ast

import AstUtilities


class AnnotationsChecker(object):
    """
    Class implementing a checker for function type annotations.
    """
    Codes = [
        ## Function Annotations
        "A001", "A002", "A003",
        
        ## Method Annotations
        "A101", "A102",
        
        ## Return Annotations
        "A201", "A202", "A203", "A204", "A205", "A206",
        
        ## Annotation Coverage
        "A881",
        
        ## Annotation Complexity
        "A891",
        
        ## Syntax Error
        "A999",
    ]

    def __init__(self, source, filename, select, ignore, expected, repeat,
                 args):
        """
        Constructor
        
        @param source source code to be checked
        @type list of str
        @param filename name of the source file
        @type str
        @param select list of selected codes
        @type list of str
        @param ignore list of codes to be ignored
        @type list of str
        @param expected list of expected codes
        @type list of str
        @param repeat flag indicating to report each occurrence of a code
        @type bool
        @param args dictionary of arguments for the annotation checks
        @type dict
        """
        self.__select = tuple(select)
        self.__ignore = ('',) if select else tuple(ignore)
        self.__expected = expected[:]
        self.__repeat = repeat
        self.__filename = filename
        self.__source = source[:]
        self.__args = args

        # statistics counters
        self.counters = {}
        
        # collection of detected errors
        self.errors = []
        
        checkersWithCodes = [
            (
                self.__checkFunctionAnnotations,
                ("A001", "A002", "A003", "A101", "A102",
                 "A201", "A202", "A203", "A204", "A205", "A206",)
            ),
            (self.__checkAnnotationsCoverage, ("A881",)),
            (self.__checkAnnotationComplexity, ("A891",)),
        ]
        
        self.__defaultArgs = {
            "MinimumCoverage": 75,      # % of type annotation coverage
            "MaximumComplexity": 3,
        }
        
        self.__checkers = []
        for checker, codes in checkersWithCodes:
            if any(not (code and self.__ignoreCode(code))
                    for code in codes):
                self.__checkers.append(checker)
    
    def __ignoreCode(self, code):
        """
        Private method to check if the message code should be ignored.

        @param code message code to check for
        @type str
        @return flag indicating to ignore the given code
        @rtype bool
        """
        return (code.startswith(self.__ignore) and
                not code.startswith(self.__select))
    
    def __error(self, lineNumber, offset, code, *args):
        """
        Private method to record an issue.
        
        @param lineNumber line number of the issue
        @type int
        @param offset position within line of the issue
        @type int
        @param code message code
        @type str
        @param args arguments for the message
        @type list
        """
        if self.__ignoreCode(code):
            return
        
        if code in self.counters:
            self.counters[code] += 1
        else:
            self.counters[code] = 1
        
        # Don't care about expected codes
        if code in self.__expected:
            return
        
        if code and (self.counters[code] == 1 or self.__repeat):
            # record the issue with one based line number
            self.errors.append(
                {
                    "file": self.__filename,
                    "line": lineNumber + 1,
                    "offset": offset,
                    "code": code,
                    "args": args,
                }
            )
    
    def __reportInvalidSyntax(self):
        """
        Private method to report a syntax error.
        """
        exc_type, exc = sys.exc_info()[:2]
        if len(exc.args) > 1:
            offset = exc.args[1]
            if len(offset) > 2:
                offset = offset[1:3]
        else:
            offset = (1, 0)
        self.__error(offset[0] - 1, offset[1] or 0,
                     'A999', exc_type.__name__, exc.args[0])
    
    def __generateTree(self):
        """
        Private method to generate an AST for our source.
        
        @return generated AST
        @rtype ast.Module
        """
        return ast.parse("".join(self.__source), self.__filename)
    
    def run(self):
        """
        Public method to check the given source against annotation issues.
        """
        if not self.__filename:
            # don't do anything, if essential data is missing
            return
        
        if not self.__checkers:
            # don't do anything, if no codes were selected
            return
        
        try:
            self.__tree = self.__generateTree()
        except (SyntaxError, TypeError):
            self.__reportInvalidSyntax()
            return
        
        for check in self.__checkers:
            check()
    
    def __checkFunctionAnnotations(self):
        """
        Private method to check for function annotation issues.
        """
        visitor = FunctionVisitor(self.__source)
        visitor.visit(self.__tree)
        for issue in visitor.issues:
            node = issue[0]
            reason = issue[1]
            params = issue[2:]
            self.__error(node.lineno - 1, node.col_offset, reason, *params)
    
    def __checkAnnotationsCoverage(self):
        """
        Private method to check for function annotation coverage.
        """
        minAnnotationsCoverage = self.__args.get(
            "MinimumCoverage", self.__defaultArgs["MinimumCoverage"])
        if minAnnotationsCoverage == 0:
            # 0 means it is switched off
            return
        
        functionDefs = [
            f for f in ast.walk(self.__tree)
            if isinstance(f, (ast.AsyncFunctionDef, ast.FunctionDef))
        ]
        if not functionDefs:
            # no functions/methods at all
            return
        
        functionDefAnnotationsInfo = [
            hasTypeAnnotations(f) for f in functionDefs
        ]
        annotationsCoverage = int(
            len(list(filter(None, functionDefAnnotationsInfo))) /
            len(functionDefAnnotationsInfo) * 100
        )
        if annotationsCoverage < minAnnotationsCoverage:
            self.__error(0, 0, "A881", annotationsCoverage)
    
    def __checkAnnotationComplexity(self):
        """
        Private method to check the type annotation complexity.
        """
        maxAnnotationComplexity = self.__args.get(
            "MaximumComplexity", self.__defaultArgs["MaximumComplexity"])
        typeAnnotations = []
        
        functionDefs = [
            f for f in ast.walk(self.__tree)
            if isinstance(f, (ast.AsyncFunctionDef, ast.FunctionDef))
        ]
        for functionDef in functionDefs:
            typeAnnotations += list(filter(
                None, [a.annotation for a in functionDef.args.args]))
            if functionDef.returns:
                typeAnnotations.append(functionDef.returns)
        typeAnnotations += [a.annotation for a in ast.walk(self.__tree)
                            if isinstance(a, ast.AnnAssign) and a.annotation]
        for annotation in typeAnnotations:
            complexity = getAnnotationComplexity(annotation)
            if complexity > maxAnnotationComplexity:
                self.__error(annotation.lineno - 1, annotation.col_offset,
                             "A891", complexity, maxAnnotationComplexity)


class FunctionVisitor(ast.NodeVisitor):
    """
    Class implementing a node visitor to check function annotations.
    
    Note: this class is modelled after flake8-annotations checker.
    """
    def __init__(self, sourceLines):
        """
        Constructor
        
        @param sourceLines lines of source code
        @type list of str
        """
        super(FunctionVisitor, self).__init__()
        
        self.__sourceLines = sourceLines
        
        self.issues = []
    
    def visit_FunctionDef(self, node):
        """
        Public method to handle a function or method definition.
        
        @param node reference to the node to be processed
        @type ast.FunctionDef
        """
        self.__checkFunctionNode(node)
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        """
        Public method to handle an async function or method definition.
        
        @param node reference to the node to be processed
        @type ast.AsyncFunctionDef
        """
        self.__checkFunctionNode(node)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        """
        Public method to handle class definitions.
        
        @param node reference to the node to be processed
        @type ast.ClassDef
        """
        methodNodes = [
            childNode for childNode in node.body
            if isinstance(childNode, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        for methodNode in methodNodes:
            self.__checkFunctionNode(methodNode, classMethod=True)
    
    def __checkFunctionNode(self, node, classMethod=False):
        """
        Private method to check an individual function definition node.
        
        @param node reference to the node to be processed
        @type ast.FunctionDef or ast.AsyncFunctionDef
        @param classMethod flag indicating a class method
        @type bool
        """
        if node.name.startswith("__") and node.name.endswith("__"):
            visibilityType = "special"
        elif node.name.startswith("__"):
            visibilityType = "private"
        elif node.name.startswith("_"):
            visibilityType = "protected"
        else:
            visibilityType = "public"
        
        if classMethod:
            decorators = [
                decorator.id for decorator in node.decorator_list
                if isinstance(decorator, ast.Name)
            ]
            if "classmethod" in decorators:
                classMethodType = "decorator"
            elif "staticmethod" in decorators:
                classMethodType = "staticmethod"
            else:
                classMethodType = ""
        else:
            classMethodType = "function"
        
        # check argument annotations
        for argType in ("args", "vararg", "kwonlyargs", "kwarg"):
            args = node.args.__getattribute__(argType)
            if args:
                if not isinstance(args, list):
                    args = [args]
                
                for arg in args:
                    if not arg.annotation:
                        self.__classifyArgumentError(
                            arg, argType, classMethodType)
        
        # check function return annotation
        if not node.returns:
            lineno = node.lineno
            colOffset = self.__sourceLines[lineno - 1].rfind(":") + 1
            self.__classifyReturnError(classMethodType, visibilityType,
                                       lineno, colOffset)
    
    def __classifyReturnError(self, methodType, visibilityType, lineno,
                              colOffset):
        """
        Private method to classify and record a return annotation issue.
        
        @param methodType type of method/function the argument belongs to
        @type str
        @param visibilityType visibility of the function
        @type str
        @param lineno line number
        @type int
        @param colOffset column number
        @type int
        """
        # create a dummy AST node to report line and column
        node = ast.AST()
        node.lineno = lineno
        node.col_offset = colOffset
        
        # now classify the issue
        if methodType == "classmethod":
            self.issues.append((node, "A206"))
        elif methodType == "staticmethod":
            self.issues.append((node, "A205"))
        elif visibilityType == "special":
            self.issues.append((node, "A204"))
        elif visibilityType == "private":
            self.issues.append((node, "A203"))
        elif visibilityType == "protected":
            self.issues.append((node, "A202"))
        else:
            self.issues.append((node, "A201"))
    
    def __classifyArgumentError(self, argNode, argType, methodType):
        """
        Private method to classify and record an argument annotation issue.
        
        @param argNode reference to the argument node
        @type ast.arguments
        @param argType type of the argument node
        @type str
        @param methodType type of method/function the argument belongs to
        @type str
        """
        # check class method issues
        if methodType != "function":
            if argNode.arg in ("cls", "self"):
                if methodType == "classmethod":
                    self.issues.append((argNode, "A102"))
                    return
                elif methodType != "staticmethod":
                    self.issues.append((argNode, "A101"))
                    return
        
        # check all other arguments
        if argType == "kwarg":
            self.issues.append((argNode, "A003", argNode.arg))
        elif argType == "vararg":
            self.issues.append((argNode, "A002", argNode.arg))
        else:
            # args and kwonlyargs
            self.issues.append((argNode, "A001", argNode.arg))

######################################################################
## some utility functions below
######################################################################


def hasTypeAnnotations(funcNode):
    """
    Function to check for type annotations.
    
    @param funcNode reference to the function definition node to be checked
    @type ast.AsyncFunctionDef or ast.FunctionDef
    @return flag indicating the presence of type annotations
    @rtype bool
    """
    hasReturnAnnotation = funcNode.returns is not None
    hasArgsAnnotations = any(a for a in funcNode.args.args
                             if a.annotation is not None)
    hasKwargsAnnotations = (funcNode.args and
                            funcNode.args.kwarg and
                            funcNode.args.kwarg.annotation is not None)
    hasKwonlyargsAnnotations = any(a for a in funcNode.args.kwonlyargs
                                   if a.annotation is not None)
    
    return any((hasReturnAnnotation, hasArgsAnnotations, hasKwargsAnnotations,
               hasKwonlyargsAnnotations))


def getAnnotationComplexity(annotationNode):
    """
    Function to determine the annotation complexity.
    
    @param annotationNode reference to the node to determine the annotation
        complexity for
    @type ast.AST
    @return annotation complexity
    @rtype = int
    """
    if AstUtilities.isString(annotationNode):
        annotationNode = ast.parse(annotationNode.s).body[0].value
    if isinstance(annotationNode, ast.Subscript):
        return 1 + getAnnotationComplexity(annotationNode.slice.value)
    if isinstance(annotationNode, ast.Tuple):
        return max(getAnnotationComplexity(n) for n in annotationNode.elts)
    return 1
