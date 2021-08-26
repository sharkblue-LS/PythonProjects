# -*- coding: utf-8 -*-

# Copyright (c) 2016 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing classes and functions to dump variable contents.
"""

from DebugConfig import ConfigQtNames, ConfigKnownQtTypes, BatchSize

#
# This code was inspired by pydevd.
#

############################################################
## Classes implementing resolvers for various compund types
############################################################


class BaseResolver(object):
    """
    Base class of the resolver class tree.
    """
    def resolve(self, var, attribute):
        """
        Public method to get an attribute from a variable.
        
        @param var variable to extract an attribute or value from
        @type any
        @param attribute name of the attribute to extract
        @type str
        @return value of the attribute
        @rtype any
        """
        return getattr(var, attribute, None)
    
    def getDictionary(self, var):
        """
        Public method to get the attributes of a variable as a dictionary.
        
        @param var variable to be converted
        @type any
        @return dictionary containing the variable attributes
        @rtype dict
        """
        names = dir(var)
        if not names and hasattr(var, "__members__"):
            names = var.__members__
        
        d = {}
        for name in names:
            try:
                attribute = getattr(var, name)
                d[name] = attribute
            except Exception:       # secok
                pass    # if we can't get it, simply ignore it
        
        return d


############################################################
## Default Resolver
############################################################


class DefaultResolver(BaseResolver):
    """
    Class used to resolve the default way.
    """
    def getDictionary(self, var):
        """
        Public method to get the attributes of a variable as a dictionary.
        
        @param var variable to be converted
        @type any
        @yield tuple containing the batch start index and a dictionary
            containing the variable attributes
        @ytype tuple of (int, dict)
        """
        names = dir(var)
        if not names and hasattr(var, "__members__"):
            names = var.__members__
        
        d = {}
        for name in names:
            try:
                attribute = getattr(var, name)
                d[name] = attribute
            except Exception:       # secok
                pass    # if we can't get it, simply ignore it
        
        yield -1, d
        while True:
            yield -2, {}


############################################################
## Resolver for Dictionaries
############################################################


class DictResolver(BaseResolver):
    """
    Class used to resolve from a dictionary.
    """
    def resolve(self, var, attribute):
        """
        Public method to get an attribute from a variable.
        
        @param var variable to extract an attribute or value from
        @type dict
        @param attribute name of the attribute to extract
        @type str
        @return value of the attribute
        @rtype any
        """
        if " (ID:" not in attribute:
            try:
                return var[attribute]
            except Exception:
                return getattr(var, attribute, None)
        
        expectedID = int(attribute.split(" (ID:")[-1][:-1])
        for key, value in var.items():
            if id(key) == expectedID:
                return value
        
        return None
    
    def keyToStr(self, key):
        """
        Public method to get a string representation for a key.
        
        @param key key to be converted
        @type any
        @return string representation of the given key
        @rtype str
        """
        if isinstance(key, str):
            key = repr(key)
            # Special handling for bytes object
            # Raw and f-Strings are always converted to str
            if key[0] == 'b':
                key = key[1:]

        return key  # __IGNORE_WARNING_M834__
    
    def getDictionary(self, var):
        """
        Public method to get the attributes of a variable as a dictionary.
        
        @param var variable to be converted
        @type any
        @yield tuple containing the batch start index and a dictionary
            containing the variable attributes
        @ytype tuple of (int, dict)
        """
        d = {}
        start = count = 0
        allItems = list(var.items())
        try:
            # Fast path: all items from same type
            allItems.sort(key=lambda x: x[0])
        except TypeError:
            # Slow path: only sort items with same type (Py3 only)
            allItems.sort(key=lambda x: (str(x[0]), x[0]))
        
        for key, value in allItems:
            key = "{0} (ID:{1})".format(self.keyToStr(key), id(key))
            d[key] = value
            count += 1
            if count >= BatchSize:
                yield start, d
                start += count
                count = 0
                d = {}
        
        if d:
            yield start, d
        
        # in case it has additional fields
        d = super(DictResolver, self).getDictionary(var)
        yield -1, d
        
        while True:
            yield -2, {}


############################################################
## Resolver for Lists and Tuples
############################################################


class ListResolver(BaseResolver):
    """
    Class used to resolve from a tuple or list.
    """
    def resolve(self, var, attribute):
        """
        Public method to get an attribute from a variable.
        
        @param var variable to extract an attribute or value from
        @type tuple or list
        @param attribute name of the attribute to extract
        @type str
        @return value of the attribute
        @rtype any
        """
        try:
            return var[int(attribute)]
        except Exception:
            return getattr(var, attribute, None)
    
    def getDictionary(self, var):
        """
        Public method to get the attributes of a variable as a dictionary.
        
        @param var variable to be converted
        @type any
        @yield tuple containing the batch start index and a dictionary
            containing the variable attributes
        @ytype tuple of (int, dict)
        """
        d = {}
        start = count = 0
        for idx, value in enumerate(var):
            d[idx] = value
            count += 1
            if count >= BatchSize:
                yield start, d
                start = idx + 1
                count = 0
                d = {}
        
        if d:
            yield start, d
        
        # in case it has additional fields
        d = super(ListResolver, self).getDictionary(var)
        yield -1, d
        
        while True:
            yield -2, {}
    

############################################################
## Resolver for dict_items, dict_keys and dict_values
############################################################


class DictViewResolver(ListResolver):
    """
    Class used to resolve from dict views.
    """
    def resolve(self, var, attribute):
        """
        Public method to get an attribute from a variable.
        
        @param var variable to extract an attribute or value from
        @type tuple or list
        @param attribute id of the value to extract
        @type str
        @return value of the attribute
        @rtype any
        """
        return super(DictViewResolver, self).resolve(list(var), attribute)
    
    def getDictionary(self, var):
        """
        Public method to get the attributes of a variable as a dictionary.
        
        @param var variable to be converted
        @type any
        @return dictionary containing the variable attributes
        @rtype dict
        """
        return super(DictViewResolver, self).getDictionary(list(var))


############################################################
## Resolver for Sets and Frozensets
############################################################


class SetResolver(BaseResolver):
    """
    Class used to resolve from a set or frozenset.
    """
    def resolve(self, var, attribute):
        """
        Public method to get an attribute from a variable.
        
        @param var variable to extract an attribute or value from
        @type tuple or list
        @param attribute id of the value to extract
        @type str
        @return value of the attribute
        @rtype any
        """
        if attribute.startswith("'ID: "):
            attribute = attribute.split(None, 1)[1][:-1]
        try:
            attribute = int(attribute)
        except Exception:
            return getattr(var, attribute, None)

        for v in var:
            if id(v) == attribute:
                return v
        
        return None
    
    def getDictionary(self, var):
        """
        Public method to get the attributes of a variable as a dictionary.
        
        @param var variable to be converted
        @type any
        @yield tuple containing the batch start index and a dictionary
            containing the variable attributes
        @ytype tuple of (int, dict)
        """
        d = {}
        start = count = 0
        for value in var:
            count += 1
            d["'ID: {0}'".format(id(value))] = value
            if count >= BatchSize:
                yield start, d
                start += count
                count = 0
                d = {}
        
        if d:
            yield start, d
        
        # in case it has additional fields
        additionals = super(SetResolver, self).getDictionary(var)
        yield -1, additionals
        
        while True:
            yield -2, {}
    

############################################################
## Resolver for Numpy Arrays
############################################################


class NdArrayResolver(BaseResolver):
    """
    Class used to resolve from numpy ndarray including some meta data.
    """
    def __isNumeric(self, arr):
        """
        Private method to check, if an array is of a numeric type.
        
        @param arr array to check
        @type ndarray
        @return flag indicating a numeric array
        @rtype bool
        """
        try:
            return arr.dtype.kind in 'biufc'
        except AttributeError:
            return False
    
    def resolve(self, var, attribute):
        """
        Public method to get an attribute from a variable.
        
        @param var variable to extract an attribute or value from
        @type tuple or list
        @param attribute id of the value to extract
        @type str
        @return value of the attribute
        @rtype any
        """
        if attribute == 'min':
            if self.__isNumeric(var):
                return var.min()
            else:
                return None
        
        if attribute == 'max':
            if self.__isNumeric(var):
                return var.max()
            else:
                return None
        
        if attribute == 'mean':
            if self.__isNumeric(var):
                return var.mean()
            else:
                return None
        
        try:
            return var[int(attribute)]
        except Exception:
            return getattr(var, attribute, None)
        
        return None
    
    def getDictionary(self, var):
        """
        Public method to get the attributes of a variable as a dictionary.
        
        @param var variable to be converted
        @type any
        @yield tuple containing the batch start index and a dictionary
            containing the variable attributes
        @ytype tuple of (int, dict)
        """
        d = {}
        start = count = 0
        try:
            len(var)  # Check if it's an unsized object, e.g. np.ndarray(())
            allItems = var.tolist()
        except TypeError:  # TypeError: len() of unsized object
            allItems = []
        
        for idx, value in enumerate(allItems):
            d[str(idx)] = value
            count += 1
            if count >= BatchSize:
                yield start, d
                start += count
                count = 0
                d = {}
        
        if d:
            yield start, d
        
        # in case it has additional fields
        d = super(NdArrayResolver, self).getDictionary(var)
        
        if var.size > 1024 * 1024:
            d['min'] = (
                'ndarray too big, calculating min would slow down debugging')
            d['max'] = (
                'ndarray too big, calculating max would slow down debugging')
            d['mean'] = (
                'ndarray too big, calculating mean would slow down debugging')
        elif self.__isNumeric(var):
            if var.size == 0:
                d['min'] = 'empty array'
                d['max'] = 'empty array'
                d['mean'] = 'empty array'
            else:
                d['min'] = var.min()
                d['max'] = var.max()
                d['mean'] = var.mean()
        else:
            d['min'] = 'not a numeric object'
            d['max'] = 'not a numeric object'
            d['mean'] = 'not a numeric object'
        
        yield -1, d
        
        while True:
            yield -2, {}


############################################################
## Resolver for Django Multi Value Dictionaries
############################################################


class MultiValueDictResolver(DictResolver):
    """
    Class used to resolve from Django multi value dictionaries.
    """
    def resolve(self, var, attribute):
        """
        Public method to get an attribute from a variable.
        
        @param var variable to extract an attribute or value from
        @type dict
        @param attribute name of the attribute to extract
        @type str
        @return value of the attribute
        @rtype any
        """
        if " (ID:" not in attribute:
            try:
                return var[attribute]
            except Exception:
                return getattr(var, attribute, None)
        
        expectedID = int(attribute.split(" (ID:")[-1][:-1])
        for key in var.keys():
            if id(key) == expectedID:
                return var.getlist(key)
        
        return None
    
    def getDictionary(self, var):
        """
        Public method to get the attributes of a variable as a dictionary.
        
        @param var variable to be converted
        @type any
        @yield tuple containing the batch start index and a dictionary
            containing the variable attributes
        @ytype tuple of (int, dict)
        """
        d = {}
        start = count = 0
        allKeys = list(var.keys())
        try:
            # Fast path: all items from same type
            allKeys.sort()
        except TypeError:
            # Slow path: only sort items with same type (Py3 only)
            allKeys.sort(key=lambda x: (str(x), x))
        
        for key in allKeys:
            dkey = "{0} (ID:{1})".format(self.keyToStr(key), id(key))
            d[dkey] = var.getlist(key)
            count += 1
            if count >= BatchSize:
                yield start, d
                start += count
                count = 0
                d = {}
        
        if d:
            yield start, d
        
        # in case it has additional fields
        d = super(DictResolver, self).getDictionary(var)
        yield -1, d
        
        while True:
            yield -2, {}
    

############################################################
## Resolver for array.array
############################################################


class ArrayResolver(BaseResolver):
    """
    Class used to resolve from array.array including some meta data.
    """
    TypeCodeMap = {
        "b": "int (signed char)",
        "B": "int (unsigned char)",
        "u": "Unicode character (Py_UNICODE)",
        "h": "int (signed short)",
        "H": "int (unsigned short)",
        "i": "int (signed int)",
        "I": "int (unsigned int)",
        "l": "int (signed long)",
        "L": "int (unsigned long)",
        "q": "int (signed long long)",
        "Q": "int (unsigned long long)",
        "f": "float (float)",
        "d": "float (double)",
    }
    
    def resolve(self, var, attribute):
        """
        Public method to get an attribute from a variable.
        
        @param var variable to extract an attribute or value from
        @type tuple or list
        @param attribute id of the value to extract
        @type str
        @return value of the attribute
        @rtype any
        """
        try:
            return var[int(attribute)]
        except Exception:
            return getattr(var, attribute, None)
        
        return None
    
    def getDictionary(self, var):
        """
        Public method to get the attributes of a variable as a dictionary.
        
        @param var variable to be converted
        @type any
        @yield tuple containing the batch start index and a dictionary
            containing the variable attributes
        @ytype tuple of (int, dict)
        """
        d = {}
        start = count = 0
        allItems = var.tolist()
        
        for idx, value in enumerate(allItems):
            d[str(idx)] = value
            count += 1
            if count >= BatchSize:
                yield start, d
                start += count
                count = 0
                d = {}
        
        if d:
            yield start, d
        
        # in case it has additional fields
        d = super(ArrayResolver, self).getDictionary(var)
        
        # Special data for array type: convert typecode to readable text
        d['type'] = self.TypeCodeMap.get(var.typecode, 'illegal type')
        
        yield -1, d
        
        while True:
            yield -2, {}


defaultResolver = DefaultResolver()
dictResolver = DictResolver()
listResolver = ListResolver()
dictViewResolver = DictViewResolver()
setResolver = SetResolver()
ndarrayResolver = NdArrayResolver()
multiValueDictResolver = MultiValueDictResolver()
arrayResolver = ArrayResolver()

############################################################
## Methods to determine the type of a variable and the
## resolver class to use
############################################################

_TypeMap = None


def _initTypeMap():
    """
    Protected function to initialize the type map.
    """
    global _TypeMap
    
    _TypeMap = [
        (type(None), None,),
        (int, None),
        (float, None),
        (complex, None),
        (str, None),
        (tuple, listResolver),
        (list, listResolver),
        (dict, dictResolver),
        (set, setResolver),
        (frozenset, setResolver),
    ]
    
    try:
        _TypeMap.append((long, None))           # __IGNORE_WARNING__
    except Exception:       # secok
        pass    # not available on all Python versions

    try:
        import array
        _TypeMap.append((array.array, arrayResolver))
    except ImportError:
        pass  # array.array may not be available
    
    try:
        import numpy
        _TypeMap.append((numpy.ndarray, ndarrayResolver))
    except ImportError:
        pass  # numpy may not be installed
    
    try:
        from django.utils.datastructures import MultiValueDict
        # it should go before dict
        _TypeMap.insert(0, (MultiValueDict, multiValueDictResolver))
    except ImportError:
        pass  # django may not be installed
    
    try:
        from collections.abc import ItemsView, KeysView, ValuesView
        _TypeMap.append((ItemsView, dictViewResolver))
        _TypeMap.append((KeysView, dictViewResolver))
        _TypeMap.append((ValuesView, dictViewResolver))
    except ImportError:
        pass  # not available on all Python versions


def getType(obj):
    """
    Public method to get the type information for an object.
    
    @param obj object to get type information for
    @type any
    @return tuple containing the type name, type string and resolver
    @rtype tuple of str, str, BaseResolver
    """
    typeObject = type(obj)
    typeName = typeObject.__name__
    # Between PyQt and PySide the returned type is different (class vs. type)
    typeStr = str(typeObject).split(' ', 1)[-1]
    typeStr = typeStr[1:-2]
    
    if (
        typeStr.startswith(ConfigQtNames) and
        typeStr.endswith(ConfigKnownQtTypes)
    ):
        resolver = None
    else:
        if _TypeMap is None:
            _initTypeMap()
        
        for typeData, resolver in _TypeMap:  # __IGNORE_WARNING_M507__
            if isinstance(obj, typeData):
                break
        else:
            resolver = defaultResolver
    
    return typeName, typeStr, resolver
