# -*- coding: utf-8 -*-
#
# This module contains the configuration of the individual eric installation
#

_pkg_config = {
    'ericDir': r'E:\PythonProjects\venv\Lib\site-packages\eric6',
    'ericPixDir': r'E:\PythonProjects\venv\Lib\site-packages\eric6\pixmaps',
    'ericIconDir': r'E:\PythonProjects\venv\Lib\site-packages\eric6\icons',
    'ericDTDDir': r'E:\PythonProjects\venv\Lib\site-packages\eric6\DTDs',
    'ericCSSDir': r'E:\PythonProjects\venv\Lib\site-packages\eric6\CSSs',
    'ericStylesDir': r'E:\PythonProjects\venv\Lib\site-packages\eric6\Styles',
    'ericDocDir': r'E:\PythonProjects\venv\Lib\site-packages\eric6\Documentation',
    'ericExamplesDir': r'E:\PythonProjects\venv\Lib\site-packages\eric6\Examples',
    'ericTranslationsDir': r'E:\PythonProjects\venv\Lib\site-packages\eric6\i18n',
    'ericTemplatesDir': r'E:\PythonProjects\venv\Lib\site-packages\eric6\DesignerTemplates',
    'ericCodeTemplatesDir': r'E:\PythonProjects\venv\Lib\site-packages\eric6\CodeTemplates',
    'ericOthersDir': r'E:\PythonProjects\venv\Lib\site-packages\eric6',
    'bindir': r'E:\PythonProjects\venv\Scripts',
    'mdir': r'E:\PythonProjects\venv\Lib\site-packages',
    'apidir': r'E:\PythonProjects\venv\Lib\site-packages\PyQt5\Qt\qsci\api',
    'apis': ['Ruby-1.8.7.api', 'Ruby-1.9.1.api', 'calliope.api', 'circuitpython.api', 'eric6.api', 'microbit.api', 'micropython.api', 'micropython.api', 'qss.api', 'zope-2.10.7.api', 'zope-2.11.2.api', 'zope-3.3.1.api'],
}

def getConfig(name):
    '''
    Module function to get a configuration value.

    @param name name of the configuration value    @type str
    @exception AttributeError raised to indicate an invalid config entry
    '''
    try:
        return _pkg_config[name]
    except KeyError:
        pass

    raise AttributeError(
        '"{0}" is not a valid configuration value'.format(name))
