# -*- coding: utf-8 -*-

# Copyright (c) 2005 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Parse a Python file and retrieve classes, functions/methods and attributes.

Parse enough of a Python file to recognize class and method definitions and
to find out the superclasses of a class as well as its attributes.
"""

import sys
import re
from functools import reduce

import Utilities
import Utilities.ClassBrowsers as ClassBrowsers
from . import ClbrBaseClasses

TABWIDTH = 4

SUPPORTED_TYPES = [ClassBrowsers.PY_SOURCE, ClassBrowsers.PTL_SOURCE]

_getnext = re.compile(
    r"""
   (?P<CodingLine>
        ^ \# \s* [*_-]* \s* coding[:=] \s* (?P<Coding> [-\w_.]+ ) \s* [*_-]* $
    )

|   (?P<String>
        \# .*? $   # ignore everything in comments
    |
        \""" [^"\\]* (?:
                        (?: \\. | "(?!"") )
                        [^"\\]*
                    )*
        \"""

    |   ''' [^'\\]* (?:
                        (?: \\. | '(?!'') )
                        [^'\\]*
                    )*
        '''

    |   " [^"\\\n]* (?: \\. [^"\\\n]*)* "

    |   ' [^'\\\n]* (?: \\. [^'\\\n]*)* '
    )

|   (?P<Publics>
        ^
        [ \t]* __all__ [ \t]* = [ \t]* \[
        (?P<Identifiers> [^\]]*? )
        \]
    )

|   (?P<MethodModifier>
        ^
        (?P<MethodModifierIndent> [ \t]* )
        (?P<MethodModifierType> @classmethod | @staticmethod )
    )

|   (?P<Method>
        ^
        (?P<MethodIndent> [ \t]* )
        (?: async [ \t]+ )? (?: cdef | cpdef | def) [ \t]+
        (?P<MethodName> \w+ )
        (?: [ \t]* \[ (?: plain | html ) \] )?
        [ \t]* \(
        (?P<MethodSignature> (?: [^)] | \)[ \t]*,? )*? )
        \) [ \t]*
        (?P<MethodReturnAnnotation> (?: -> [ \t]* [^:]+ )? )
        [ \t]* :
    )

|   (?P<Class>
        ^
        (?P<ClassIndent> [ \t]* )
        (?: cdef [ \t]+ )?
        class [ \t]+
        (?P<ClassName> \w+ )
        [ \t]*
        (?P<ClassSupers> \( [^)]* \) )?
        [ \t]* :
    )

|   (?P<Attribute>
        ^
        (?P<AttributeIndent> [ \t]* )
        self [ \t]* \. [ \t]*
        (?P<AttributeName> \w+ )
        [ \t]* =
    )

|   (?P<Variable>
        ^
        (?P<VariableIndent> [ \t]* )
        (?P<VariableName> \w+ )
        [ \t]* =
    )

|   (?P<Main>
        ^
        if \s+ __name__ \s* == \s* [^:]+ : $
    )

|   (?P<ConditionalDefine>
        ^
        (?P<ConditionalDefineIndent> [ \t]* )
        (?: (?: if | elif ) [ \t]+ [^:]* | else [ \t]* ) :
        (?= \s* (?: async [ \t]+ )? def)
    )

|   (?P<Import>
        ^ [ \t]* (?: c? import | from [ \t]+ \. [ \t]+ c? import ) [ \t]+
        (?P<ImportList> (?: [^#;\\\n]* (?: \\\n )* )* )
    )

|   (?P<ImportFrom>
        ^ [ \t]* from [ \t]+
        (?P<ImportFromPath>
            \.* \w+
            (?:
                [ \t]* \. [ \t]* \w+
            )*
        )
        [ \t]+
        c? import [ \t]+
        (?P<ImportFromList>
            (?: \( \s* .*? \s* \) )
            |
            (?: [^#;\\\n]* (?: \\\n )* )* )
    )""",
    re.VERBOSE | re.DOTALL | re.MULTILINE).search

_commentsub = re.compile(r"""#[^\n]*\n|#[^\n]*$""").sub

_modules = {}                           # cache of modules we've seen


