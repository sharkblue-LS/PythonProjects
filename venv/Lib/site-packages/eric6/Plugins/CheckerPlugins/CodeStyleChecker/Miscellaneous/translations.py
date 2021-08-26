# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#


"""
Module implementing message translations for the code style plugin messages
(miscellaneous part).
"""

from PyQt5.QtCore import QCoreApplication

_miscellaneousMessages = {
    "M101": QCoreApplication.translate(
        "MiscellaneousChecker",
        "coding magic comment not found"),
    "M102": QCoreApplication.translate(
        "MiscellaneousChecker",
        "unknown encoding ({0}) found in coding magic comment"),
    "M111": QCoreApplication.translate(
        "MiscellaneousChecker",
        "copyright notice not present"),
    "M112": QCoreApplication.translate(
        "MiscellaneousChecker",
        "copyright notice contains invalid author"),
    "M131": QCoreApplication.translate(
        "MiscellaneousChecker",
        '"{0}" is a Python builtin and is being shadowed; '
        'consider renaming the variable'),
    "M132": QCoreApplication.translate(
        "MiscellaneousChecker",
        '"{0}" is used as an argument and thus shadows a '
        'Python builtin; consider renaming the argument'),
    "M181": QCoreApplication.translate(
        "MiscellaneousChecker",
        'unnecessary generator - rewrite as a list comprehension'),
    "M182": QCoreApplication.translate(
        "MiscellaneousChecker",
        'unnecessary generator - rewrite as a set comprehension'),
    "M183": QCoreApplication.translate(
        "MiscellaneousChecker",
        'unnecessary generator - rewrite as a dict comprehension'),
    "M184": QCoreApplication.translate(
        "MiscellaneousChecker",
        'unnecessary list comprehension - rewrite as a set comprehension'),
    "M185": QCoreApplication.translate(
        "MiscellaneousChecker",
        'unnecessary list comprehension - rewrite as a dict comprehension'),
    "M186": QCoreApplication.translate(
        "MiscellaneousChecker",
        'unnecessary {0} call - rewrite as a literal'),
    "M187": QCoreApplication.translate(
        "MiscellaneousChecker",
        'unnecessary list comprehension - "{0}" can take a generator'),
    "M191": QCoreApplication.translate(
        "MiscellaneousChecker",
        'unnecessary {0} literal - rewrite as a {1} literal'),
    "M192": QCoreApplication.translate(
        "MiscellaneousChecker",
        'unnecessary {0} passed to tuple() - rewrite as a {1} literal'),
    "M193": QCoreApplication.translate(
        "MiscellaneousChecker",
        'unnecessary {0} passed to list() - rewrite as a {1} literal'),
    "M195": QCoreApplication.translate(
        "MiscellaneousChecker",
        'unnecessary list call - remove the outer call to list()'),
    "M196": QCoreApplication.translate(
        "MiscellaneousChecker",
        'unnecessary list comprehension - "in" can take a generator'),
    "M197": QCoreApplication.translate(
        "MiscellaneousChecker",
        'unnecessary {0} passed to tuple() - remove the outer call to {1}()'),
    "M198": QCoreApplication.translate(
        "MiscellaneousChecker",
        'unnecessary {0} passed to list() - remove the outer call to {1}()'),
    
    "M201": QCoreApplication.translate(
        "MiscellaneousChecker",
        "sort keys - '{0}' should be before '{1}'"),
    
    "M301": QCoreApplication.translate(
        "MiscellaneousChecker",
        "use of 'datetime.datetime()' without 'tzinfo' argument should be"
        " avoided"),
    "M302": QCoreApplication.translate(
        "MiscellaneousChecker",
        "use of 'datetime.datetime.today()' should be avoided.\n"
        "Use 'datetime.datetime.now(tz=)' instead."),
    "M303": QCoreApplication.translate(
        "MiscellaneousChecker",
        "use of 'datetime.datetime.utcnow()' should be avoided.\n"
        "Use 'datetime.datetime.now(tz=)' instead."),
    "M304": QCoreApplication.translate(
        "MiscellaneousChecker",
        "use of 'datetime.datetime.utcfromtimestamp()' should be avoided.\n"
        "Use 'datetime.datetime.fromtimestamp(, tz=)' instead."),
    "M305": QCoreApplication.translate(
        "MiscellaneousChecker",
        "use of 'datetime.datetime.now()' without 'tz' argument should be"
        " avoided"),
    "M306": QCoreApplication.translate(
        "MiscellaneousChecker",
        "use of 'datetime.datetime.fromtimestamp()' without 'tz' argument"
        " should be avoided"),
    "M307": QCoreApplication.translate(
        "MiscellaneousChecker",
        "use of 'datetime.datetime.strptime()' should be followed by"
        " '.replace(tzinfo=)'"),
    "M308": QCoreApplication.translate(
        "MiscellaneousChecker",
        "use of 'datetime.datetime.fromordinal()' should be avoided"),
    "M311": QCoreApplication.translate(
        "MiscellaneousChecker",
        "use of 'datetime.date()' should be avoided.\n"
        "Use 'datetime.datetime(, tzinfo=).date()' instead."),
    "M312": QCoreApplication.translate(
        "MiscellaneousChecker",
        "use of 'datetime.date.today()' should be avoided.\n"
        "Use 'datetime.datetime.now(tz=).date()' instead."),
    "M313": QCoreApplication.translate(
        "MiscellaneousChecker",
        "use of 'datetime.date.fromtimestamp()' should be avoided.\n"
        "Use 'datetime.datetime.fromtimestamp(tz=).date()' instead."),
    "M314": QCoreApplication.translate(
        "MiscellaneousChecker",
        "use of 'datetime.date.fromordinal()' should be avoided"),
    "M315": QCoreApplication.translate(
        "MiscellaneousChecker",
        "use of 'datetime.date.fromisoformat()' should be avoided"),
    "M321": QCoreApplication.translate(
        "MiscellaneousChecker",
        "use of 'datetime.time()' without 'tzinfo' argument should be"
        " avoided"),
    
    "M401": QCoreApplication.translate(
        "MiscellaneousChecker",
        "'sys.version[:3]' referenced (Python 3.10), use 'sys.version_info'"),
    "M402": QCoreApplication.translate(
        "MiscellaneousChecker",
        "'sys.version[2]' referenced (Python 3.10), use 'sys.version_info'"),
    "M403": QCoreApplication.translate(
        "MiscellaneousChecker",
        "'sys.version' compared to string (Python 3.10), use"
        " 'sys.version_info'"),
    "M411": QCoreApplication.translate(
        "MiscellaneousChecker",
        "'sys.version_info[0] == 3' referenced (Python 4), use '>='"),
    "M412": QCoreApplication.translate(
        "MiscellaneousChecker",
        "'six.PY3' referenced (Python 4), use 'not six.PY2'"),
    "M413": QCoreApplication.translate(
        "MiscellaneousChecker",
        "'sys.version_info[1]' compared to integer (Python 4),"
        " compare 'sys.version_info' to tuple"),
    "M414": QCoreApplication.translate(
        "MiscellaneousChecker",
        "'sys.version_info.minor' compared to integer (Python 4),"
        " compare 'sys.version_info' to tuple"),
    "M421": QCoreApplication.translate(
        "MiscellaneousChecker",
        "'sys.version[0]' referenced (Python 10), use 'sys.version_info'"),
    "M422": QCoreApplication.translate(
        "MiscellaneousChecker",
        "'sys.version' compared to string (Python 10),"
        " use 'sys.version_info'"),
    "M423": QCoreApplication.translate(
        "MiscellaneousChecker",
        "'sys.version[:1]' referenced (Python 10), use 'sys.version_info'"),
    
    "M501": QCoreApplication.translate(
        "MiscellaneousChecker",
        "Python does not support the unary prefix increment"),
    "M502": QCoreApplication.translate(
        "MiscellaneousChecker",
        "using .strip() with multi-character strings is misleading"),
    "M503": QCoreApplication.translate(
        "MiscellaneousChecker",
        "do not call assert False since python -O removes these calls"),
    "M504": QCoreApplication.translate(
        "MiscellaneousChecker",
        "'sys.maxint' is not defined in Python 3 - use 'sys.maxsize'"),
    "M505": QCoreApplication.translate(
        "MiscellaneousChecker",
        "'BaseException.message' has been deprecated as of Python 2.6 and is"
        " removed in Python 3 - use 'str(e)'"),
    "M506": QCoreApplication.translate(
        "MiscellaneousChecker",
        "assigning to 'os.environ' does not clear the environment -"
        " use 'os.environ.clear()'"),
    "M507": QCoreApplication.translate(
        "MiscellaneousChecker",
        "loop control variable {0} not used within the loop body -"
        " start the name with an underscore"),
    "M508": QCoreApplication.translate(
        "MiscellaneousChecker",
        "unncessary f-string"),
    "M509": QCoreApplication.translate(
        "MiscellaneousChecker",
        "cannot use 'self.__class__' as first argument of 'super()' call"),
    "M511": QCoreApplication.translate(
        "MiscellaneousChecker",
        """using 'hasattr(x, "__call__")' to test if 'x' is callable is"""
        """ unreliable"""),
    "M512": QCoreApplication.translate(
        "MiscellaneousChecker",
        "do not call getattr with a constant attribute value"),
    "M513": QCoreApplication.translate(
        "MiscellaneousChecker",
        "do not call setattr with a constant attribute value"),
    "M521": QCoreApplication.translate(
        "MiscellaneousChecker",
        "Python 3 does not include '.iter*' methods on dictionaries"),
    "M522": QCoreApplication.translate(
        "MiscellaneousChecker",
        "Python 3 does not include '.view*' methods on dictionaries"),
    "M523": QCoreApplication.translate(
        "MiscellaneousChecker",
        "'.next()' does not exist in Python 3"),
    "M524": QCoreApplication.translate(
        "MiscellaneousChecker",
        "'__metaclass__' does nothing on Python 3 -"
        " use 'class MyClass(BaseClass, metaclass=...)'"),
    
    "M601": QCoreApplication.translate(
        "MiscellaneousChecker",
        "found {0} formatter"),
    "M611": QCoreApplication.translate(
        "MiscellaneousChecker",
        "format string does contain unindexed parameters"),
    "M612": QCoreApplication.translate(
        "MiscellaneousChecker",
        "docstring does contain unindexed parameters"),
    "M613": QCoreApplication.translate(
        "MiscellaneousChecker",
        "other string does contain unindexed parameters"),
    "M621": QCoreApplication.translate(
        "MiscellaneousChecker",
        "format call uses too large index ({0})"),
    "M622": QCoreApplication.translate(
        "MiscellaneousChecker",
        "format call uses missing keyword ({0})"),
    "M623": QCoreApplication.translate(
        "MiscellaneousChecker",
        "format call uses keyword arguments but no named entries"),
    "M624": QCoreApplication.translate(
        "MiscellaneousChecker",
        "format call uses variable arguments but no numbered entries"),
    "M625": QCoreApplication.translate(
        "MiscellaneousChecker",
        "format call uses implicit and explicit indexes together"),
    "M631": QCoreApplication.translate(
        "MiscellaneousChecker",
        "format call provides unused index ({0})"),
    "M632": QCoreApplication.translate(
        "MiscellaneousChecker",
        "format call provides unused keyword ({0})"),
    "M651": QCoreApplication.translate(
        "MiscellaneousChecker",
        "logging statement uses string.format()"),
    "M652": QCoreApplication.translate(
        "MiscellaneousChecker",
        "logging statement uses '%'"),          # __IGNORE_WARNING_M601__
    "M653": QCoreApplication.translate(
        "MiscellaneousChecker",
        "logging statement uses '+'"),
    "M654": QCoreApplication.translate(
        "MiscellaneousChecker",
        "logging statement uses f-string"),
    "M655": QCoreApplication.translate(
        "MiscellaneousChecker",
        "logging statement uses 'warn' instead of 'warning'"),
    
    "M701": QCoreApplication.translate(
        "MiscellaneousChecker",
        "expected these __future__ imports: {0}; but only got: {1}"),
    "M702": QCoreApplication.translate(
        "MiscellaneousChecker",
        "expected these __future__ imports: {0}; but got none"),
    "M711": QCoreApplication.translate(
        "MiscellaneousChecker",
        "gettext import with alias _ found: {0}"),
    
    "M801": QCoreApplication.translate(
        "MiscellaneousChecker",
        "print statement found"),
    "M811": QCoreApplication.translate(
        "MiscellaneousChecker",
        "one element tuple found"),
    "M821": QCoreApplication.translate(
        "MiscellaneousChecker",
        "mutable default argument of type {0}"),
    "M822": QCoreApplication.translate(
        "MiscellaneousChecker",
        "mutable default argument of type {0}"),
    "M823": QCoreApplication.translate(
        "MiscellaneousChecker",
        "mutable default argument of function call '{0}'"),
    "M831": QCoreApplication.translate(
        "MiscellaneousChecker",
        "None should not be added at any return if function has no return"
        " value except None"),
    "M832": QCoreApplication.translate(
        "MiscellaneousChecker",
        "an explicit value at every return should be added if function has"
        " a return value except None"),
    "M833": QCoreApplication.translate(
        "MiscellaneousChecker",
        "an explicit return at the end of the function should be added if"
        " it has a return value except None"),
    "M834": QCoreApplication.translate(
        "MiscellaneousChecker",
        "a value should not be assigned to a variable if it will be used as a"
        " return value only"),
    "M841": QCoreApplication.translate(
        "MiscellaneousChecker",
        "prefer implied line continuation inside parentheses, "
        "brackets and braces as opposed to a backslash"),
    "M891": QCoreApplication.translate(
        "MiscellaneousChecker",
        "commented code lines should be removed"),
    
    "M901": QCoreApplication.translate(
        "MiscellaneousChecker",
        "{0}: {1}"),
}

_miscellaneousMessagesSampleArgs = {
    "M102": ["enc42"],
    "M131": ["list"],
    "M132": ["list"],
    "M188": ["sorted"],
    "M186": ["list"],
    "M191": ["list", "set"],
    "M192": ["list", "tuple"],
    "M193": ["tuple", "list"],
    "M197": ["tuple", "tuple"],
    "M198": ["list", "list"],
    "M201": ["bar", "foo"],
    "M507": ["x"],
    "M601": ["%s"],
    "M621": [5],
    "M622": ["foo"],
    "M631": [5],
    "M632": ["foo"],
    "M701": ["print_function, unicode_literals", "print_function"],
    "M702": ["print_function, unicode_literals"],
    "M711": ["lgettext"],
    "M821": ["Dict"],
    "M822": ["Call"],
    "M823": ["dict"],
    "M901": ["SyntaxError", "Invalid Syntax"],
}
