# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the syntax check for YAML.
"""

import queue
import multiprocessing


def initService():
    """
    Initialize the service and return the entry point.
    
    @return the entry point for the background client
    @rtype func
    """
    return yamlSyntaxCheck


def initBatchService():
    """
    Initialize the batch service and return the entry point.
    
    @return the entry point for the background client
    @rtype func
    """
    return yamlSyntaxBatchCheck


def normalizeCode(codestring):
    """
    Function to normalize the given code.
    
    @param codestring code to be normalized
    @type str
    @return normalized code
    @rtype str
    """
    codestring = codestring.replace("\r\n", "\n").replace("\r", "\n")

    if codestring and codestring[-1] != '\n':
        codestring = codestring + '\n'
    
    return codestring


def yamlSyntaxCheck(file, codestring):
    """
    Function to check a YAML source file for syntax errors.
    
    @param file source filename
    @type str
    @param codestring string containing the code to check
    @type str
    @return dictionary with the keys 'error' and 'warnings' which
            hold a list containing details about the error/ warnings
            (file name, line number, column, codestring (only at syntax
            errors), the message, a list with arguments for the message)
    @rtype dict
    """
    return __yamlSyntaxCheck(file, codestring)


def yamlSyntaxBatchCheck(argumentsList, send, fx, cancelled, maxProcesses=0):
    """
    Module function to check syntax for a batch of files.
    
    @param argumentsList list of arguments tuples as given for yamlSyntaxCheck
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
                filename, result = doneQueue.get()
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
    Module function acting as the parallel worker for the syntax check.
    
    @param inputQueue input queue
    @type multiprocessing.Queue
    @param outputQueue output queue
    @type multiprocessing.Queue
    """
    for filename, args in iter(inputQueue.get, 'STOP'):
        source = args[0]
        result = __yamlSyntaxCheck(filename, source)
        outputQueue.put((filename, result))


def __yamlSyntaxCheck(file, codestring):
    """
    Function to check a YAML source file for syntax errors.
    
    @param file source filename
    @type str
    @param codestring string containing the code to check
    @type str
    @return dictionary with the keys 'error' and 'warnings' which
            hold a list containing details about the error/ warnings
            (file name, line number, column, codestring (only at syntax
            errors), the message, a list with arguments for the message)
    @rtype dict
    """
    try:
        from yaml import safe_load_all, MarkedYAMLError
    except ImportError:
        error = "pyyaml not available. Install it via the PyPI interface."
        return [{'error': (file, 0, 0, '', error)}]
    
    codestring = normalizeCode(codestring)
    
    try:
        for _obj in safe_load_all(codestring):
            # do nothing with it, just to get parse errors
            pass
    except MarkedYAMLError as exc:
        if exc.problem_mark:
            line = exc.problem_mark.line + 1
            column = exc.problem_mark.column
        else:
            line, column = 0, 0
        error = exc.problem
        
        cline = min(len(codestring.splitlines()), int(line)) - 1
        code = codestring.splitlines()[cline]
        
        return [{'error': (file, line, column, code, error)}]
    
    return [{}]
