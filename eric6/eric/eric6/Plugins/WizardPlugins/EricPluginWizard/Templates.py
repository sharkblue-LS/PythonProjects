# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the various plug-in templates.
"""

mainTemplate = '''# -*- coding: utf-8 -*-

# Copyright (c) {year} {author} <{email}>
#

"""
Module documentation goes here.
"""

from PyQt5.QtCore import QObject

{config0}\
# Start-Of-Header
name = "{name}"
author = "{author} <{email}>"
autoactivate = {autoactivate}
deactivateable = {deactivateable}
version = "{version}"
{onDemand}\
className = "{className}"
packageName = "{packageName}"
shortDescription = "{shortDescription}"
longDescription = (
    """{longDescription}"""
)
needsRestart = {needsRestart}
pyqtApi = 2
# End-Of-Header

error = ""
    

{modulesetup}\
{exeData}\
{apiFiles}\
{preview}\
{config1}\
class {className}(QObject):
    """
    Class documentation goes here.
    """
{config2}\
    def __init__(self, ui):
        """
        Constructor
        
        @param ui reference to the user interface object
        @type UI.UserInterface
        """
        super({className}, self).__init__(ui)
        self.__ui = ui
    
    def activate(self):
        """
        Public method to activate this plug-in.
        
        @return tuple of None and activation status
        @rtype bool
        """
        global error
        error = ""     # clear previous error
        
        return None, True
    
    def deactivate(self):
        """
        Public method to deactivate this plug-in.
        """
        pass
{config3}'''

configTemplate0 = '''import Preferences

'''

configTemplate1 = '''def getConfigData():
    """
    Module function returning data as required by the configuration dialog.
    
    @return dictionary containing the relevant data
    @rtype dict
    """
    return {{
        "<unique key>": ["<display string>", "<pixmap filename>",
            pageCreationFunction, None, None],
    }}


def prepareUninstall():
    """
    Module function to prepare for an un-installation.
    """
    Preferences.Prefs.settings.remove({className}.PreferencesKey)


'''

configTemplate2 = '''    PreferencesKey = "{preferencesKey}"
    
'''

configTemplate3 = '''\
    
    def getPreferences(self, key):
        """
        Public method to retrieve the various settings values.
        
        @param key the key of the value to get
        @type str
        @return the requested setting value
        @rtype any
        """
        return None
    
    def setPreferences(self, key, value):
        """
        Public method to store the various settings values.
        
        @param key the key of the setting to be set
        @type str
        @param value the value to be set
        @type any
        """
        pass
'''

onDemandTemplate = '''pluginType = "{pluginType}"
pluginTypename = "{pluginTypename}"
'''

previewPixmapTemplate = '''def previewPix():
    """
    Module function to return a preview pixmap.
    
    @return preview pixmap
    @rtype QPixmap
    """
    from PyQt5.QtGui import QPixmap
    
    fname = "preview.png"
    return QPixmap(fname)
    

'''

exeDisplayDataListTemplate = '''def exeDisplayDataList():
    """
    Module function to support the display of some executable info.
    
    @return list of dictionaries containing the data to query the presence of
        the executable
    @rtype list of dict
    """
    dataList = []
    data = {
        "programEntry": True,
        "header": "<translated header string>",
        "exe": "dummyExe",
        "versionCommand": "--version",
        "versionStartsWith": "dummyExe",
        "versionRe": "",
        "versionPosition": -1,
        "version": "",
        "versionCleanup": None,
        "exeModule": None,
    }
    for exePath in ["exe1", "exe2"]:
        data["exe"] = exePath
        data["versionStartsWith"] = "<identifier>"
        dataList.append(data.copy())
    return dataList


'''

exeDisplayDataTemplate = '''def exeDisplayData():
    """
    Module function to support the display of some executable info.
    
    @return dictionary containing the data to query the presence of
        the executable
    @rtype dict
    """
    data = {
        "programEntry": True,
        "header": "<translated header string>",
        "exe": exe,
        "versionCommand": "--version",
        "versionStartsWith": "<identifier>",
        "versionRe": "",
        "versionPosition": -1,
        "version": "",
        "versionCleanup": None,
        "exeModule": None,
    }
    
    return data


'''

exeDisplayDataInfoTemplate = '''def exeDisplayData():
    """
    Module function to support the display of some executable info.
    
    @return dictionary containing the data to be shown
    @rtype dict
    """
    data = {
        "programEntry": False,
        "header": "<translated header string>",
        "text": "<translated entry string>",
        "version": "",
    }
    
    return data


'''

moduleSetupTemplate = '''def moduleSetup():
    """
    Module function to perform module level setup.
    """
    pass


'''

apiFilesTemplate = '''def apiFiles(language):
    """
    Module function to return the API files made available by this plug-in.
    
    @param language language to get APIs for
    @type str
    @return list of API filenames
    @rtype list of str
    """
    if language in ["Python3",  "Python"]:
        apisDir = os.path.join(
            os.path.dirname(__file__), "APIs", "Python")
        apis = glob.glob(os.path.join(apisDir, '*.api'))
        apisDir = os.path.join(
            os.path.dirname(__file__), "APIs", "Python3")
        apis.extend(glob.glob(os.path.join(apisDir, '*.api')))
    else:
        apis = []
    return apis


'''

#
# eflag: noqa = M841
