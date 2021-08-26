# -*- coding: utf-8 -*-

# Copyright (c) 2011 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the code style checker.
"""

import queue
import ast
import sys
import multiprocessing

import pycodestyle
from Naming.NamingStyleChecker import NamingStyleChecker

# register the name checker
pycodestyle.register_check(NamingStyleChecker, NamingStyleChecker.Codes)

from DocStyle.DocStyleChecker import DocStyleChecker
from Miscellaneous.MiscellaneousChecker import MiscellaneousChecker
from Complexity.ComplexityChecker import ComplexityChecker
from Security.SecurityChecker import SecurityChecker
from PathLib.PathlibChecker import PathlibChecker


def initService():
    """
    Initialize the service and return the entry point.
    
    @return the entry point for the background client (function)
    """
    return codeStyleCheck


def initBatchService():
    """
    Initialize the batch service and return the entry point.
    
    @return the entry point for the background client (function)
    """
    return codeStyleBatchCheck


class CodeStyleCheckerReport(pycodestyle.BaseReport):
    """
    Class implementing a special report to be used with our dialog.
    """
    def __init__(self, options):
        """
        Constructor
        
        @param options options for the report (optparse.Values)
        """
        super(CodeStyleCheckerReport, self).__init__(options)
        
        self.__repeat = options.repeat
        self.errors = []
    
    def error_args(self, line_number, offset, code, check, *args):
        """
        Public method to collect the error messages.
        
        @param line_number line number of the issue (integer)
        @param offset position within line of the issue (integer)
        @param code message code (string)
        @param check reference to the checker function (function)
        @param args arguments for the message (list)
        @return error code (string)
        """
        code = super(CodeStyleCheckerReport, self).error_args(
            line_number, offset, code, check, *args)
        if code and (self.counters[code] == 1 or self.__repeat):
            self.errors.append(
                {
                    "file": self.filename,
                    "line": line_number,
                    "offset": offset,
                    "code": code,
                    "args": args,
                }
            )
        return code


def extractLineFlags(line, startComment="#", endComment="", flagsLine=False):
    """
    Function to extract flags starting and ending with '__' from a line
    comment.
    
    @param line line to extract flags from (string)
    @param startComment string identifying the start of the comment (string)
    @param endComment string identifying the end of a comment (string)
    @param flagsLine flag indicating to check for a flags only line (bool)
    @return list containing the extracted flags (list of strings)
    """
    flags = []
    
    if not flagsLine or (
       flagsLine and line.strip().startswith(startComment)):
        pos = line.rfind(startComment)
        if pos >= 0:
            comment = line[pos + len(startComment):].strip()
            if endComment:
                endPos = line.rfind(endComment)
                if endPos >= 0:
                    comment = comment[:endPos]
            flags = [f.strip() for f in comment.split()
                     if (f.startswith("__") and f.endswith("__"))]
            flags += [f.strip().lower() for f in comment.split()
                      if f in ("noqa", "NOQA",
                               "nosec", "NOSEC",
                               "secok", "SECOK")]
    return flags


def ignoreCode(code, lineFlags):
    """
    Function to check, if the given code should be ignored as per line flags.
    
    @param code error code to be checked
    @type str
    @param lineFlags list of line flags to check against
    @type list of str
    @return flag indicating to ignore the code
    @rtype bool
    """
    if lineFlags:
        
        if (
            "__IGNORE_WARNING__" in lineFlags or
            "noqa" in lineFlags or
            "nosec" in lineFlags
        ):
            # ignore all warning codes
            return True
        
        for flag in lineFlags:
            # check individual warning code
            if flag.startswith("__IGNORE_WARNING_"):
                ignoredCode = flag[2:-2].rsplit("_", 1)[-1]
                if code.startswith(ignoredCode):
                    return True
    
    return False


def securityOk(code, lineFlags):
    """
    Function to check, if the given code is an acknowledged security report.
    
    @param code error code to be checked
    @type str
    @param lineFlags list of line flags to check against
    @type list of str
    @return flag indicating an acknowledged security report
    @rtype bool
    """
    if lineFlags:
        return "secok" in lineFlags
    
    return False


def codeStyleCheck(filename, source, args):
    """
    Do the code style check and/or fix found errors.
    
    @param filename source filename
    @type str
    @param source string containing the code to check
    @type str
    @param args arguments used by the codeStyleCheck function (list of
        excludeMessages, includeMessages, repeatMessages, fixCodes,
        noFixCodes, fixIssues, maxLineLength, maxDocLineLength, blankLines,
        hangClosing, docType, codeComplexityArgs, miscellaneousArgs, errors,
        eol, encoding, backup)
    @type list of (str, str, bool, str, str, bool, int, list of (int, int),
        bool, str, dict, dict, list of str, str, str, bool)
    @return tuple of statistics (dict) and list of results (tuple for each
        found violation of style (lineno, position, text, ignored, fixed,
        autofixing, fixedMsg))
    @rtype tuple of (dict, list of tuples of (int, int, str, bool, bool, bool,
        str))
    """
    return __checkCodeStyle(filename, source, args)


def codeStyleBatchCheck(argumentsList, send, fx, cancelled, maxProcesses=0):
    """
    Module function to check code style for a batch of files.
    
    @param argumentsList list of arguments tuples as given for codeStyleCheck
    @type list
    @param send reference to send function
    @type func
    @param fx registered service name
    @type str
    @param cancelled reference to function checking for a cancellation
    @type func
    @param maxProcesses number of processes to be used
    @type int
    """
    if maxProcesses == 0:
        # determine based on CPU count
        try:
            NumberOfProcesses = multiprocessing.cpu_count()
            if NumberOfProcesses >= 1:
                NumberOfProcesses -= 1
        except NotImplementedError:
            NumberOfProcesses = 1
    else:
        NumberOfProcesses = maxProcesses

    # Create queues
    taskQueue = multiprocessing.Queue()
    doneQueue = multiprocessing.Queue()

    # Submit tasks (initially two time number of processes
    initialTasks = 2 * NumberOfProcesses
    for task in argumentsList[:initialTasks]:
        taskQueue.put(task)

    # Start worker processes
    for _ in range(NumberOfProcesses):
        multiprocessing.Process(
            target=worker, args=(taskQueue, doneQueue)
        ).start()

    # Get and send results
    endIndex = len(argumentsList) - initialTasks
    for i in range(len(argumentsList)):
        resultSent = False
        wasCancelled = False
        
        while not resultSent:
            try:
                # get result (waiting max. 3 seconds and send it to frontend
                filename, result = doneQueue.get(timeout=3)
                send(fx, filename, result)
                resultSent = True
            except queue.Empty:
                # ignore empty queue, just carry on
                if cancelled():
                    wasCancelled = True
                    break
        
        if wasCancelled or cancelled():
            # just exit the loop ignoring the results of queued tasks
            break
        
        if i < endIndex:
            taskQueue.put(argumentsList[i + initialTasks])

    # Tell child processes to stop
    for _ in range(NumberOfProcesses):
        taskQueue.put('STOP')


def worker(inputQueue, outputQueue):
    """
    Module function acting as the parallel worker for the style check.
    
    @param inputQueue input queue (multiprocessing.Queue)
    @param outputQueue output queue (multiprocessing.Queue)
    """
    for filename, source, args in iter(inputQueue.get, 'STOP'):
        result = __checkCodeStyle(filename, source, args)
        outputQueue.put((filename, result))


def __checkSyntax(filename, source):
    """
    Private module function to perform a syntax check.
    
    @param filename source filename
    @type str
    @param source string containing the code to check
    @type str
    @return tuple containing the error dictionary with syntax error details
        and a statistics dictionary or a tuple containing two None
    @rtype tuple of (dict, dict) or tuple of (None, None)
    """
    src = "".join(source)
    
    try:
        ast.parse(src, filename, 'exec')
        return None, None
    except (SyntaxError, TypeError):
        exc_type, exc = sys.exc_info()[:2]
        if len(exc.args) > 1:
            offset = exc.args[1]
            if len(offset) > 2:
                offset = offset[1:3]
        else:
            offset = (1, 0)
        return ({
            "file": filename,
            "line": offset[0],
            "offset": offset[1],
            "code": "E901",
            "args": [exc_type.__name__, exc.args[0]],
        }, {
            "E901": 1,
        })


def __checkCodeStyle(filename, source, args):
    """
    Private module function to perform the code style check and/or fix
    found errors.
    
    @param filename source filename
    @type str
    @param source string containing the code to check
    @type str
    @param args arguments used by the codeStyleCheck function (list of
        excludeMessages, includeMessages, repeatMessages, fixCodes,
        noFixCodes, fixIssues, maxLineLength, maxDocLineLength, blankLines,
        hangClosing, docType, codeComplexityArgs, miscellaneousArgs,
        annotationArgs, securityArgs, errors, eol, encoding, backup)
    @type list of (str, str, bool, str, str, bool, int, list of (int, int),
        bool, str, dict, dict, dict, list of str, str, str, bool)
    @return tuple of statistics data and list of result dictionaries with
        keys:
        <ul>
        <li>file: file name</li>
        <li>line: line_number</li>
        <li>offset: offset within line</li>
        <li>code: message code</li>
        <li>args: list of arguments to format the message</li>
        <li>ignored: flag indicating this issue was ignored</li>
        <li>fixed: flag indicating this issue was fixed</li>
        <li>autofixing: flag indicating that a fix can be done</li>
        <li>fixcode: message code for the fix</li>
        <li>fixargs: list of arguments to format the fix message</li>
        </ul>
    @rtype tuple of (dict, list of dict)
    """
    (excludeMessages, includeMessages, repeatMessages, fixCodes, noFixCodes,
     fixIssues, maxLineLength, maxDocLineLength, blankLines, hangClosing,
     docType, codeComplexityArgs, miscellaneousArgs, annotationArgs,
     securityArgs, errors, eol, encoding, backup) = args
    
    stats = {}

    if fixIssues:
        from CodeStyleFixer import CodeStyleFixer
        fixer = CodeStyleFixer(
            filename, source, fixCodes, noFixCodes,
            maxLineLength, blankLines, True, eol, backup)
        # always fix in place
    else:
        fixer = None
    
    if not errors:
        if includeMessages:
            select = [s.strip() for s in
                      includeMessages.split(',') if s.strip()]
        else:
            select = []
        if excludeMessages:
            ignore = [i.strip() for i in
                      excludeMessages.split(',') if i.strip()]
        else:
            ignore = []
        
        syntaxError, syntaxStats = __checkSyntax(filename, source)
        if syntaxError:
            errors = [syntaxError]
            stats.update(syntaxStats)
        
        # perform the checks only, if syntax is ok
        else:
            # check coding style
            pycodestyle.BLANK_LINES_CONFIG = {
                # Top level class and function.
                'top_level': blankLines[0],
                # Methods and nested class and function.
                'method': blankLines[1],
            }
            styleGuide = pycodestyle.StyleGuide(
                reporter=CodeStyleCheckerReport,
                repeat=repeatMessages,
                select=select,
                ignore=ignore,
                max_line_length=maxLineLength,
                max_doc_length=maxDocLineLength,
                hang_closing=hangClosing,
            )
            report = styleGuide.check_files([filename])
            stats.update(report.counters)
            errors = report.errors
            
            # check documentation style
            docStyleChecker = DocStyleChecker(
                source, filename, select, ignore, [], repeatMessages,
                maxLineLength=maxDocLineLength, docType=docType)
            docStyleChecker.run()
            stats.update(docStyleChecker.counters)
            errors += docStyleChecker.errors
            
            # miscellaneous additional checks
            miscellaneousChecker = MiscellaneousChecker(
                source, filename, select, ignore, [], repeatMessages,
                miscellaneousArgs)
            miscellaneousChecker.run()
            stats.update(miscellaneousChecker.counters)
            errors += miscellaneousChecker.errors
            
            # check code complexity
            complexityChecker = ComplexityChecker(
                source, filename, select, ignore, codeComplexityArgs)
            complexityChecker.run()
            stats.update(complexityChecker.counters)
            errors += complexityChecker.errors
            
            # check function annotations
            if sys.version_info >= (3, 5, 0):
                # annotations are supported from Python 3.5 on
                from Annotations.AnnotationsChecker import AnnotationsChecker
                annotationsChecker = AnnotationsChecker(
                    source, filename, select, ignore, [], repeatMessages,
                    annotationArgs)
                annotationsChecker.run()
                stats.update(annotationsChecker.counters)
                errors += annotationsChecker.errors
            
            securityChecker = SecurityChecker(
                source, filename, select, ignore, [], repeatMessages,
                securityArgs)
            securityChecker.run()
            stats.update(securityChecker.counters)
            errors += securityChecker.errors
            
            pathlibChecker = PathlibChecker(
                source, filename, select, ignore, [], repeatMessages)
            pathlibChecker.run()
            stats.update(pathlibChecker.counters)
            errors += pathlibChecker.errors
    
    errorsDict = {}
    for error in errors:
        if error["line"] > len(source):
            error["line"] = len(source)
        # inverse processing of messages and fixes
        errorLine = errorsDict.setdefault(error["line"], [])
        errorLine.append((error["offset"], error))
    deferredFixes = {}
    results = []
    for lineno, errorsList in errorsDict.items():
        errorsList.sort(key=lambda x: x[0], reverse=True)
        for _, error in errorsList:
            error.update({
                "ignored": False,
                "fixed": False,
                "autofixing": False,
                "fixcode": "",
                "fixargs": [],
                "securityOk": False,
            })
            
            if source:
                code = error["code"]
                lineFlags = extractLineFlags(source[lineno - 1].strip())
                try:
                    lineFlags += extractLineFlags(source[lineno].strip(),
                                                  flagsLine=True)
                except IndexError:
                    pass
                
                if securityOk(code, lineFlags):
                    error["securityOk"] = True
                
                if ignoreCode(code, lineFlags):
                    error["ignored"] = True
                else:
                    if fixer:
                        res, fixcode, fixargs, id_ = fixer.fixIssue(
                            lineno, error["offset"], code)
                        if res == -1:
                            deferredFixes[id_] = error
                        else:
                            error.update({
                                "fixed": res == 1,
                                "autofixing": True,
                                "fixcode": fixcode,
                                "fixargs": fixargs,
                            })
            
            results.append(error)
    
    if fixer:
        deferredResults = fixer.finalize()
        for id_ in deferredResults:
            fixed, fixcode, fixargs = deferredResults[id_]
            error = deferredFixes[id_]
            error.update({
                "ignored": False,
                "fixed": fixed == 1,
                "autofixing": True,
                "fixcode": fixcode,
                "fixargs": fixargs,
            })

        saveError = fixer.saveFile(encoding)
        if saveError:
            for error in results:
                error.update({
                    "fixcode": saveError[0],
                    "fixargs": saveError[1],
                })

    return stats, results
