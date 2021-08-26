========================
README for the eric6 IDE
========================

0. What is eric6?
-----------------
eric6 is a full featured Python editor and IDE, written in Python. It is based
on the cross platform Qt UI toolkit, integrating the highly flexible Scintilla
editor control. It is designed to be usable as everyday quick and dirty editor
as well as being usable as a professional project management tool integrating
many advanced features Python offers the professional coder. eric6 includes a
plug-in system, which allows easy extension of the IDE functionality with
plug-ins downloadable from the net. For more details see
<https://eric-ide.python-projects.org>.

1. Installation
---------------
Installing eric6 is a simple process. There are various methods available.
Please choose the one best suited to your needs and skills. eric6 may be must
with Python 3, Qt5 and PyQt5.

1.1 Create a Python virtual environment for eric6
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is recommended to install eric6 into a Python virtual environment in order
to keep your Python distribution clean. In order to do that create it by
entering the following command in a terminal window.

**Linux, macOS**::

    python3 -m venv eric6_venv

**Windows**::

    python.exe -m venv eric6_venv

Replace ``eric6_venv`` with the desired path to the directory for the virtual
environment. All further instructions will assume this environment name.

1.2a Variant 1: Installation via the "install.py" script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This method results in the most complete install on all supported platforms.
After extracting the eric6 distribution archive just execute the following
command in a terminal window.

**Linux, macOS**::

    ~/eric6_venv/bin/python3 install.py

**Windows**::

    eric6_venv\Scripts\python.exe install.py

Change the path to the Python executable appropriately. The installation script
will check for all prerequisites and will ask for confirmation to install
them. If the installation process needs tuning type
``~/eric6_venv/bin/python3 install.py --help`` for some help. Using the
``--yes`` option answers yes to all questions automatically.

If you want to uninstall the package just execute the ``uninstall.py`` script.
This gets rid of all installed files. In this case please send an email to the
below mentioned address and tell me your reason. This might give me a hint on
how to improve eric6.

During the installation process a file containing some information about the
installation will be created. If this is not desired, the ``--no-info``
command line option may be added to the above given install command.

1.2b Variant 2: Installation via the Python Package Index PyPI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This method is the easiest one but does not create a macOS® Application. Enter
the following command in a terminal window.

**Linux, macOS**::

    ~/eric6_venv/bin/python3 -m pip install --upgrade eric-ide

**Windows**::

    eric6_venv\Scripts\python.exe -m pip install --upgrade eric-ide

Once the installation is finished navigate to the executable directory of
the Python virtual environment and execute the ``eric6_post_install`` script.
This will create application menu entries on Linux and desktop and start menu
entries on Windows® platforms.

**Linux**::

    ~/eric6_venv/bin/eric6_post_install

**Windows**::

    eric6_venv\Scripts\eric6_post_install.exe

1.3 Installation of Qt Tools via Qt online installer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In order to get the most out of eric6 it is recommended to install the Qt Tools
like ``Qt Designer`` or ``Qt Linguist``. The recommended way is this.

1. Download the Qt online installer from the Qt download site.

2. Install Qt by executing the installer.

3. Configure the path to the Qt tools on the ``Qt`` configuration page of the
   eric6 configuration dialog.

2. Installation of translations
-------------------------------
The default distribution archive of eric6 includes all supported translations
already. If the above installation variant 1 was performed with this, you may
skip this section.

If the ``nolang`` archive was used, translations may be added later on by
downloading the desired language pack, extract it to a temporary directory
and execute the install-i18n.py script (type
``~/eric6_venv/bin/python3 install-i18n.py``).

3. Running
----------
Just call up eric6, which will start the IDE. Use the "what is"-help
(arrow with ?) to get some help. The eric web site provides some
documents describing certain aspects of eric. To start the unit test module in
a standalone variant simply call up eric6_unittest. This will show the same
dialog (though with a little bit less functionality) as if started from within
eric6. The web browser can be started as a standalone program by executing the
eric6_browser script.

