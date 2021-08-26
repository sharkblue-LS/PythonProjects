# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#
# Original (c) 2005 Divmod, Inc.  See __init__.py file for details
#
# This module is based on pyflakes, but was modified to
# be integrated into eric

"""
Module providing the class Message and its subclasses.
"""


class Message(object):
    """
    Class defining the base for all specific message classes.
    """
    message_id = 'F00'
    message = ''
    message_args = ()

    def __init__(self, filename, loc):
        """
        Constructor
        
        @param filename name of the file
        @type str
        @param loc location of the issue
        """
        self.filename = filename
        self.lineno = loc.lineno
        self.col = getattr(loc, 'col_offset', 0)

    def __str__(self):
        """
        Special method return a string representation of the instance object.
        
        @return string representation of the object
        @rtype str
        """
        return '{0}:{1}:{2} {3}'.format(
            self.filename, self.lineno, self.col + 1,
            self.message % self.message_args)
    
    def getMessageData(self):
        """
        Public method to get the individual message data elements.
        
        @return tuple containing file name, line number, column, message ID
            and message arguments
        @rtype tuple of (str, int, int, str, list)
        """
        return (self.filename, self.lineno, self.col, self.message_id,
                self.message_args)


class UnusedImport(Message):
    """
    Class defining the "Unused Import" message.
    """
    message_id = 'F01'
    message = '%r imported but unused'

    def __init__(self, filename, loc, name):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param name name of the unused import (string)
        """
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class RedefinedWhileUnused(Message):
    """
    Class defining the "Redefined While Unused" message.
    """
    message_id = 'F02'
    message = 'redefinition of unused %r from line %r'

    def __init__(self, filename, loc, name, orig_loc):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param name name of the redefined object (string)
        @param orig_loc location of the original definition
        """
        Message.__init__(self, filename, loc)
        self.message_args = (name, orig_loc.lineno)


class RedefinedInListComp(Message):
    """
    Class defining the "Redefined In List Comprehension" message.
    """
    message_id = 'F12'
    message = 'list comprehension redefines %r from line %r'

    def __init__(self, filename, loc, name, orig_loc):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param name name of the redefined object (string)
        @param orig_loc location of the original definition
        """
        Message.__init__(self, filename, loc)
        self.message_args = (name, orig_loc.lineno)


class ImportShadowedByLoopVar(Message):
    """
    Class defining the "Import Shadowed By Loop Var" message.
    """
    message_id = 'F03'
    message = 'import %r from line %r shadowed by loop variable'

    def __init__(self, filename, loc, name, orig_loc):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param name name of the shadowed import (string)
        @param orig_loc location of the import
        """
        Message.__init__(self, filename, loc)
        self.message_args = (name, orig_loc.lineno)


class ImportStarNotPermitted(Message):
    """
    Class defining the "Import * not permitted" message.
    """
    message_id = 'F16'
    message = "'from %s import *' only allowed at module level"

    def __init__(self, filename, loc, modname):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param modname name of the module (string)
        """
        Message.__init__(self, filename, loc)
        self.message_args = (modname,)


class ImportStarUsed(Message):
    """
    Class defining the "Import Star Used" message.
    """
    message_id = 'F04'
    message = "'from %s import *' used; unable to detect undefined names"

    def __init__(self, filename, loc, modname):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param modname name of the module imported using star import (string)
        """
        Message.__init__(self, filename, loc)
        self.message_args = (modname,)


