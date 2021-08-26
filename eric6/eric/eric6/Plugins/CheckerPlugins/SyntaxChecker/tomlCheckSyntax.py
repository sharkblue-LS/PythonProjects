# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the syntax check for TOML.
"""

import queue
import multiprocessing


def initService():
    """
    Initialize the service and return the entry point.
    
    @return the entry point for the background client
    @rtype func
    """
    return tomlSyntaxCheck


def initBatchService():
    """
    Initialize the batch service and return the entry point.
    
    @return the entry point for the background client
    @rtype func
    """
    return tomlSyntaxBatchCheck


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


def tomlSyntaxCheck(file, codestring):
    """
    Function to check a TOML source file for syntax errors.
    
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
    return __tomlSyntaxCheck(file, codestring)


def tomlSyntaxBatchCheck(argumentsList, send, fx, cancelled, maxProcesses=0):
    """
    Module function to check syntax for a batch of files.
    
    @param argumentsList list of arguments tuples as given for tomlSyntaxCheck
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
        result = __tomlSyntaxCheck(filename, source)
        outputQueue.put((filename, result))


def __tomlSyntaxCheck(file, codestring):
    """
    Function to check a TOML source file for syntax errors.
    
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
        import toml
    except ImportError:
        error = "toml not available. Install it via the PyPI interface."
        return [{'error': (file, 0, 0, '', error)}]
    
    codestring = normalizeCode(codestring)
    
    try:
        toml.loads(codestring)
    except toml.TomlDecodeError as exc:
        line = exc.lineno
        column = exc.colno
        error = exc.msg
        
        cline = min(len(codestring.splitlines()), int(line)) - 1
        code = codestring.splitlines()[cline]
        
        return [{'error': (file, line, column, code, error)}]
    
    return [{}]