Please note, the first time you start eric6 it will recognize, that it
hasn't been configured yet, and will show the configuration dialog.
Please take your time and go through all the configuration items.
However, every configuration option has a meaningful default value.

4. Running from the sources
---------------------------
If you want to run eric6 from within the source tree you have to execute
the ``compileUiFiles.py`` script once after a fresh checkout from the source
repository or when new dialogs have been added. Thereafter just execute
the ``eric6.py`` script.

5. Tray starter
---------------
eric6 comes with a little utility called "eric6_tray". This embeds an icon
in the system tray, which contains a context menu to start eric6 and all
it's utilities. Double clicking this icon starts the eric6 IDE.

6. Completions/Calltips
-----------------------
eric6 provides an interface to the QScintilla completion and call-tips
functionality. QScintilla2 comes with API files for Python and itself. PyQt4
and PyQt5 contain API files as well. These are installed by default. An API
file for eric6 is installed in the same place, if installation variant 1 was
chosen.

In order to use completions and call-tips in eric6 please configure these
functions in the "Preferences Dialog" on the "Editor -> APIs", 
"Editor -> Autocompletion" and "Editor -> Calltips" pages.

Additional completions and call-tip providers are available through the eric6
plug-in system. See below for details.

7. Remote Debugger
------------------
In order to enable the remote debugger start eric6, open the preferences
dialog and configure the settings on the debugger pages.

The remote login must be possible without any further interaction (i.e.
no password prompt). If the remote setup differs from the local one you
must configure the Python interpreter and the Debug Client to be used
in the Preferences dialog. Use the ``install-debugclients.py`` script
to install the debug client files and set the entries of the a.m.
configuration page accordingly. 

To ease the installation process of the debug client, the eric6 sources
include the script ``install-debugclients.py``.

8. Passive Debugging
--------------------
Passive debugging mode allows the startup of the debugger from outside
of the IDE. The IDE waits for a connection attempt. For further details
see the file README-passive-debugging.rst.

9. Plug-in System
-----------------
eric6 contains a plug-in system, that is used to extend eric6's 
functionality. Some plug-ins are part of eric6. Additional plugins
are available via the Internet. Please use the built-in plug-in
repository dialog to get a list of available (official) plug-ins
and to download them. For more details about the plug-in system
please see the documentation area.

10. Interfaces to additional software packages
----------------------------------------------
At the moment eric6 provides interfaces to the following software
packages.

    Qt-Designer 
        This is part of the Qt distribution and is used to generate user
        interfaces.
    
    Qt-Linguist 
        This is part of the Qt distribution and is used to generate
        translations.
    
    Qt-Assistant 
        This is part of the Qt distribution and may be used to display help
        files.
    
    Mercurial
        This is a distributed version control system available from
        <https://www.mercurial-scm.org/>. It is the one used by eric6 itself.
    
    Git
        This is another (and probably more widely known) distributed version
        control system. It is available from <https://www.git-scm.com>.
    
    Subversion 
        This is a version control system available from
        <https://subversion.apache.org>. eric6 supports two different
        Subversion interfaces. One is using the svn command line tool, the
        other is using the PySvn Python interface
        <https://pysvn.sourceforge.io/>. The selection is done automatically
        depending on the installed software. The PySvn interface is preferred.
        This automatism can be overridden an a per project basis using the
        "User Properties" dialog.
    
    coverage.py 
        This is a tool to check Python code coverage. A slightly modified
        version is part of the eric6 distribution. The original version is
        available from
        <http://www.nedbatchelder.com/code/modules/coverage.html>
    
    profile 
        This is part of the standard Python distribution and is used to profile
        Python source code.

11. Internationalization
------------------------
eric6 and its tools are prepared to show the UI in different languages, which
can be configured via the preferences dialog. The Qt and QScintilla
translations are searched in the translations directory given in the
preferences dialog (Qt page). If the translations cannot be found, some part
of the HMI might show English texts even if you have selected something else.
If you are missing eric6 translations for your language and are willing to
volunteer for this work please send me an email naming the country code and
I will send you the respective Qt-Linguist file.