class ImportStarUsage(Message):
    """
    Class defining the "Import Star Usage" message.
    """
    message_id = 'F17'
    message = "%r may be undefined, or defined from star imports: %s"

    def __init__(self, filename, loc, name, from_list):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param name name of the variable (string)
        @param from_list list of modules imported from with * (string)
        """
        Message.__init__(self, filename, loc)
        self.message_args = (name, from_list)


class UndefinedName(Message):
    """
    Class defining the "Undefined Name" message.
    """
    message_id = 'F05'
    message = 'undefined name %r'

    def __init__(self, filename, loc, name):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param name undefined name (string)
        """
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class DoctestSyntaxError(Message):
    """
    Class defining the "Doctest syntax Error" message.
    """
    message_id = 'F13'
    message = 'syntax error in doctest'

    def __init__(self, filename, loc, position=None):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param position position of the syntax error
        """
        Message.__init__(self, filename, loc)
        if position:
            (self.lineno, self.col) = position
        self.message_args = ()


class UndefinedExport(Message):
    """
    Class defining the "Undefined Export" message.
    """
    message_id = 'F06'
    message = 'undefined name %r in __all__'

    def __init__(self, filename, loc, name):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param name undefined exported name (string)
        """
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class UndefinedLocal(Message):
    """
    Class defining the "Undefined Local Variable" message.
    """
    message_id = 'F07'
    message = 'local variable %r {0} referenced before assignment'

    default = 'defined in enclosing scope on line %r'
    builtin = 'defined as a builtin'

    def __init__(self, filename, loc, name, orig_loc):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param name name of the prematurely referenced variable (string)
        @param orig_loc location of the variable definition
        """
        Message.__init__(self, filename, loc)
        if orig_loc is None:
            self.message = self.message.format(self.builtin)
            self.message_args = (name,)
            self.message_id = 'F07B'
        else:
            self.message = self.message.format(self.default)
            self.message_args = (name, orig_loc.lineno)
            self.message_id = 'F07A'


class DuplicateArgument(Message):
    """
    Class defining the "Duplicate Argument" message.
    """
    message_id = 'F08'
    message = 'duplicate argument %r in function definition'

    def __init__(self, filename, loc, name):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param name name of the duplicate argument (string)
        """
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class MultiValueRepeatedKeyLiteral(Message):
    """
    Class defining the multiple used dictionary key message.
    """
    message_id = 'F18'
    message = 'dictionary key %r repeated with different values'

    def __init__(self, filename, loc, key):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param key dictionary key (string)
        """
        Message.__init__(self, filename, loc)
        self.message_args = (key,)


class MultiValueRepeatedKeyVariable(Message):
    """
    Class defining the multiple used dictionary key variable message.
    """
    message_id = 'F19'
    message = 'dictionary key variable %s repeated with different values'

    def __init__(self, filename, loc, key):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param key dictionary key variable (string)
        """
        Message.__init__(self, filename, loc)
        self.message_args = (key,)


class LateFutureImport(Message):
    """
    Class defining the "Late Future Import" message.
    """
    message_id = 'F10'
    message = 'from __future__ imports must occur at the beginning of the file'

    def __init__(self, filename, loc, names):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param names names of the imported futures (string)
        """
        Message.__init__(self, filename, loc)
        self.message_args = ()


class FutureFeatureNotDefined(Message):
    """
    Class defining the undefined __future__ feature message.
    """
    message_id = 'F20'
    message = 'future feature %s is not defined'

    def __init__(self, filename, loc, name):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param name name of the imported undefined future feature (string)
        """
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class UnusedVariable(Message):
    """
    Class defining the "Unused Variable" message.
    
    Indicates that a variable has been explicitly assigned to but not actually
    used.
    """
    message_id = 'F11'
    message = 'local variable %r is assigned to but never used'

    def __init__(self, filename, loc, names):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param names names of unused variable (string)
        """
        Message.__init__(self, filename, loc)
        self.message_args = (names,)


class ReturnWithArgsInsideGenerator(Message):
    """
    Class defining the "Return values in generator" message.
    
    Indicates a return statement with arguments inside a generator.
    """
    message_id = 'F14'
    message = '\'return\' with argument inside generator'


class ReturnOutsideFunction(Message):
    """
    Class defining the "Return outside function" message.
    
    Indicates a return statement outside of a function/method.
    """
    message_id = 'F15'
    message = '\'return\' outside function'


class YieldOutsideFunction(Message):
    """
    Class defining the "Yield outside function" message.
    
    Indicates a yield or yield from statement outside of a function/method.
    """
    message_id = 'F21'
    message = '\'yield\' outside function'


# For whatever reason, Python gives different error messages for these two. We
# match the Python error message exactly.
class ContinueOutsideLoop(Message):
    """
    Class defining the "Continue outside loop" message.
    
    Indicates a continue statement outside of a while or for loop.
    """
    message_id = 'F22'
    message = '\'continue\' not properly in loop'


class BreakOutsideLoop(Message):
    """
    Class defining the "Break outside loop" message.
    
    Indicates a break statement outside of a while or for loop.
    """
    message_id = 'F23'
    message = '\'break\' outside loop'


class ContinueInFinally(Message):
    """
    Class defining the "Continue in finally block" message.
    
    Indicates a continue statement in a finally block in a while or for loop.
    """
    message_id = 'F24'
    message = '\'continue\' not supported inside \'finally\' clause'


class DefaultExceptNotLast(Message):
    """
    Class defining the "Default except not being the last" message.
    
    Indicates an except: block as not the last exception handler.
    """
    message_id = 'F25'
    message = 'default \'except:\' must be last'


class TwoStarredExpressions(Message):
    """
    Class defining the "multiple starred expressions" message.
    
    Two or more starred expressions in an assignment (a, *b, *c = d).
    """
    message_id = 'F26'
    message = 'two starred expressions in assignment'


class TooManyExpressionsInStarredAssignment(Message):
    """
    Class defining the "too many starred expressions" message.
    
    Too many expressions in an assignment with star-unpacking
    """
    message_id = 'F27'
    message = 'too many expressions in star-unpacking assignment'


class IfTuple(Message):
    """
    Class defining the "non-empty tuple literal" message.
    
    Conditional test is a non-empty tuple literal, which are always True.
    """
    message_id = 'F49'
    message = (
        '\'if tuple literal\' is always true, perhaps remove accidental comma?'
    )


class AssertTuple(Message):
    """
    Class defining the "tuple assertion" message.
    
    Assertion test is a tuple, which are always True.
    """
    message_id = 'F28'
    message = 'assertion is always true, perhaps remove parentheses?'


class ForwardAnnotationSyntaxError(Message):
    """
    Class defining the "forward annotation syntax error" message.
    
    Found a syntax error in forward annotation.
    """
    message_id = 'F29'
    message = 'syntax error in forward annotation %r'

    def __init__(self, filename, loc, annotation):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param annotation erroneous forward annotation (string)
        """
        Message.__init__(self, filename, loc)
        self.message_args = (annotation,)