class VisibilityMixin(ClbrBaseClasses.ClbrVisibilityMixinBase):
    """
    Mixin class implementing the notion of visibility.
    """
    def __init__(self):
        """
        Constructor
        """
        if self.name.startswith('__'):
            self.setPrivate()
        elif self.name.startswith('_'):
            self.setProtected()
        else:
            self.setPublic()


class Class(ClbrBaseClasses.Class, VisibilityMixin):
    """
    Class to represent a Python class.
    """
    def __init__(self, module, name, superClasses, file, lineno):
        """
        Constructor
        
        @param module name of the module containing this class
        @param name name of this class
        @param superClasses list of class names this class is inherited from
        @param file filename containing this class
        @param lineno linenumber of the class definition
        """
        ClbrBaseClasses.Class.__init__(self, module, name, superClasses, file,
                                       lineno)
        VisibilityMixin.__init__(self)


class Function(ClbrBaseClasses.Function, VisibilityMixin):
    """
    Class to represent a Python function.
    """
    def __init__(self, module, name, file, lineno, signature='', separator=',',
                 modifierType=ClbrBaseClasses.Function.General, annotation=""):
        """
        Constructor
        
        @param module name of the module containing this function
        @param name name of this function
        @param file filename containing this class
        @param lineno linenumber of the class definition
        @param signature parameterlist of the method
        @param separator string separating the parameters
        @param modifierType type of the function
        @param annotation return annotation
        """
        ClbrBaseClasses.Function.__init__(self, module, name, file, lineno,
                                          signature, separator, modifierType,
                                          annotation)
        VisibilityMixin.__init__(self)


class Attribute(ClbrBaseClasses.Attribute, VisibilityMixin):
    """
    Class to represent a class attribute.
    """
    def __init__(self, module, name, file, lineno):
        """
        Constructor
        
        @param module name of the module containing this class
        @param name name of this class
        @param file filename containing this attribute
        @param lineno linenumber of the class definition
        """
        ClbrBaseClasses.Attribute.__init__(self, module, name, file, lineno)
        VisibilityMixin.__init__(self)


class Publics(object):
    """
    Class to represent the list of public identifiers.
    """
    def __init__(self, module, file, lineno, idents):
        """
        Constructor
        
        @param module name of the module containing this function
        @param file filename containing this class
        @param lineno linenumber of the class definition
        @param idents list of public identifiers
        """
        self.module = module
        self.name = '__all__'
        self.file = file
        self.lineno = lineno
        self.identifiers = [e.replace('"', '').replace("'", "").strip()
                            for e in idents.split(',')]


class Imports(object):
    """
    Class to represent the list of imported modules.
    """
    def __init__(self, module, file):
        """
        Constructor
        
        @param module name of the module containing the import (string)
        @param file file name containing the import (string)
        """
        self.module = module
        self.name = 'import'
        self.file = file
        self.imports = {}
    
    def addImport(self, moduleName, names, lineno):
        """
        Public method to add a list of imported names.
        
        @param moduleName name of the imported module (string)
        @param names list of names (list of strings)
        @param lineno line number of the import
        """
        if moduleName not in self.imports:
            module = ImportedModule(self.module, self.file, moduleName)
            self.imports[moduleName] = module
        else:
            module = self.imports[moduleName]
        module.addImport(lineno, names)
    
    def getImport(self, moduleName):
        """
        Public method to get an imported module item.
        
        @param moduleName name of the imported module (string)
        @return imported module item (ImportedModule) or None
        """
        if moduleName in self.imports:
            return self.imports[moduleName]
        else:
            return None
    
    def getImports(self):
        """
        Public method to get all imported module names.
        
        @return dictionary of imported module names with name as key and list
            of line numbers of imports as value
        """
        return self.imports


