# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a checker for miscellaneous checks.
"""

import sys
import ast
import re
import itertools
from string import Formatter
from collections import defaultdict
import tokenize

import AstUtilities

from .eradicate import Eradicator

from .MiscellaneousDefaults import MiscellaneousCheckerDefaultArgs


def composeCallPath(node):
    """
    Generator function to assemble the call path of a given node.
    
    @param node node to assemble call path for
    @type ast.Node
    @yield call path components
    @ytype str
    """
    if isinstance(node, ast.Attribute):
        for v in composeCallPath(node.value):
            yield v
        yield node.attr
    elif isinstance(node, ast.Name):
        yield node.id


class MiscellaneousChecker(object):
    """
    Class implementing a checker for miscellaneous checks.
    """
    Codes = [
        ## Coding line
        "M101", "M102",
        
        ## Copyright
        "M111", "M112",
        
        ## Shadowed Builtins
        "M131", "M132",
        
        ## Comprehensions
        "M181", "M182", "M183", "M184",
        "M185", "M186", "M187",
        "M191", "M192", "M193",
        "M195", "M196", "M197", "M198",
        
        ## Dictionaries with sorted keys
        "M201",
        
        ## Naive datetime usage
        "M301", "M302", "M303", "M304", "M305", "M306", "M307", "M308",
        "M311", "M312", "M313", "M314", "M315",
        "M321",
        
        ## sys.version and sys.version_info usage
        "M401", "M402", "M403",
        "M411", "M412", "M413", "M414",
        "M421", "M422", "M423",
        
        ## Bugbear
        "M501", "M502", "M503", "M504", "M505", "M506", "M507", "M508",
        "M509",
        "M511", "M512", "M513",
        "M521", "M522", "M523", "M524",
        
        ## Format Strings
        "M601",
        "M611", "M612", "M613",
        "M621", "M622", "M623", "M624", "M625",
        "M631", "M632",
        
        ## Logging
        "M651", "M652", "M653", "M654", "M655",
        
        ## Future statements
        "M701", "M702",
        
        ## Gettext
        "M711",
        
        ## print
        "M801",
        
        ## one element tuple
        "M811",
        
        ## Mutable Defaults
        "M821", "M822",
        
        ## return statements
        "M831", "M832", "M833", "M834",
        
        ## line continuation
        "M841",
        
        ## commented code
        "M891",
        
        ## syntax error
        "M901",
    ]
    
    Formatter = Formatter()
    FormatFieldRegex = re.compile(r'^((?:\s|.)*?)(\..*|\[.*\])?$')
    
    BuiltinsWhiteList = [
        "__name__",
        "__doc__",
        "credits",
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
        @param args dictionary of arguments for the miscellaneous checks
        @type dict
        """
        self.__select = tuple(select)
        self.__ignore = ('',) if select else tuple(ignore)
        self.__expected = expected[:]
        self.__repeat = repeat
        self.__filename = filename
        self.__source = source[:]
        self.__args = args
        
        self.__pep3101FormatRegex = re.compile(
            r'^(?:[^\'"]*[\'"][^\'"]*[\'"])*\s*%|^\s*%')
        
        import builtins
        self.__builtins = [b for b in dir(builtins)
                           if b not in self.BuiltinsWhiteList]
        
        self.__eradicator = Eradicator()
        
        # statistics counters
        self.counters = {}
        
        # collection of detected errors
        self.errors = []
        
        checkersWithCodes = [
            (self.__checkCoding, ("M101", "M102")),
            (self.__checkCopyright, ("M111", "M112")),
            (self.__checkBuiltins, ("M131", "M132")),
            (self.__checkComprehensions, ("M181", "M182", "M183", "M184",
                                          "M185", "M186", "M187",
                                          "M191", "M192", "M193",
                                          "M195", "M196", "M197", "M198")),
            (self.__checkDictWithSortedKeys, ("M201",)),
            (self.__checkDateTime, ("M301", "M302", "M303", "M304", "M305",
                                    "M306", "M307", "M308", "M311", "M312",
                                    "M313", "M314", "M315", "M321")),
            (self.__checkSysVersion, ("M401", "M402", "M403",
                                      "M411", "M412", "M413", "M414",
                                      "M421", "M422", "M423")),
            (self.__checkBugBear, ("M501", "M502", "M503", "M504", "M505",
                                   "M506", "M507", "M508", "M509",
                                   "M511", "M512", "M513",
                                   "M521", "M522", "M523", "M524")),
            (self.__checkPep3101, ("M601",)),
            (self.__checkFormatString, ("M611", "M612", "M613",
                                        "M621", "M622", "M623", "M624", "M625",
                                        "M631", "M632")),
            (self.__checkLogging, ("M651", "M652", "M653", "M654", "M655")),
            (self.__checkFuture, ("M701", "M702")),
            (self.__checkGettext, ("M711",)),
            (self.__checkPrintStatements, ("M801",)),
            (self.__checkTuple, ("M811",)),
            (self.__checkMutableDefault, ("M821", "M822")),
            (self.__checkReturn, ("M831", "M832", "M833", "M834")),
            (self.__checkLineContinuation, ("M841",)),
            (self.__checkCommentedCode, ("M891",)),
        ]
        
        # the eradicate whitelist
        commentedCodeCheckerArgs = self.__args.get(
            "CommentedCodeChecker",
            MiscellaneousCheckerDefaultArgs["CommentedCodeChecker"])
        commentedCodeCheckerWhitelist = commentedCodeCheckerArgs.get(
            "WhiteList",
            MiscellaneousCheckerDefaultArgs[
                "CommentedCodeChecker"]["WhiteList"])
        self.__eradicator.update_whitelist(commentedCodeCheckerWhitelist,
                                           extend_default=False)
        
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
                     'M901', exc_type.__name__, exc.args[0])
    
    def __generateTree(self):
        """
        Private method to generate an AST for our source.
        
        @return generated AST
        @rtype ast.AST
        """
        return ast.parse("".join(self.__source), self.__filename)
    
    def run(self):
        """
        Public method to check the given source against miscellaneous
        conditions.
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
    
    def __getCoding(self):
        """
        Private method to get the defined coding of the source.
        
        @return tuple containing the line number and the coding
        @rtype tuple of int and str
        """
        for lineno, line in enumerate(self.__source[:5]):
            matched = re.search(r'coding[:=]\s*([-\w_.]+)',
                                line, re.IGNORECASE)
            if matched:
                return lineno, matched.group(1)
        else:
            return 0, ""
    
    def __checkCoding(self):
        """
        Private method to check the presence of a coding line and valid
        encodings.
        """
        if len(self.__source) == 0:
            return
        
        encodings = [e.lower().strip()
                     for e in self.__args.get(
                     "CodingChecker",
                     MiscellaneousCheckerDefaultArgs["CodingChecker"])
                     .split(",")]
        lineno, coding = self.__getCoding()
        if coding:
            if coding.lower() not in encodings:
                self.__error(lineno, 0, "M102", coding)
        else:
            self.__error(0, 0, "M101")
    
    def __checkCopyright(self):
        """
        Private method to check the presence of a copyright statement.
        """
        source = "".join(self.__source)
        copyrightArgs = self.__args.get(
            "CopyrightChecker",
            MiscellaneousCheckerDefaultArgs["CopyrightChecker"])
        copyrightMinFileSize = copyrightArgs.get(
            "MinFilesize",
            MiscellaneousCheckerDefaultArgs["CopyrightChecker"]["MinFilesize"])
        copyrightAuthor = copyrightArgs.get(
            "Author",
            MiscellaneousCheckerDefaultArgs["CopyrightChecker"]["Author"])
        copyrightRegexStr = (
            r"Copyright\s+(\(C\)\s+)?(\d{{4}}\s+-\s+)?\d{{4}}\s+{author}"
        )
        
        tocheck = max(1024, copyrightMinFileSize)
        topOfSource = source[:tocheck]
        if len(topOfSource) < copyrightMinFileSize:
            return

        copyrightRe = re.compile(copyrightRegexStr.format(author=r".*"),
                                 re.IGNORECASE)
        if not copyrightRe.search(topOfSource):
            self.__error(0, 0, "M111")
            return
        
        if copyrightAuthor:
            copyrightAuthorRe = re.compile(
                copyrightRegexStr.format(author=copyrightAuthor),
                re.IGNORECASE)
            if not copyrightAuthorRe.search(topOfSource):
                self.__error(0, 0, "M112")
    
    def __checkCommentedCode(self):
        """
        Private method to check for commented code.
        """
        source = "".join(self.__source)
        commentedCodeCheckerArgs = self.__args.get(
            "CommentedCodeChecker",
            MiscellaneousCheckerDefaultArgs["CommentedCodeChecker"])
        aggressive = commentedCodeCheckerArgs.get(
            "Aggressive",
            MiscellaneousCheckerDefaultArgs[
                "CommentedCodeChecker"]["Aggressive"])
        for markedLine in self.__eradicator.commented_out_code_line_numbers(
                source, aggressive=aggressive):
            self.__error(markedLine - 1, 0, "M891")
    
    def __checkLineContinuation(self):
        """
        Private method to check line continuation using backslash.
        """
        # generate source lines without comments
        linesIterator = iter(self.__source)
        tokens = tokenize.generate_tokens(lambda: next(linesIterator))
        comments = [token for token in tokens if token[0] == tokenize.COMMENT]
        stripped = self.__source[:]
        for comment in comments:
            lineno = comment[3][0]
            start = comment[2][1]
            stop = comment[3][1]
            content = stripped[lineno - 1]
            withoutComment = content[:start] + content[stop:]
            stripped[lineno - 1] = withoutComment.rstrip()
        
        # perform check with 'cleaned' source
        for lineIndex, line in enumerate(stripped):
            strippedLine = line.strip()
            if (strippedLine.endswith('\\') and
                    not strippedLine.startswith(('assert', 'with'))):
                self.__error(lineIndex, len(line), "M841")
    
    def __checkPrintStatements(self):
        """
        Private method to check for print statements.
        """
        for node in ast.walk(self.__tree):
            if (
                (isinstance(node, ast.Call) and
                 getattr(node.func, 'id', None) == 'print') or
                (hasattr(ast, 'Print') and isinstance(node, ast.Print))
            ):
                self.__error(node.lineno - 1, node.col_offset, "M801")
    
    def __checkTuple(self):
        """
        Private method to check for one element tuples.
        """
        for node in ast.walk(self.__tree):
            if (
                isinstance(node, ast.Tuple) and
                len(node.elts) == 1
            ):
                self.__error(node.lineno - 1, node.col_offset, "M811")
    
    def __checkFuture(self):
        """
        Private method to check the __future__ imports.
        """
        expectedImports = {
            i.strip()
            for i in self.__args.get("FutureChecker", "").split(",")
            if bool(i.strip())}
        if len(expectedImports) == 0:
            # nothing to check for; disabling the check
            return
        
        imports = set()
        node = None
        hasCode = False
        
        for node in ast.walk(self.__tree):
            if (isinstance(node, ast.ImportFrom) and
                    node.module == '__future__'):
                imports |= {name.name for name in node.names}
            elif isinstance(node, ast.Expr):
                if not AstUtilities.isString(node.value):
                    hasCode = True
                    break
            elif not (
                AstUtilities.isString(node) or
                isinstance(node, ast.Module)
            ):
                hasCode = True
                break

        if isinstance(node, ast.Module) or not hasCode:
            return

        if not (imports >= expectedImports):
            if imports:
                self.__error(node.lineno - 1, node.col_offset, "M701",
                             ", ".join(expectedImports), ", ".join(imports))
            else:
                self.__error(node.lineno - 1, node.col_offset, "M702",
                             ", ".join(expectedImports))
    
    def __checkPep3101(self):
        """
        Private method to check for old style string formatting.
        """
        for lineno, line in enumerate(self.__source):
            match = self.__pep3101FormatRegex.search(line)
            if match:
                lineLen = len(line)
                pos = line.find('%')
                formatPos = pos
                formatter = '%'
                if line[pos + 1] == "(":
                    pos = line.find(")", pos)
                c = line[pos]
                while c not in "diouxXeEfFgGcrs":
                    pos += 1
                    if pos >= lineLen:
                        break
                    c = line[pos]
                if c in "diouxXeEfFgGcrs":
                    formatter += c
                self.__error(lineno, formatPos, "M601", formatter)
    
    def __checkFormatString(self):
        """
        Private method to check string format strings.
        """
        coding = self.__getCoding()[1]
        if not coding:
            # default to utf-8
            coding = "utf-8"
        
        visitor = TextVisitor()
        visitor.visit(self.__tree)
        for node in visitor.nodes:
            text = node.s
            if isinstance(text, bytes):
                try:
                    text = text.decode(coding)
                except UnicodeDecodeError:
                    continue
            fields, implicit, explicit = self.__getFields(text)
            if implicit:
                if node in visitor.calls:
                    self.__error(node.lineno - 1, node.col_offset, "M611")
                else:
                    if node.is_docstring:
                        self.__error(node.lineno - 1, node.col_offset, "M612")
                    else:
                        self.__error(node.lineno - 1, node.col_offset, "M613")
            
            if node in visitor.calls:
                call, strArgs = visitor.calls[node]
                
                numbers = set()
                names = set()
                # Determine which fields require a keyword and which an arg
                for name in fields:
                    fieldMatch = self.FormatFieldRegex.match(name)
                    try:
                        number = int(fieldMatch.group(1))
                    except ValueError:
                        number = -1
                    # negative numbers are considered keywords
                    if number >= 0:
                        numbers.add(number)
                    else:
                        names.add(fieldMatch.group(1))
                
                keywords = {keyword.arg for keyword in call.keywords}
                numArgs = len(call.args)
                if strArgs:
                    numArgs -= 1
                hasKwArgs = any(kw.arg is None for kw in call.keywords)
                hasStarArgs = sum(1 for arg in call.args
                                  if isinstance(arg, ast.Starred))
                
                if hasKwArgs:
                    keywords.discard(None)
                if hasStarArgs:
                    numArgs -= 1
                
                # if starargs or kwargs is not None, it can't count the
                # parameters but at least check if the args are used
                if hasKwArgs:
                    if not names:
                        # No names but kwargs
                        self.__error(call.lineno - 1, call.col_offset, "M623")
                if hasStarArgs:
                    if not numbers:
                        # No numbers but args
                        self.__error(call.lineno - 1, call.col_offset, "M624")
                
                if not hasKwArgs and not hasStarArgs:
                    # can actually verify numbers and names
                    for number in sorted(numbers):
                        if number >= numArgs:
                            self.__error(call.lineno - 1, call.col_offset,
                                         "M621", number)
                    
                    for name in sorted(names):
                        if name not in keywords:
                            self.__error(call.lineno - 1, call.col_offset,
                                         "M622", name)
                
                for arg in range(numArgs):
                    if arg not in numbers:
                        self.__error(call.lineno - 1, call.col_offset, "M631",
                                     arg)
                
                for keyword in keywords:
                    if keyword not in names:
                        self.__error(call.lineno - 1, call.col_offset, "M632",
                                     keyword)
                
                if implicit and explicit:
                    self.__error(call.lineno - 1, call.col_offset, "M625")
    
    def __getFields(self, string):
        """
        Private method to extract the format field information.
        
        @param string format string to be parsed
        @type str
        @return format field information as a tuple with fields, implicit
            field definitions present and explicit field definitions present
        @rtype tuple of set of str, bool, bool
        """
        fields = set()
        cnt = itertools.count()
        implicit = False
        explicit = False
        try:
            for _literal, field, spec, conv in self.Formatter.parse(string):
                if field is not None and (conv is None or conv in 'rsa'):
                    if not field:
                        field = str(next(cnt))
                        implicit = True
                    else:
                        explicit = True
                    fields.add(field)
                    fields.update(parsedSpec[1]
                                  for parsedSpec in self.Formatter.parse(spec)
                                  if parsedSpec[1] is not None)
        except ValueError:
            return set(), False, False
        else:
            return fields, implicit, explicit
    
    def __checkBuiltins(self):
        """
        Private method to check, if built-ins are shadowed.
        """
        functionDefs = [ast.FunctionDef]
        try:
            functionDefs.append(ast.AsyncFunctionDef)
        except AttributeError:
            pass
        
        ignoreBuiltinAssignments = self.__args.get(
            "BuiltinsChecker",
            MiscellaneousCheckerDefaultArgs["BuiltinsChecker"])
        
        for node in ast.walk(self.__tree):
            if isinstance(node, ast.Assign):
                # assign statement
                for element in node.targets:
                    if (
                        isinstance(element, ast.Name) and
                        element.id in self.__builtins
                    ):
                        value = node.value
                        if (
                            isinstance(value, ast.Name) and
                            element.id in ignoreBuiltinAssignments and
                            value.id in ignoreBuiltinAssignments[element.id]
                        ):
                            # ignore compatibility assignments
                            continue
                        self.__error(element.lineno - 1, element.col_offset,
                                     "M131", element.id)
                    elif isinstance(element, (ast.Tuple, ast.List)):
                        for tupleElement in element.elts:
                            if (
                                isinstance(tupleElement, ast.Name) and
                                tupleElement.id in self.__builtins
                            ):
                                self.__error(tupleElement.lineno - 1,
                                             tupleElement.col_offset,
                                             "M131", tupleElement.id)
            elif isinstance(node, ast.For):
                # for loop
                target = node.target
                if (
                    isinstance(target, ast.Name) and
                    target.id in self.__builtins
                ):
                    self.__error(target.lineno - 1, target.col_offset,
                                 "M131", target.id)
                elif isinstance(target, (ast.Tuple, ast.List)):
                    for element in target.elts:
                        if (
                            isinstance(element, ast.Name) and
                            element.id in self.__builtins
                        ):
                            self.__error(element.lineno - 1,
                                         element.col_offset,
                                         "M131", element.id)
            elif any(isinstance(node, functionDef)
                     for functionDef in functionDefs):
                # (asynchronous) function definition
                for arg in node.args.args:
                    if (
                        isinstance(arg, ast.arg) and
                        arg.arg in self.__builtins
                    ):
                        self.__error(arg.lineno - 1, arg.col_offset,
                                     "M132", arg.arg)
    
    def __checkComprehensions(self):
        """
        Private method to check some comprehension related things.
        """
        for node in ast.walk(self.__tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                nArgs = len(node.args)
                
                if (
                    nArgs == 1 and
                    isinstance(node.args[0], ast.GeneratorExp) and
                    node.func.id in ('list', 'set')
                ):
                    errorCode = {
                        "list": "M181",
                        "set": "M182",
                    }[node.func.id]
                    self.__error(node.lineno - 1, node.col_offset, errorCode)

                elif (
                    nArgs == 1 and
                    isinstance(node.args[0], ast.GeneratorExp) and
                    isinstance(node.args[0].elt, ast.Tuple) and
                    len(node.args[0].elt.elts) == 2 and
                    node.func.id == "dict"
                ):
                    self.__error(node.lineno - 1, node.col_offset, "M183")
                
                elif (
                    nArgs == 1 and
                    isinstance(node.args[0], ast.ListComp) and
                    node.func.id in ('list', 'set', 'dict')
                ):
                    errorCode = {
                        'list': 'M195',
                        'dict': 'M185',
                        'set': 'M184',
                    }[node.func.id]
                    self.__error(node.lineno - 1, node.col_offset, errorCode)
                
                elif nArgs == 1 and (
                    isinstance(node.args[0], ast.Tuple) and
                    node.func.id == "tuple" or
                    isinstance(node.args[0], ast.List) and
                    node.func.id == "list"
                ):
                    errorCode = {
                        'tuple': 'M197',
                        'list': 'M198',
                    }[node.func.id]
                    self.__error(node.lineno - 1, node.col_offset, errorCode,
                                 type(node.args[0]).__name__.lower(),
                                 node.func.id)
                
                elif (
                    nArgs == 1 and
                    isinstance(node.args[0], (ast.Tuple, ast.List)) and
                    node.func.id in ("tuple", "list", "set", "dict")
                ):
                    errorCode = {
                        "tuple": "M192",
                        "list": "M193",
                        "set": "M191",
                        "dict": "M191",
                    }[node.func.id]
                    self.__error(node.lineno - 1, node.col_offset, errorCode,
                                 type(node.args[0]).__name__.lower(),
                                 node.func.id)

                elif (
                    nArgs == 1 and
                    isinstance(node.args[0], ast.ListComp) and
                    node.func.id in ('all', 'any', 'enumerate', 'frozenset',
                                     'max', 'min', 'sorted', 'sum', 'tuple',)
                ):
                    self.__error(node.lineno - 1, node.col_offset, "M187",
                                 node.func.id)
                
                elif (
                    nArgs == 0 and
                    not any(isinstance(a, ast.Starred) for a in node.args) and
                    not any(k.arg is None for k in node.keywords) and
                    node.func.id in ("tuple", "list", "dict")
                ):
                    self.__error(node.lineno - 1, node.col_offset, "M186",
                                 node.func.id)
                
                elif isinstance(node, ast.Compare) and (
                    len(node.ops) == 1 and
                    isinstance(node.ops[0], ast.In) and
                    len(node.comparators) == 1 and
                    isinstance(node.comparators[0], ast.ListComp)
                ):
                    self.__error(node.lineno - 1, node.col_offset, "M196")
    
    def __checkMutableDefault(self):
        """
        Private method to check for use of mutable types as default arguments.
        """
        mutableTypes = (
            ast.Call,
            ast.Dict,
            ast.List,
            ast.Set,
        )
        mutableCalls = (
            "Counter",
            "OrderedDict",
            "collections.Counter",
            "collections.OrderedDict",
            "collections.defaultdict",
            "collections.deque",
            "defaultdict",
            "deque",
            "dict",
            "list",
            "set",
        )
        immutableCalls = (
            "tuple",
            "frozenset",
        )
        functionDefs = [ast.FunctionDef]
        try:
            functionDefs.append(ast.AsyncFunctionDef)
        except AttributeError:
            pass
        
        for node in ast.walk(self.__tree):
            if any(isinstance(node, functionDef)
                   for functionDef in functionDefs):
                defaults = node.args.defaults[:]
                try:
                    defaults += node.args.kw_defaults[:]
                except AttributeError:
                    pass
                for default in defaults:
                    if any(isinstance(default, mutableType)
                           for mutableType in mutableTypes):
                        typeName = type(default).__name__
                        if isinstance(default, ast.Call):
                            callPath = '.'.join(composeCallPath(default.func))
                            if callPath in mutableCalls:
                                self.__error(default.lineno - 1,
                                             default.col_offset,
                                             "M823", callPath + "()")
                            elif callPath not in immutableCalls:
                                self.__error(default.lineno - 1,
                                             default.col_offset,
                                             "M822", typeName)
                        else:
                            self.__error(default.lineno - 1,
                                         default.col_offset,
                                         "M821", typeName)
    
    def __dictShouldBeChecked(self, node):
        """
        Private function to test, if the node should be checked.
        
        @param node reference to the AST node
        @return flag indicating to check the node
        @rtype bool
        """
        if not all(AstUtilities.isString(key) for key in node.keys):
            return False
        
        if (
            "__IGNORE_WARNING__" in self.__source[node.lineno - 1] or
            "__IGNORE_WARNING_M201__" in self.__source[node.lineno - 1]
        ):
            return False
        
        lineNumbers = [key.lineno for key in node.keys]
        return len(lineNumbers) == len(set(lineNumbers))
    
    def __checkDictWithSortedKeys(self):
        """
        Private method to check, if dictionary keys appear in sorted order.
        """
        for node in ast.walk(self.__tree):
            if isinstance(node, ast.Dict) and self.__dictShouldBeChecked(node):
                for key1, key2 in zip(node.keys, node.keys[1:]):
                    if key2.s < key1.s:
                        self.__error(key2.lineno - 1, key2.col_offset,
                                     "M201", key2.s, key1.s)
    
    def __checkLogging(self):
        """
        Private method to check logging statements.
        """
        visitor = LoggingVisitor()
        visitor.visit(self.__tree)
        for node, reason in visitor.violations:
            self.__error(node.lineno - 1, node.col_offset, reason)
    
    def __checkGettext(self):
        """
        Private method to check the 'gettext' import statement.
        """
        for node in ast.walk(self.__tree):
            if (
                isinstance(node, ast.ImportFrom) and
                any(name.asname == '_' for name in node.names)
            ):
                self.__error(node.lineno - 1, node.col_offset, "M711",
                             node.names[0].name)
    
    def __checkBugBear(self):
        """
        Private method for bugbear checks.
        """
        visitor = BugBearVisitor()
        visitor.visit(self.__tree)
        for violation in visitor.violations:
            node = violation[0]
            reason = violation[1]
            params = violation[2:]
            self.__error(node.lineno - 1, node.col_offset, reason, *params)
    
    def __checkReturn(self):
        """
        Private method to check return statements.
        """
        visitor = ReturnVisitor()
        visitor.visit(self.__tree)
        for violation in visitor.violations:
            node = violation[0]
            reason = violation[1]
            self.__error(node.lineno - 1, node.col_offset, reason)
    
    def __checkDateTime(self):
        """
        Private method to check use of naive datetime functions.
        """
        # step 1: generate an augmented node tree containing parent info
        #         for each child node
        tree = self.__generateTree()
        for node in ast.walk(tree):
            for childNode in ast.iter_child_nodes(node):
                childNode._dtCheckerParent = node
        
        # step 2: perform checks and report issues
        visitor = DateTimeVisitor()
        visitor.visit(tree)
        for violation in visitor.violations:
            node = violation[0]
            reason = violation[1]
            self.__error(node.lineno - 1, node.col_offset, reason)
    
    def __checkSysVersion(self):
        """
        Private method to check the use of sys.version and sys.version_info.
        """
        visitor = SysVersionVisitor()
        visitor.visit(self.__tree)
        for violation in visitor.violations:
            node = violation[0]
            reason = violation[1]
            self.__error(node.lineno - 1, node.col_offset, reason)


class TextVisitor(ast.NodeVisitor):
    """
    Class implementing a node visitor for bytes and str instances.

    It tries to detect docstrings as string of the first expression of each
    module, class or function.
    """
    # modelled after the string format flake8 extension
    
    def __init__(self):
        """
        Constructor
        """
        super(TextVisitor, self).__init__()
        self.nodes = []
        self.calls = {}

    def __addNode(self, node):
        """
        Private method to add a node to our list of nodes.
        
        @param node reference to the node to add
        @type ast.AST
        """
        if not hasattr(node, 'is_docstring'):
            node.is_docstring = False
        self.nodes.append(node)

    def visit_Str(self, node):
        """
        Public method to record a string node.
        
        @param node reference to the string node
        @type ast.Str
        """
        self.__addNode(node)

    def visit_Bytes(self, node):
        """
        Public method to record a bytes node.
        
        @param node reference to the bytes node
        @type ast.Bytes
        """
        self.__addNode(node)
    
    def visit_Constant(self, node):
        """
        Public method to handle constant nodes.
        
        @param node reference to the bytes node
        @type ast.Constant
        """
        if sys.version_info >= (3, 8, 0):
            if AstUtilities.isBaseString(node):
                self.__addNode(node)
            else:
                super(TextVisitor, self).generic_visit(node)
        else:
            super(TextVisitor, self).generic_visit(node)

    def __visitDefinition(self, node):
        """
        Private method handling class and function definitions.
        
        @param node reference to the node to handle
        @type ast.FunctionDef, ast.AsyncFunctionDef or ast.ClassDef
        """
        # Manually traverse class or function definition
        # * Handle decorators normally
        # * Use special check for body content
        # * Don't handle the rest (e.g. bases)
        for decorator in node.decorator_list:
            self.visit(decorator)
        self.__visitBody(node)

    def __visitBody(self, node):
        """
        Private method to traverse the body of the node manually.

        If the first node is an expression which contains a string or bytes it
        marks that as a docstring.
        
        @param node reference to the node to traverse
        @type ast.AST
        """
        if (
            node.body and
            isinstance(node.body[0], ast.Expr) and
            AstUtilities.isBaseString(node.body[0].value)
        ):
            node.body[0].value.is_docstring = True

        for subnode in node.body:
            self.visit(subnode)

    def visit_Module(self, node):
        """
        Public method to handle a module.
        
        @param node reference to the node to handle
        @type ast.Module
        """
        self.__visitBody(node)

    def visit_ClassDef(self, node):
        """
        Public method to handle a class definition.
        
        @param node reference to the node to handle
        @type ast.ClassDef
        """
        # Skipped nodes: ('name', 'bases', 'keywords', 'starargs', 'kwargs')
        self.__visitDefinition(node)

    def visit_FunctionDef(self, node):
        """
        Public method to handle a function definition.
        
        @param node reference to the node to handle
        @type ast.FunctionDef
        """
        # Skipped nodes: ('name', 'args', 'returns')
        self.__visitDefinition(node)

    def visit_AsyncFunctionDef(self, node):
        """
        Public method to handle an asynchronous function definition.
        
        @param node reference to the node to handle
        @type ast.AsyncFunctionDef
        """
        # Skipped nodes: ('name', 'args', 'returns')
        self.__visitDefinition(node)

    def visit_Call(self, node):
        """
        Public method to handle a function call.
        
        @param node reference to the node to handle
        @type ast.Call
        """
        if (
            isinstance(node.func, ast.Attribute) and
            node.func.attr == 'format'
        ):
            if AstUtilities.isBaseString(node.func.value):
                self.calls[node.func.value] = (node, False)
            elif (
                isinstance(node.func.value, ast.Name) and
                node.func.value.id == 'str' and
                node.args and
                AstUtilities.isBaseString(node.args[0])
            ):
                self.calls[node.args[0]] = (node, True)
        super(TextVisitor, self).generic_visit(node)


class LoggingVisitor(ast.NodeVisitor):
    """
    Class implementing a node visitor to check logging statements.
    """
    LoggingLevels = {
        "debug",
        "critical",
        "error",
        "info",
        "warn",
        "warning",
    }
    
    def __init__(self):
        """
        Constructor
        """
        super(LoggingVisitor, self).__init__()
        
        self.__currentLoggingCall = None
        self.__currentLoggingArgument = None
        self.__currentLoggingLevel = None
        self.__currentExtraKeyword = None
        self.violations = []

    def __withinLoggingStatement(self):
        """
        Private method to check, if we are inside a logging statement.
        
        @return flag indicating we are inside a logging statement
        @rtype bool
        """
        return self.__currentLoggingCall is not None

    def __withinLoggingArgument(self):
        """
        Private method to check, if we are inside a logging argument.
        
        @return flag indicating we are inside a logging argument
        @rtype bool
        """
        return self.__currentLoggingArgument is not None

    def __withinExtraKeyword(self, node):
        """
        Private method to check, if we are inside the extra keyword.
        
        @param node reference to the node to be checked
        @type ast.keyword
        @return flag indicating we are inside the extra keyword
        @rtype bool
        """
        return (
            self.__currentExtraKeyword is not None and
            self.__currentExtraKeyword != node
        )
    
    def __detectLoggingLevel(self, node):
        """
        Private method to decide whether an AST Call is a logging call.
        
        @param node reference to the node to be processed
        @type ast.Call
        @return logging level
        @rtype str or None
        """
        try:
            if node.func.value.id == "warnings":
                return None
            
            if node.func.attr in LoggingVisitor.LoggingLevels:
                return node.func.attr
        except AttributeError:
            pass
        
        return None

    def __isFormatCall(self, node):
        """
        Private method to check if a function call uses format.

        @param node reference to the node to be processed
        @type ast.Call
        @return flag indicating the function call uses format
        @rtype bool
        """
        try:
            return node.func.attr == "format"
        except AttributeError:
            return False
    
    def visit_Call(self, node):
        """
        Public method to handle a function call.

        Every logging statement and string format is expected to be a function
        call.
        
        @param node reference to the node to be processed
        @type ast.Call
        """
        # we are in a logging statement
        if self.__withinLoggingStatement():
            if self.__withinLoggingArgument() and self.__isFormatCall(node):
                self.violations.append((node, "M651"))
                super(LoggingVisitor, self).generic_visit(node)
                return
        
        loggingLevel = self.__detectLoggingLevel(node)
        
        if loggingLevel and self.__currentLoggingLevel is None:
            self.__currentLoggingLevel = loggingLevel
        
        # we are in some other statement
        if loggingLevel is None:
            super(LoggingVisitor, self).generic_visit(node)
            return
        
        # we are entering a new logging statement
        self.__currentLoggingCall = node
        
        if loggingLevel == "warn":
            self.violations.append((node, "M655"))
        
        for index, child in enumerate(ast.iter_child_nodes(node)):
            if index == 1:
                self.__currentLoggingArgument = child
            if (
                index > 1 and
                isinstance(child, ast.keyword) and
                child.arg == "extra"
            ):
                self.__currentExtraKeyword = child
            
            super(LoggingVisitor, self).visit(child)
            
            self.__currentLoggingArgument = None
            self.__currentExtraKeyword = None
        
        self.__currentLoggingCall = None
        self.__currentLoggingLevel = None
    
    def visit_BinOp(self, node):
        """
        Public method to handle binary operations while processing the first
        logging argument.
        
        @param node reference to the node to be processed
        @type ast.BinOp
        """
        if self.__withinLoggingStatement() and self.__withinLoggingArgument():
            # handle percent format
            if isinstance(node.op, ast.Mod):
                self.violations.append((node, "M652"))
            
            # handle string concat
            if isinstance(node.op, ast.Add):
                self.violations.append((node, "M653"))
        
        super(LoggingVisitor, self).generic_visit(node)
    
    def visit_JoinedStr(self, node):
        """
        Public method to handle f-string arguments.
        
        @param node reference to the node to be processed
        @type ast.JoinedStr
        """
        if self.__withinLoggingStatement():
            if any(isinstance(i, ast.FormattedValue) for i in node.values):
                if self.__withinLoggingArgument():
                    self.violations.append((node, "M654"))
                    
                    super(LoggingVisitor, self).generic_visit(node)


class BugBearVisitor(ast.NodeVisitor):
    """
    Class implementing a node visitor to check for various topics.
    """
    #
    # This class was implemented along the BugBear flake8 extension (v 19.3.0).
    # Original: Copyright (c) 2016 Łukasz Langa
    #
    
    NodeWindowSize = 4
    
    def __init__(self):
        """
        Constructor
        """
        super(BugBearVisitor, self).__init__()
        
        self.__nodeStack = []
        self.__nodeWindow = []
        self.violations = []
    
    def visit(self, node):
        """
        Public method to traverse a given AST node.
        
        @param node AST node to be traversed
        @type ast.Node
        """
        self.__nodeStack.append(node)
        self.__nodeWindow.append(node)
        self.__nodeWindow = self.__nodeWindow[-BugBearVisitor.NodeWindowSize:]
        
        super(BugBearVisitor, self).visit(node)
        
        self.__nodeStack.pop()
    
    def visit_UAdd(self, node):
        """
        Public method to handle unary additions.
        
        @param node reference to the node to be processed
        @type ast.UAdd
        """
        trailingNodes = list(map(type, self.__nodeWindow[-4:]))
        if trailingNodes == [ast.UnaryOp, ast.UAdd, ast.UnaryOp, ast.UAdd]:
            originator = self.__nodeWindow[-4]
            self.violations.append((originator, "M501"))
        
        self.generic_visit(node)
    
    def visit_Call(self, node):
        """
        Public method to handle a function call.
        
        @param node reference to the node to be processed
        @type ast.Call
        """
        validPaths = ("six", "future.utils", "builtins")
        methodsDict = {
            "M521": ("iterkeys", "itervalues", "iteritems", "iterlists"),
            "M522": ("viewkeys", "viewvalues", "viewitems", "viewlists"),
            "M523": ("next",),
        }
        
        if isinstance(node.func, ast.Attribute):
            for code, methods in methodsDict.items():
                if node.func.attr in methods:
                    callPath = ".".join(composeCallPath(node.func.value))
                    if callPath not in validPaths:
                        self.violations.append((node, code))
                    break
            else:
                self.__checkForM502(node)
        else:
            try:
                # bad super() call
                if isinstance(node.func, ast.Name) and node.func.id == "super":
                    args = node.args
                    if (
                        len(args) == 2 and
                        isinstance(args[0], ast.Attribute) and
                        isinstance(args[0].value, ast.Name) and
                        args[0].value.id == 'self' and
                        args[0].attr == '__class__'
                    ):
                        self.violations.append((node, "M509"))
                
                # bad getattr and setattr
                if (
                    node.func.id in ("getattr", "hasattr") and
                    node.args[1].s == "__call__"
                ):
                    self.violations.append((node, "M511"))
                if (
                    node.func.id == "getattr" and
                    len(node.args) == 2 and
                    AstUtilities.isString(node.args[1])
                ):
                    self.violations.append((node, "M512"))
                elif (
                    node.func.id == "setattr" and
                    len(node.args) == 3 and
                    AstUtilities.isString(node.args[1])
                ):
                    self.violations.append((node, "M513"))
            except (AttributeError, IndexError):
                pass

            self.generic_visit(node)
    
    def visit_Attribute(self, node):
        """
        Public method to handle attributes.
        
        @param node reference to the node to be processed
        @type ast.Attribute
        """
        callPath = list(composeCallPath(node))
        
        if '.'.join(callPath) == 'sys.maxint':
            self.violations.append((node, "M504"))
        
        elif (
            len(callPath) == 2 and
            callPath[1] == 'message'
        ):
            name = callPath[0]
            for elem in reversed(self.__nodeStack[:-1]):
                if isinstance(elem, ast.ExceptHandler) and elem.name == name:
                    self.violations.append((node, "M505"))
                    break
    
    def visit_Assign(self, node):
        """
        Public method to handle assignments.
        
        @param node reference to the node to be processed
        @type ast.Assign
        """
        if isinstance(self.__nodeStack[-2], ast.ClassDef):
            # By using 'hasattr' below we're ignoring starred arguments, slices
            # and tuples for simplicity.
            assignTargets = {t.id for t in node.targets if hasattr(t, 'id')}
            if '__metaclass__' in assignTargets:
                self.violations.append((node, "M524"))
        
        elif len(node.targets) == 1:
            target = node.targets[0]
            if (
                isinstance(target, ast.Attribute) and
                isinstance(target.value, ast.Name)
            ):
                if (target.value.id, target.attr) == ('os', 'environ'):
                    self.violations.append((node, "M506"))
        
        self.generic_visit(node)
    
    def visit_For(self, node):
        """
        Public method to handle 'for' statements.
        
        @param node reference to the node to be processed
        @type ast.For
        """
        self.__checkForM507(node)
        
        self.generic_visit(node)
    
    def visit_AsyncFor(self, node):
        """
        Public method to handle 'for' statements.
        
        @param node reference to the node to be processed
        @type ast.AsyncFor
        """
        self.__checkForM507(node)
        
        self.generic_visit(node)
    
    def visit_Assert(self, node):
        """
        Public method to handle 'assert' statements.
        
        @param node reference to the node to be processed
        @type ast.Assert
        """
        if (
            AstUtilities.isNameConstant(node.test) and
            AstUtilities.getValue(node.test) is False
        ):
            self.violations.append((node, "M503"))
        
        self.generic_visit(node)
    
    def visit_JoinedStr(self, node):
        """
        Public method to handle f-string arguments.
        
        @param node reference to the node to be processed
        @type ast.JoinedStr
        """
        for value in node.values:
            if isinstance(value, ast.FormattedValue):
                return
        
        self.violations.append((node, "M508"))
    
    def __checkForM502(self, node):
        """
        Private method to check the use of *strip().
        
        @param node reference to the node to be processed
        @type ast.Call
        """
        if node.func.attr not in ("lstrip", "rstrip", "strip"):
            return          # method name doesn't match
        
        if len(node.args) != 1 or not AstUtilities.isString(node.args[0]):
            return          # used arguments don't match the builtin strip
        
        s = AstUtilities.getValue(node.args[0])
        if len(s) == 1:
            return          # stripping just one character
        
        if len(s) == len(set(s)):
            return          # no characters appear more than once

        self.violations.append((node, "M502"))
    
    def __checkForM507(self, node):
        """
        Private method to check for unused loop variables.
        
        @param node reference to the node to be processed
        @type ast.For
        """
        targets = NameFinder()
        targets.visit(node.target)
        ctrlNames = set(filter(lambda s: not s.startswith('_'),
                               targets.getNames()))
        body = NameFinder()
        for expr in node.body:
            body.visit(expr)
        usedNames = set(body.getNames())
        for name in sorted(ctrlNames - usedNames):
            n = targets.getNames()[name][0]
            self.violations.append((n, "M507", name))


class NameFinder(ast.NodeVisitor):
    """
    Class to extract a name out of a tree of nodes.
    """
    def __init__(self):
        """
        Constructor
        """
        super(NameFinder, self).__init__()
        
        self.__names = {}

    def visit_Name(self, node):
        """
        Public method to handle 'Name' nodes.
        
        @param node reference to the node to be processed
        @type ast.Name
        """
        self.__names.setdefault(node.id, []).append(node)

    def visit(self, node):
        """
        Public method to traverse a given AST node.
        
        @param node AST node to be traversed
        @type ast.Node
        """
        if isinstance(node, list):
            for elem in node:
                super(NameFinder, self).visit(elem)
        else:
            super(NameFinder, self).visit(node)
    
    def getNames(self):
        """
        Public method to return the extracted names and Name nodes.
        
        @return dictionary containing the names as keys and the list of nodes
        @rtype dict
        """
        return self.__names


class ReturnVisitor(ast.NodeVisitor):
    """
    Class implementing a node visitor to check return statements.
    """
    Assigns = 'assigns'
    Refs = 'refs'
    Returns = 'returns'
    
    def __init__(self):
        """
        Constructor
        """
        super(ReturnVisitor, self).__init__()
        
        self.__stack = []
        self.violations = []
        self.__loopCount = 0
    
    @property
    def assigns(self):
        """
        Public method to get the Assign nodes.
        
        @return dictionary containing the node name as key and line number
            as value
        @rtype dict
        """
        return self.__stack[-1][ReturnVisitor.Assigns]
    
    @property
    def refs(self):
        """
        Public method to get the References nodes.
        
        @return dictionary containing the node name as key and line number
            as value
        @rtype dict
        """
        return self.__stack[-1][ReturnVisitor.Refs]
    
    @property
    def returns(self):
        """
        Public method to get the Return nodes.
        
        @return dictionary containing the node name as key and line number
            as value
        @rtype dict
        """
        return self.__stack[-1][ReturnVisitor.Returns]
    
    def visit_For(self, node):
        """
        Public method to handle a for loop.
        
        @param node reference to the for node to handle
        @type ast.For
        """
        self.__visitLoop(node)
    
    def visit_AsyncFor(self, node):
        """
        Public method to handle an async for loop.
        
        @param node reference to the async for node to handle
        @type ast.AsyncFor
        """
        self.__visitLoop(node)
    
    def visit_While(self, node):
        """
        Public method to handle a while loop.
        
        @param node reference to the while node to handle
        @type ast.While
        """
        self.__visitLoop(node)
    
    def __visitLoop(self, node):
        """
        Private method to handle loop nodes.
        
        @param node reference to the loop node to handle
        @type ast.For, ast.AsyncFor or ast.While
        """
        self.__loopCount += 1
        self.generic_visit(node)
        self.__loopCount -= 1
    
    def __visitWithStack(self, node):
        """
        Private method to traverse a given function node using a stack.
        
        @param node AST node to be traversed
        @type ast.FunctionDef or ast.AsyncFunctionDef
        """
        self.__stack.append({
            ReturnVisitor.Assigns: defaultdict(list),
            ReturnVisitor.Refs: defaultdict(list),
            ReturnVisitor.Returns: []
        })
        
        self.generic_visit(node)
        self.__checkFunction(node)
        self.__stack.pop()
    
    def visit_FunctionDef(self, node):
        """
        Public method to handle a function definition.
        
        @param node reference to the node to handle
        @type ast.FunctionDef
        """
        self.__visitWithStack(node)
    
    def visit_AsyncFunctionDef(self, node):
        """
        Public method to handle a function definition.
        
        @param node reference to the node to handle
        @type ast.AsyncFunctionDef
        """
        self.__visitWithStack(node)
    
    def visit_Return(self, node):
        """
        Public method to handle a return node.
        
        @param node reference to the node to handle
        @type ast.Return
        """
        self.returns.append(node)
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        """
        Public method to handle an assign node.
        
        @param node reference to the node to handle
        @type ast.Assign
        """
        if not self.__stack:
            return

        self.generic_visit(node.value)
        
        target = node.targets[0]
        if (
            isinstance(target, ast.Tuple) and
            not isinstance(node.value, ast.Tuple)
        ):
            # skip unpacking assign
            return
        
        self.__visitAssignTarget(target)
    
    def visit_Name(self, node):
        """
        Public method to handle a name node.
        
        @param node reference to the node to handle
        @type ast.Name
        """
        if self.__stack:
            self.refs[node.id].append(node.lineno)
    
    def __visitAssignTarget(self, node):
        """
        Private method to handle an assign target node.
        
        @param node reference to the node to handle
        @type ast.AST
        """
        if isinstance(node, ast.Tuple):
            for elt in node.elts:
                self.__visitAssignTarget(elt)
            return
        
        if not self.__loopCount and isinstance(node, ast.Name):
            self.assigns[node.id].append(node.lineno)
            return
        
        self.generic_visit(node)
    
    def __checkFunction(self, node):
        """
        Private method to check a function definition node.
        
        @param node reference to the node to check
        @type ast.AsyncFunctionDef or ast.FunctionDef
        """
        if not self.returns or not node.body:
            return
        
        if len(node.body) == 1 and isinstance(node.body[-1], ast.Return):
            # skip functions that consist of `return None` only
            return
        
        if not self.__resultExists():
            self.__checkUnnecessaryReturnNone()
            return
        
        self.__checkImplicitReturnValue()
        self.__checkImplicitReturn(node.body[-1])
        
        for n in self.returns:
            if n.value:
                self.__checkUnnecessaryAssign(n.value)
    
    def __isNone(self, node):
        """
        Private method to check, if a node value is None.
        
        @param node reference to the node to check
        @type ast.AST
        @return flag indicating the node contains a None value
        @rtype bool
        """
        return (
            AstUtilities.isNameConstant(node) and
            AstUtilities.getValue(node) is None
        )
    
    def __isFalse(self, node):
        """
        Private method to check, if a node value is False.
        
        @param node reference to the node to check
        @type ast.AST
        @return flag indicating the node contains a False value
        @rtype bool
        """
        return (
            AstUtilities.isNameConstant(node) and
            AstUtilities.getValue(node) is False
        )
    
    def __resultExists(self):
        """
        Private method to check the existance of a return result.
        
        @return flag indicating the existence of a return result
        @rtype bool
        """
        for node in self.returns:
            value = node.value
            if value and not self.__isNone(value):
                return True
        
        return False
    
    def __checkImplicitReturnValue(self):
        """
        Private method to check for implicit return values.
        """
        for node in self.returns:
            if not node.value:
                self.violations.append((node, "M832"))
    
    def __checkUnnecessaryReturnNone(self):
        """
        Private method to check for an unnecessary 'return None' statement.
        """
        for node in self.returns:
            if self.__isNone(node.value):
                self.violations.append((node, "M831"))
    
    def __checkImplicitReturn(self, node):
        """
        Private method to check for an implicit return statement.
        
        @param node reference to the node to check
        @type ast.AST
        """
        if isinstance(node, ast.If):
            if not node.body or not node.orelse:
                self.violations.append((node, "M833"))
                return
            
            self.__checkImplicitReturn(node.body[-1])
            self.__checkImplicitReturn(node.orelse[-1])
            return
        
        if isinstance(node, (ast.For, ast.AsyncFor)) and node.orelse:
            self.__checkImplicitReturn(node.orelse[-1])
            return
        
        if isinstance(node, (ast.With, ast.AsyncWith)):
            self.__checkImplicitReturn(node.body[-1])
            return
        
        if isinstance(node, ast.Assert) and self.__isFalse(node.test):
            return
        
        try:
            okNodes = (ast.Return, ast.Raise, ast.While, ast.Try)
        except AttributeError:
            okNodes = (ast.Return, ast.Raise, ast.While)
        if not isinstance(node, okNodes):
            self.violations.append((node, "M833"))
    
    def __checkUnnecessaryAssign(self, node):
        """
        Private method to check for an unnecessary assign statement.
        
        @param node reference to the node to check
        @type ast.AST
        """
        if not isinstance(node, ast.Name):
            return
        
        varname = node.id
        returnLineno = node.lineno
        
        if varname not in self.assigns:
            return
        
        if varname not in self.refs:
            self.violations.append((node, "M834"))
            return
        
        if self.__hasRefsBeforeNextAssign(varname, returnLineno):
            return
        
        self.violations.append((node, "M834"))

    def __hasRefsBeforeNextAssign(self, varname, returnLineno):
        """
        Private method to check for references before a following assign
        statement.
        
        @param varname variable name to check for
        @type str
        @param returnLineno line number of the return statement
        @type int
        @return flag indicating the existence of references
        @rtype bool
        """
        beforeAssign = 0
        afterAssign = None
        
        for lineno in sorted(self.assigns[varname]):
            if lineno > returnLineno:
                afterAssign = lineno
                break
            
            if lineno <= returnLineno:
                beforeAssign = lineno
        
        for lineno in self.refs[varname]:
            if lineno == returnLineno:
                continue
            
            if afterAssign:
                if beforeAssign < lineno <= afterAssign:
                    return True
            
            elif beforeAssign < lineno:
                return True
        
        return False


class DateTimeVisitor(ast.NodeVisitor):
    """
    Class implementing a node visitor to check datetime function calls.
    
    Note: This class is modelled after flake8_datetimez checker.
    """
    def __init__(self):
        """
        Constructor
        """
        super(DateTimeVisitor, self).__init__()
        
        self.violations = []
    
    def __getFromKeywords(self, keywords, name):
        """
        Private method to get a keyword node given its name.
        
        @param keywords list of keyword argument nodes
        @type list of ast.AST
        @param name name of the keyword node
        @type str
        @return keyword node
        @rtype ast.AST
        """
        for keyword in keywords:
            if keyword.arg == name:
                return keyword
        
        return None
    
    def visit_Call(self, node):
        """
        Public method to handle a function call.

        Every datetime related function call is check for use of the naive
        variant (i.e. use without TZ info).
        
        @param node reference to the node to be processed
        @type ast.Call
        """
        # datetime.something()
        isDateTimeClass = (
            isinstance(node.func, ast.Attribute) and
            isinstance(node.func.value, ast.Name) and
            node.func.value.id == 'datetime')
        
        # datetime.datetime.something()
        isDateTimeModuleAndClass = (
            isinstance(node.func, ast.Attribute) and
            isinstance(node.func.value, ast.Attribute) and
            node.func.value.attr == 'datetime' and
            isinstance(node.func.value.value, ast.Name) and
            node.func.value.value.id == 'datetime')
        
        if isDateTimeClass:
            if node.func.attr == 'datetime':
                # datetime.datetime(2000, 1, 1, 0, 0, 0, 0,
                #                   datetime.timezone.utc)
                isCase1 = (
                    len(node.args) >= 8 and
                    not (
                        AstUtilities.isNameConstant(node.args[7]) and
                        AstUtilities.getValue(node.args[7]) is None
                    )
                )
                
                # datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)
                tzinfoKeyword = self.__getFromKeywords(node.keywords, 'tzinfo')
                isCase2 = (
                    tzinfoKeyword is not None and
                    not (
                        AstUtilities.isNameConstant(tzinfoKeyword.value) and
                        AstUtilities.getValue(tzinfoKeyword.value) is None
                    )
                )
                
                if not (isCase1 or isCase2):
                    self.violations.append((node, "M301"))
            
            elif node.func.attr == 'time':
                # time(12, 10, 45, 0, datetime.timezone.utc)
                isCase1 = (
                    len(node.args) >= 5 and
                    not (
                        AstUtilities.isNameConstant(node.args[4]) and
                        AstUtilities.getValue(node.args[4]) is None
                    )
                )
                
                # datetime.time(12, 10, 45, tzinfo=datetime.timezone.utc)
                tzinfoKeyword = self.__getFromKeywords(node.keywords, 'tzinfo')
                isCase2 = (
                    tzinfoKeyword is not None and
                    not (
                        AstUtilities.isNameConstant(tzinfoKeyword.value) and
                        AstUtilities.getValue(tzinfoKeyword.value) is None
                    )
                )
                
                if not (isCase1 or isCase2):
                    self.violations.append((node, "M321"))
            
            elif node.func.attr == 'date':
                self.violations.append((node, "M311"))
        
        if isDateTimeClass or isDateTimeModuleAndClass:
            if node.func.attr == 'today':
                self.violations.append((node, "M302"))
            
            elif node.func.attr == 'utcnow':
                self.violations.append((node, "M303"))
            
            elif node.func.attr == 'utcfromtimestamp':
                self.violations.append((node, "M304"))
            
            elif node.func.attr in 'now':
                # datetime.now(UTC)
                isCase1 = (
                    len(node.args) == 1 and
                    len(node.keywords) == 0 and
                    not (
                        AstUtilities.isNameConstant(node.args[0]) and
                        AstUtilities.getValue(node.args[0]) is None
                    )
                )
                
                # datetime.now(tz=UTC)
                tzKeyword = self.__getFromKeywords(node.keywords, 'tz')
                isCase2 = (
                    tzKeyword is not None and
                    not (
                        AstUtilities.isNameConstant(tzKeyword.value) and
                        AstUtilities.getValue(tzKeyword.value) is None
                    )
                )
                
                if not (isCase1 or isCase2):
                    self.violations.append((node, "M305"))
            
            elif node.func.attr == 'fromtimestamp':
                # datetime.fromtimestamp(1234, UTC)
                isCase1 = (
                    len(node.args) == 2 and
                    len(node.keywords) == 0 and
                    not (
                        AstUtilities.isNameConstant(node.args[1]) and
                        AstUtilities.getValue(node.args[1]) is None
                    )
                )
                
                # datetime.fromtimestamp(1234, tz=UTC)
                tzKeyword = self.__getFromKeywords(node.keywords, 'tz')
                isCase2 = (
                    tzKeyword is not None and
                    not (
                        AstUtilities.isNameConstant(tzKeyword.value) and
                        AstUtilities.getValue(tzKeyword.value) is None
                    )
                )
                
                if not (isCase1 or isCase2):
                    self.violations.append((node, "M306"))
            
            elif node.func.attr == 'strptime':
                # datetime.strptime(...).replace(tzinfo=UTC)
                parent = getattr(node, '_dtCheckerParent', None)
                pparent = getattr(parent, '_dtCheckerParent', None)
                if not (isinstance(parent, ast.Attribute) and
                        parent.attr == 'replace'):
                    isCase1 = False
                elif not isinstance(pparent, ast.Call):
                    isCase1 = False
                else:
                    tzinfoKeyword = self.__getFromKeywords(pparent.keywords,
                                                           'tzinfo')
                    isCase1 = (
                        tzinfoKeyword is not None and
                        not (
                            AstUtilities.isNameConstant(
                                tzinfoKeyword.value) and
                            AstUtilities.getValue(tzinfoKeyword.value) is None
                        )
                    )
                
                if not isCase1:
                    self.violations.append((node, "M307"))
            
            elif node.func.attr == 'fromordinal':
                self.violations.append((node, "M308"))
        
        # date.something()
        isDateClass = (isinstance(node.func, ast.Attribute) and
                       isinstance(node.func.value, ast.Name) and
                       node.func.value.id == 'date')
        
        # datetime.date.something()
        isDateModuleAndClass = (isinstance(node.func, ast.Attribute) and
                                isinstance(node.func.value, ast.Attribute) and
                                node.func.value.attr == 'date' and
                                isinstance(node.func.value.value, ast.Name) and
                                node.func.value.value.id == 'datetime')
        
        if isDateClass or isDateModuleAndClass:
            if node.func.attr == 'today':
                self.violations.append((node, "M312"))
            
            elif node.func.attr == 'fromtimestamp':
                self.violations.append((node, "M313"))
            
            elif node.func.attr == 'fromordinal':
                self.violations.append((node, "M314"))
            
            elif node.func.attr == 'fromisoformat':
                self.violations.append((node, "M315"))
        
        self.generic_visit(node)


class SysVersionVisitor(ast.NodeVisitor):
    """
    Class implementing a node visitor to check the use of sys.version and
    sys.version_info.
    
    Note: This class is modelled after flake8-2020 checker.
    """
    def __init__(self):
        """
        Constructor
        """
        super(SysVersionVisitor, self).__init__()
        
        self.violations = []
        self.__fromImports = {}
    
    def visit_ImportFrom(self, node):
        """
        Public method to handle a from ... import ... statement.
        
        @param node reference to the node to be processed
        @type ast.ImportFrom
        """
        for alias in node.names:
            if node.module is not None and not alias.asname:
                self.__fromImports[alias.name] = node.module
        
        self.generic_visit(node)
    
    def __isSys(self, attr, node):
        """
        Private method to check for a reference to sys attribute.
        
        @param attr attribute name
        @type str
        @param node reference to the node to be checked
        @type ast.Node
        @return flag indicating a match
        @rtype bool
        """
        match = False
        if (
            isinstance(node, ast.Attribute) and
            isinstance(node.value, ast.Name) and
            node.value.id == "sys" and
            node.attr == attr
        ):
            match = True
        elif (
            isinstance(node, ast.Name) and
            node.id == attr and
            self.__fromImports.get(node.id) == "sys"
        ):
            match = True
        
        return match
    
    def __isSysVersionUpperSlice(self, node, n):
        """
        Private method to check the upper slice of sys.version.
        
        @param node reference to the node to be checked
        @type ast.Node
        @param n slice value to check against
        @type int
        @return flag indicating a match
        @rtype bool
        """
        return (
            self.__isSys("version", node.value) and
            isinstance(node.slice, ast.Slice) and
            node.slice.lower is None and
            AstUtilities.isNumber(node.slice.upper) and
            AstUtilities.getValue(node.slice.upper) == n and
            node.slice.step is None
        )
    
    def visit_Subscript(self, node):
        """
        Public method to handle a subscript.
        
        @param node reference to the node to be processed
        @type ast.Subscript
        """
        if self.__isSysVersionUpperSlice(node, 1):
            self.violations.append((node.value, "M423"))
        elif self.__isSysVersionUpperSlice(node, 3):
            self.violations.append((node.value, "M401"))
        elif (
            self.__isSys('version', node.value) and
            isinstance(node.slice, ast.Index) and
            AstUtilities.isNumber(node.slice.value) and
            AstUtilities.getValue(node.slice.value) == 2
        ):
            self.violations.append((node.value, "M402"))
        elif (
            self.__isSys('version', node.value) and
            isinstance(node.slice, ast.Index) and
            AstUtilities.isNumber(node.slice.value) and
            AstUtilities.getValue(node.slice.value) == 0
        ):
            self.violations.append((node.value, "M421"))

        self.generic_visit(node)
    
    def visit_Compare(self, node):
        """
        Public method to handle a comparison.
        
        @param node reference to the node to be processed
        @type ast.Compare
        """
        if (
            isinstance(node.left, ast.Subscript) and
            self.__isSys('version_info', node.left.value) and
            isinstance(node.left.slice, ast.Index) and
            AstUtilities.isNumber(node.left.slice.value) and
            AstUtilities.getValue(node.left.slice.value) == 0 and
            len(node.ops) == 1 and
            isinstance(node.ops[0], ast.Eq) and
            AstUtilities.isNumber(node.comparators[0]) and
            AstUtilities.getValue(node.comparators[0]) == 3
        ):
            self.violations.append((node.left, "M411"))
        elif (
            self.__isSys('version', node.left) and
            len(node.ops) == 1 and
            isinstance(node.ops[0], (ast.Lt, ast.LtE, ast.Gt, ast.GtE)) and
            AstUtilities.isString(node.comparators[0])
        ):
            if len(AstUtilities.getValue(node.comparators[0])) == 1:
                errorCode = "M422"
            else:
                errorCode = "M403"
            self.violations.append((node.left, errorCode))
        elif (
            isinstance(node.left, ast.Subscript) and
            self.__isSys('version_info', node.left.value) and
            isinstance(node.left.slice, ast.Index) and
            AstUtilities.isNumber(node.left.slice.value) and
            AstUtilities.getValue(node.left.slice.value) == 1 and
            len(node.ops) == 1 and
            isinstance(node.ops[0], (ast.Lt, ast.LtE, ast.Gt, ast.GtE)) and
            AstUtilities.isNumber(node.comparators[0])
        ):
            self.violations.append((node, "M413"))
        elif (
            isinstance(node.left, ast.Attribute) and
            self.__isSys('version_info', node.left.value) and
            node.left.attr == 'minor' and
            len(node.ops) == 1 and
            isinstance(node.ops[0], (ast.Lt, ast.LtE, ast.Gt, ast.GtE)) and
            AstUtilities.isNumber(node.comparators[0])
        ):
            self.violations.append((node, "M414"))
        
        self.generic_visit(node)
    
    def visit_Attribute(self, node):
        """
        Public method to handle an attribute.
        
        @param node reference to the node to be processed
        @type ast.Attribute
        """
        if (
            isinstance(node.value, ast.Name) and
            node.value.id == 'six' and
            node.attr == 'PY3'
        ):
            self.violations.append((node, "M412"))
        
        self.generic_visit(node)

    def visit_Name(self, node):
        """
        Public method to handle an name.
        
        @param node reference to the node to be processed
        @type ast.Name
        """
        if node.id == 'PY3' and self.__fromImports.get(node.id) == 'six':
            self.violations.append((node, "M412"))
        
        self.generic_visit(node)

#
# eflag: noqa = M891