class CommentAnnotationSyntaxError(Message):
    """
    Class defining the "Comment Annotation Syntax Error" message.
    
    Indicates a syntax error in a type comment.
    """
    message_id = 'F31'
    message = 'syntax error in type comment %r'

    def __init__(self, filename, loc, annotation):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param annotation erroneous forward annotation (string)
        """
        Message.__init__(self, filename, loc)
        self.message_args = (annotation,)


class RaiseNotImplemented(Message):
    """
    Class defining the "raise not implemented" message.
    
    Use NotImplementedError instead of NotImplemented.
    """
    message_id = 'F30'
    message = "'raise NotImplemented' should be 'raise NotImplementedError'"


class InvalidPrintSyntax(Message):
    """
    Class defining the "Invalid Print Syntax" message.
    
    Indicates the use of >> with a print function.
    """
    message_id = 'F32'
    message = 'use of >> is invalid with print function'


class IsLiteral(Message):
    """
    Class defining the "Is Literal" message.
    
    Indicates the use of "is" or "is not" against str, int and bytes.
    """
    message_id = 'F33'
    message = 'use ==/!= to compare str, bytes, and int literals'


class FStringMissingPlaceholders(Message):
    """
    Class defining the "Missing Placeholder" message.
    
    Indicates that an f-string is missing some placeholders.
    """
    message_id = 'F34'
    message = 'f-string is missing placeholders'


class StringDotFormatExtraPositionalArguments(Message):
    """
    Class defining the "Unused Arguments" message.
    
    Indicates that an f-string has unused arguments.
    """
    message_id = 'F35'
    message = "'...'.format(...) has unused arguments at position(s): %s"

    def __init__(self, filename, loc, extra_positions):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param extra_positions indexes of unused arguments
        """
        Message.__init__(self, filename, loc)
        self.message_args = (extra_positions,)


class StringDotFormatExtraNamedArguments(Message):
    """
    Class defining the "Unused Named Arguments" message.
    
    Indicates that an f-string has unused named arguments.
    """
    message_id = 'F36'
    message = "'...'.format(...) has unused named argument(s): %s"

    def __init__(self, filename, loc, extra_keywords):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param extra_keywords index of unused named arguments
        """
        Message.__init__(self, filename, loc)
        self.message_args = (extra_keywords,)


class StringDotFormatMissingArgument(Message):
    """
    Class defining the "Missing Arguments" message.
    
    Indicates that an f-string is missing some arguments.
    """
    message_id = 'F37'
    message = "'...'.format(...) is missing argument(s) for placeholder(s): %s"

    def __init__(self, filename, loc, missing_arguments):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param missing_arguments missing arguments
        """
        Message.__init__(self, filename, loc)
        self.message_args = (missing_arguments,)