class ImportedModule(object):
    """
    Class to represent an imported module.
    """
    def __init__(self, module, file, importedModule):
        """
        Constructor
        
        @param module name of the module containing the import (string)
        @param file file name containing the import (string)
        @param importedModule name of the imported module (string)
        """
        self.module = module
        self.name = 'import'
        self.file = file
        self.importedModuleName = importedModule
        self.linenos = []
        self.importedNames = {}
        # dictionary of imported names with name as key and list of line
        # numbers as value
    
    def addImport(self, lineno, importedNames):
        """
        Public method to add a list of imported names.
        
        @param lineno line number of the import
        @param importedNames list of imported names (list of strings)
        """
        if lineno not in self.linenos:
            self.linenos.append(lineno)
        
        for name in importedNames:
            if name not in self.importedNames:
                self.importedNames[name] = [lineno]
            else:
                self.importedNames[name].append(lineno)
    

def readmodule_ex(module, path=None, inpackage=False, isPyFile=False):
    """
    Read a module file and return a dictionary of classes.

    Search for MODULE in PATH and sys.path, read and parse the
    module and return a dictionary with one entry for each class
    found in the module.
    
    @param module name of the module file
    @type str
    @param path path the module should be searched in
    @type list of str
    @param inpackage flag indicating a module inside a package is scanned
    @type bool
    @param isPyFile flag indicating a Python file
    @type bool
    @return the resulting dictionary
    @rtype dict
    """
    global _modules
    
    if module in _modules:
        # we've seen this module before...
        return _modules[module]
    if module in sys.builtin_module_names:
        # this is a built-in module
        _modules[module] = {}
        return {}

    # search the path for the module
    path = [] if path is None else path[:]
    f = None
    if inpackage:
        try:
            f, file, (suff, mode, type) = ClassBrowsers.find_module(
                module, path)
        except ImportError:
            f = None
    if f is None:
        fullpath = path[:] + sys.path[:]
        f, file, (suff, mode, type) = ClassBrowsers.find_module(
            module, fullpath, isPyFile)
    if f:
        f.close()
    if type not in SUPPORTED_TYPES:
        # not Python source, can't do anything with this module
        _modules[module] = {}
        return {}

    try:
        src = Utilities.readEncodedFile(file)[0]
    except (UnicodeError, OSError):
        # can't do anything with this module
        _modules[module] = {}
        return {}
    
    _modules[module] = scan(src, file, module)
    return _modules[module]