12. Window Layout
-----------------
eric6 provides a configurable window layout. The visibility of the various tool
panes can be configured. The position of the shell pane may be configured as
well.

13. Source code documentation
-----------------------------
eric6 has a built in source code documentation generator, which is
usable via the command line as well. For further details please see
the file README-eric6-doc.rst.

14. Included Tools
------------------
eric6 comes with a long list of tools. These can be started via the eric6
tray starter or directly via the command line. They are available from within
the IDE. The included tools are (sorted alphabetically):

  * **eric6_api.py**

    This is the tool to generate API files from Python source code.

  * **eric6_browser.py**

    This is the eric6 web browser. It is a full blown browser based on
    QtWebEngine, which is based on the Chromium web engine.

  * **eric6_compare.py**

    This tool may be used to compare two files side-by-side. Differences
    between the files are highlighted by coloring the text.

  * **eric6_configure.py**

    This is the standalone variant of the configuration dialog. It offers
    most of the configuration options as are available from within eric6.

  * **eric6_diff.py**

    This tool may be used to view the differences between two files. These
    are shown as a unified or context diff.

  * **eric6_doc.py**

    This is the tool to extract source code documentation from source files
    and format that as HTML files.

  * **eric6_editor.py**

    This is a stripped down, standalone variant of the editor embedded in the
    eric6 IDE.

  * **eric6_hexeditor.py**

    This is a standalone hex editor to work with binary files.

  * **eric6_iconeditor.py**

    This is a little tool to create pixel based icons and save them in a
    pixmap format.

  * **eric6_plugininstall.py**

    This is a standalone utility to install eric6 plug-ins available on the
    local machine.

  * **eric6_pluginrepository.py**

    This is a standalone variant of the plug-in repository window. It is used
    to view the available plug-ins and download them to the local machine.

  * **eric6_pluginuninstall.py**

    This is a standalone utility to uninstall eric6 plug-ins.

  * **eric6_qregularexpression.py**

    This tool may be used to create regular expressions based on
    QRegularExpression.

  * **eric6_re.py**

    This tool may be used to create Python regular expressions as used with the
    re module.

  * **eric6_shell.py**

    This is a standalone, graphical Python shell application.

  * **eric6_snap.py**

    This tool may be used to create screenshots of the whole screen, individual
    windows or selectable areas.

  * **eric6_sqlbrowser.py**

    This is a simple tool to inspect SQL databases. All database products
    supported by Qt may be inspected. Note, that Qt database drivers may be
    installed first.

  * **eric6_tray.py**

    This is the tray starter application. See above for some details.

  * **eric6_trpreviewer**

    This tool may be used to preview translations of Qt forms. Forms and
    language files may be loaded separately. Multiple languages can be loaded
    and the active language can be switched between the loaded ones.

  * **eric6_uipreviewer**

    This tool is used to preview Qt forms. The display may be switched between
    the available Qt window styles.

  * **eric6_unittest**

    This is a standalone tool to execute existing unit tests.

14. License
-----------
eric6 (and the others) is released under the conditions of the GPLv3. See 
separate license file ``LICENSE.GPL3`` for more details. Third party software
included in eric6 is released under their respective license and contained in
the eric6 distribution for convenience. 

15. Bugs and other reports
--------------------------
Please send bug reports, feature requests or contributions to eric bugs
address. After the IDE is installed you can use the "Report Bug..."
entry of the Help menu, which will send an email to
<eric-bugs@eric-ide.python-projects.org>. To request a new feature use the
"Request Feature..." entry of the Help menu, which will send an email to
<eric-featurerequest@eric-ide.python-projects.org>.

Alternatively bugs may be reported via the eric6 issue tracker at 
<https://tracker.die-offenbachs.homelinux.org/>.