class StringDotFormatMixingAutomatic(Message):
    """
    Class defining the "Mixing Automatic and Manual" message.
    
    Indicates that an f-string mixes automatic and manual numbering.
    """
    message_id = 'F38'
    message = "'...'.format(...) mixes automatic and manual numbering"


class StringDotFormatInvalidFormat(Message):
    """
    Class defining the "Invalid Format String" message.
    
    Indicates that an f-string contains an invalid format string.
    """
    message_id = 'F39'
    message = "'...'.format(...) has invalid format string: %s"

    def __init__(self, filename, loc, error):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param error error details
        """
        Message.__init__(self, filename, loc)
        if not isinstance(error, str):
            error = str(error)
        self.message_args = (error,)


class PercentFormatInvalidFormat(Message):
    """
    Class defining the "Invalid Percent Format String" message.
    
    Indicates that a percent format has an invalid format string.
    """
    message_id = 'F40'
    message = "'...' %% ... has invalid format string: %s"

    def __init__(self, filename, loc, error):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param error error details
        """
        Message.__init__(self, filename, loc)
        self.message_args = (error,)


class PercentFormatMixedPositionalAndNamed(Message):
    """
    Class defining the "Mixed Positional and Named" message.
    
    Indicates that a percent format has mixed positional and named
    placeholders.
    """
    message_id = 'F41'
    message = "'...' %% ... has mixed positional and named placeholders"


class PercentFormatUnsupportedFormatCharacter(Message):
    """
    Class defining the "Unsupported Format Character" message.
    
    Indicates that a percent format has an unsupported format character.
    """
    message_id = 'F42'
    message = "'...' %% ... has unsupported format character %r"

    def __init__(self, filename, loc, c):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param c unsupported format character
        """
        Message.__init__(self, filename, loc)
        self.message_args = (c,)


class PercentFormatPositionalCountMismatch(Message):
    """
    Class defining the "Placeholder Substitution Mismatch" message.
    
    Indicates that a percent format has a mismatching number of placeholders
    and substitutions.
    """
    message_id = 'F43'
    message = "'...' %% ... has %d placeholder(s) but %d substitution(s)"

    def __init__(self, filename, loc, n_placeholders, n_substitutions):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param n_placeholders number of placeholders (integer)
        @param n_substitutions number of substitutions (integer)
        """
        Message.__init__(self, filename, loc)
        self.message_args = (n_placeholders, n_substitutions)


class PercentFormatExtraNamedArguments(Message):
    """
    Class defining the "Unused Named Arguments" message.
    
    Indicates that a percent format has unused named arguments.
    """
    message_id = 'F44'
    message = "'...' %% ... has unused named argument(s): %s"

    def __init__(self, filename, loc, extra_keywords):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param extra_keywords index of unused named arguments
        """
        Message.__init__(self, filename, loc)
        self.message_args = (extra_keywords,)


class PercentFormatMissingArgument(Message):
    """
    Class defining the "Missing Arguments" message.
    
    Indicates that a percent format is missing arguments for some placeholders.
    """
    message_id = 'F45'
    message = "'...' %% ... is missing argument(s) for placeholder(s): %s"

    def __init__(self, filename, loc, missing_arguments):
        """
        Constructor
        
        @param filename name of the file (string)
        @param loc location of the issue
        @param missing_arguments missing arguments
        """
        Message.__init__(self, filename, loc)
        self.message_args = (missing_arguments,)


class PercentFormatExpectedMapping(Message):
    """
    Class defining the "Sequence instead of Mapping" message.
    
    Indicates that a percent format expected a mapping but got a sequence.
    """
    message_id = 'F46'
    message = "'...' %% ... expected mapping but got sequence"


class PercentFormatExpectedSequence(Message):
    """
    Class defining the "Mapping instead of Sequence" message.
    
    Indicates that a percent format expected a sequence but got a mapping.
    """
    message_id = 'F47'
    message = "'...' %% ... expected sequence but got mapping"


class PercentFormatStarRequiresSequence(Message):
    """
    Class defining the "'*' Requires Sequence" message.
    
    Indicates that a percent format expected a sequence.
    """
    message_id = 'F48'
    message = "'...' %% ... `*` specifier requires sequence"