def scan(src, file, module):
    """
    Public method to scan the given source text.
    
    @param src source text to be scanned
    @type str
    @param file file name associated with the source text
    @type str
    @param module module name associated with the source text
    @type str
    @return dictionary containing the extracted data
    @rtype dict
    """
    def calculateEndline(lineno, lines, indent):
        """
        Function to calculate the end line of a class or method/function.
        
        @param lineno line number to start at (one based)
        @type int
        @param lines list of source lines
        @type list of str
        @param indent indent length the class/method/function definition
        @type int
        @return end line of the class/method/function (one based)
        @rtype int
        """
        # start with zero based line after start line
        while lineno < len(lines):
            line = lines[lineno]
            if line.strip():
                # line contains some text
                lineIndent = _indent(line.replace(line.lstrip(), ""))
                if lineIndent <= indent:
                    return lineno
            lineno += 1
        
        # nothing found
        return -1
    
    # convert eol markers the Python style
    src = src.replace("\r\n", "\n").replace("\r", "\n")
    srcLines = src.splitlines()
    
    dictionary = {}
    dict_counts = {}
    
    classstack = []  # stack of (class, indent) pairs
    conditionalsstack = []  # stack of indents of conditional defines
    deltastack = []
    deltaindent = 0
    deltaindentcalculated = False
    
    lineno, last_lineno_pos = 1, 0
    i = 0
    modifierType = ClbrBaseClasses.Function.General
    modifierIndent = -1
    while True:
        m = _getnext(src, i)
        if not m:
            break
        start, i = m.span()

        if m.start("MethodModifier") >= 0:
            modifierIndent = _indent(m.group("MethodModifierIndent"))
            modifierType = m.group("MethodModifierType")
        
        elif m.start("Method") >= 0:
            # found a method definition or function
            thisindent = _indent(m.group("MethodIndent"))
            meth_name = m.group("MethodName")
            meth_sig = m.group("MethodSignature")
            meth_sig = meth_sig.replace('\\\n', '')
            meth_sig = _commentsub('', meth_sig)
            meth_ret = m.group("MethodReturnAnnotation")
            meth_ret = meth_ret.replace('\\\n', '')
            meth_ret = _commentsub('', meth_ret)
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            if modifierType and modifierIndent == thisindent:
                if modifierType == "@staticmethod":
                    modifier = ClbrBaseClasses.Function.Static
                elif modifierType == "@classmethod":
                    modifier = ClbrBaseClasses.Function.Class
                else:
                    modifier = ClbrBaseClasses.Function.General
            else:
                modifier = ClbrBaseClasses.Function.General
            # modify indentation level for conditional defines
            if conditionalsstack:
                if thisindent > conditionalsstack[-1]:
                    if not deltaindentcalculated:
                        deltastack.append(thisindent - conditionalsstack[-1])
                        deltaindent = reduce(lambda x, y: x + y, deltastack)
                        deltaindentcalculated = True
                    thisindent -= deltaindent
                else:
                    while (
                        conditionalsstack and
                        conditionalsstack[-1] >= thisindent
                    ):
                        del conditionalsstack[-1]
                        if deltastack:
                            del deltastack[-1]
                    deltaindentcalculated = False
            # close all classes indented at least as much
            while classstack and classstack[-1][1] >= thisindent:
                del classstack[-1]
            if classstack:
                # it's a class method
                cur_class = classstack[-1][0]
                if cur_class:
                    # it's a method/nested def
                    f = Function(None, meth_name,
                                 file, lineno, meth_sig, annotation=meth_ret,
                                 modifierType=modifier)
                    cur_class._addmethod(meth_name, f)
                else:
                    f = None
            else:
                # it's a function
                f = Function(module, meth_name,
                             file, lineno, meth_sig, annotation=meth_ret,
                             modifierType=modifier)
                if meth_name in dict_counts:
                    dict_counts[meth_name] += 1
                    meth_name = "{0}_{1:d}".format(
                        meth_name, dict_counts[meth_name])
                else:
                    dict_counts[meth_name] = 0
                dictionary[meth_name] = f
            if f:
                endlineno = calculateEndline(lineno, srcLines, thisindent)
                f.setEndLine(endlineno)
                classstack.append((f, thisindent))  # Marker for nested fns
            
            # reset the modifier settings
            modifierType = ClbrBaseClasses.Function.General
            modifierIndent = -1

        elif m.start("String") >= 0:
            pass

        elif m.start("Class") >= 0:
            # we found a class definition
            thisindent = _indent(m.group("ClassIndent"))
            # close all classes indented at least as much
            while classstack and classstack[-1][1] >= thisindent:
                del classstack[-1]
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            class_name = m.group("ClassName")
            inherit = m.group("ClassSupers")
            if inherit:
                # the class inherits from other classes
                inherit = inherit[1:-1].strip()
                inherit = _commentsub('', inherit)
                names = []
                for n in inherit.split(','):
                    n = n.strip()
                    if n in dictionary:
                        # we know this super class
                        n = dictionary[n]
                    else:
                        c = n.split('.')
                        if len(c) > 1:
                            # super class
                            # is of the
                            # form module.class:
                            # look in
                            # module for class
                            m = c[-2]
                            c = c[-1]
                            if m in _modules:
                                d = _modules[m]
                                if c in d:
                                    n = d[c]
                    names.append(n)
                inherit = names
            # modify indentation level for conditional defines
            if conditionalsstack:
                if thisindent > conditionalsstack[-1]:
                    if not deltaindentcalculated:
                        deltastack.append(thisindent - conditionalsstack[-1])
                        deltaindent = reduce(lambda x, y: x + y, deltastack)
                        deltaindentcalculated = True
                    thisindent -= deltaindent
                else:
                    while (
                        conditionalsstack and
                        conditionalsstack[-1] >= thisindent
                    ):
                        del conditionalsstack[-1]
                        if deltastack:
                            del deltastack[-1]
                    deltaindentcalculated = False
            # remember this class
            cur_class = Class(module, class_name, inherit,
                              file, lineno)
            endlineno = calculateEndline(lineno, srcLines, thisindent)
            cur_class.setEndLine(endlineno)
            if not classstack:
                if class_name in dict_counts:
                    dict_counts[class_name] += 1
                    class_name = "{0}_{1:d}".format(
                        class_name, dict_counts[class_name])
                else:
                    dict_counts[class_name] = 0
                dictionary[class_name] = cur_class
            else:
                classstack[-1][0]._addclass(class_name, cur_class)
            classstack.append((cur_class, thisindent))

        elif m.start("Attribute") >= 0:
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            index = -1
            while index >= -len(classstack):
                if (
                    classstack[index][0] is not None and
                    not isinstance(classstack[index][0], Function)
                ):
                    attr = Attribute(
                        module, m.group("AttributeName"), file, lineno)
                    classstack[index][0]._addattribute(attr)
                    break
                else:
                    index -= 1

        elif m.start("Main") >= 0:
            # 'main' part of the script, reset class stack
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            classstack = []

        elif m.start("Variable") >= 0:
            thisindent = _indent(m.group("VariableIndent"))
            variable_name = m.group("VariableName")
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            if thisindent == 0 or not classstack:
                # global variable, reset class stack first
                classstack = []
                
                if "@@Globals@@" not in dictionary:
                    dictionary["@@Globals@@"] = ClbrBaseClasses.ClbrBase(
                        module, "Globals", file, lineno)
                dictionary["@@Globals@@"]._addglobal(
                    Attribute(module, variable_name, file, lineno))
            else:
                index = -1
                while index >= -len(classstack):
                    if classstack[index][1] >= thisindent:
                        index -= 1
                    else:
                        if isinstance(classstack[index][0], Class):
                            classstack[index][0]._addglobal(
                                Attribute(module, variable_name, file, lineno))
                        break

        elif m.start("Publics") >= 0:
            idents = m.group("Identifiers")
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            pubs = Publics(module, file, lineno, idents)
            dictionary['__all__'] = pubs
        
        elif m.start("Import") >= 0:
            #- import module
            names = [n.strip() for n in
                     "".join(m.group("ImportList").splitlines())
                     .replace("\\", "").split(',')]
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            if "@@Import@@" not in dictionary:
                dictionary["@@Import@@"] = Imports(module, file)
            for name in names:
                dictionary["@@Import@@"].addImport(name, [], lineno)
        
        elif m.start("ImportFrom") >= 0:
            #- from module import stuff
            mod = m.group("ImportFromPath")
            namesLines = (m.group("ImportFromList")
                          .replace("(", "").replace(")", "")
                          .replace("\\", "")
                          .strip().splitlines())
            namesLines = [line.split("#")[0].strip()
                          for line in namesLines]
            names = [n.strip() for n in
                     "".join(namesLines)
                     .split(',')]
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            if "@@Import@@" not in dictionary:
                dictionary["@@Import@@"] = Imports(module, file)
            dictionary["@@Import@@"].addImport(mod, names, lineno)
        
        elif m.start("ConditionalDefine") >= 0:
            # a conditional function/method definition
            thisindent = _indent(m.group("ConditionalDefineIndent"))
            while conditionalsstack and conditionalsstack[-1] >= thisindent:
                del conditionalsstack[-1]
                if deltastack:
                    del deltastack[-1]
            conditionalsstack.append(thisindent)
            deltaindentcalculated = False
        
        elif m.start("CodingLine") >= 0:
            # a coding statement
            coding = m.group("Coding")
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            if "@@Coding@@" not in dictionary:
                dictionary["@@Coding@@"] = ClbrBaseClasses.Coding(
                    module, file, lineno, coding)

    if '__all__' in dictionary:
        # set visibility of all top level elements
        pubs = dictionary['__all__']
        for key in dictionary.keys():
            if key == '__all__' or key.startswith("@@"):
                continue
            if key in pubs.identifiers:
                dictionary[key].setPublic()
            else:
                dictionary[key].setPrivate()
        del dictionary['__all__']
    
    return dictionary


def _indent(ws):
    """
    Module function to return the indentation depth.
    
    @param ws the whitespace to be checked (string)
    @return length of the whitespace string (integer)
    """
    return len(ws.expandtabs(TABWIDTH))
