# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a context manager locking and unlocking a mutex.
"""

import contextlib


class E5MutexLocker(contextlib.AbstractContextManager):
    """
    Class implementing a context manager locking and unlocking a mutex.
    """
    def __init__(self, mutex):
        """
        Constructor
        
        @param mutex reference to the mutex to be locked
        @type QMutex or QRecursiveMutex
        """
        self.__mutex = mutex
    
    def __enter__(self):
        """
        Special method called when entering the runtime ccontext.
        
        @return reference to the context manager object
        @rtype E5OverrideCursor
        """
        self.__mutex.lock()
        
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Special method called when exiting the runtime ccontext.
        
        @param exc_type type of an exception raised in the runtime context
        @param exc_value value of an exception raised in the runtime context
        @param traceback traceback of an exception raised in the runtime
            context
        @return always returns None to not suppress any exception
        @rtype None
        """
        self.__mutex.unlock()
        
        return None     # __IGNORE_WARNING_M831__
