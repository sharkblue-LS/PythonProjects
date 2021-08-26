# -*- coding: utf-8 -*-

# Copyright (c) 2008 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#


"""
Module implementing the helpbrowser using QWebView.
"""

from PyQt5.QtCore import (
    pyqtSlot, pyqtSignal, QUrl, QUrlQuery, QTimer, QEventLoop, QPoint, QPointF,
    QT_VERSION
)
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWebEngineWidgets import (
    QWebEnginePage, QWebEngineSettings, QWebEngineScript
)
try:
    from PyQt5.QtWebEngine import PYQT_WEBENGINE_VERSION
    # __IGNORE_EXCEPTION__
except (AttributeError, ImportError):
    PYQT_WEBENGINE_VERSION = QT_VERSION
from PyQt5.QtWebChannel import QWebChannel

try:
    from PyQt5.QtNetwork import QSslConfiguration, QSslCertificate
    SSL_AVAILABLE = True
except ImportError:
    SSL_AVAILABLE = False

from E5Gui import E5MessageBox

from WebBrowser.WebBrowserWindow import WebBrowserWindow

from .JavaScript.ExternalJsObject import ExternalJsObject

from .Tools.WebHitTestResult import WebHitTestResult
from .Tools import Scripts

import Preferences
import Globals


class WebBrowserPage(QWebEnginePage):
    """
    Class implementing an enhanced web page.
    
    @signal safeBrowsingAbort() emitted to indicate an abort due to a safe
        browsing event
    @signal safeBrowsingBad(threatType, threatMessages) emitted to indicate a
        malicious web site as determined by safe browsing
    @signal printPageRequested() emitted to indicate a print request of the
        shown web page
    @signal navigationRequestAccepted(url, navigation type, main frame) emitted
        to signal an accepted navigation request
    @signal sslConfigurationChanged() emitted to indicate a change of the
        stored SSL configuration data
    """
    SafeJsWorld = QWebEngineScript.ScriptWorldId.ApplicationWorld
    UnsafeJsWorld = QWebEngineScript.ScriptWorldId.MainWorld
    
    safeBrowsingAbort = pyqtSignal()
    safeBrowsingBad = pyqtSignal(str, str)
    
    printPageRequested = pyqtSignal()
    navigationRequestAccepted = pyqtSignal(QUrl, QWebEnginePage.NavigationType,
                                           bool)
    
    sslConfigurationChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent parent widget of this window (QWidget)
        """
        super(WebBrowserPage, self).__init__(
            WebBrowserWindow.webProfile(), parent)
        
        self.__printer = None
        self.__badSite = False
        self.__registerProtocolHandlerRequest = None
        
        self.featurePermissionRequested.connect(
            self.__featurePermissionRequested)
        self.authenticationRequired.connect(
            lambda url, auth: WebBrowserWindow.networkManager().authentication(
                url, auth, self))
        self.proxyAuthenticationRequired.connect(
            WebBrowserWindow.networkManager().proxyAuthentication)
        self.fullScreenRequested.connect(self.__fullScreenRequested)
        self.urlChanged.connect(self.__urlChanged)
        self.contentsSizeChanged.connect(self.__contentsSizeChanged)
        
        try:
            self.registerProtocolHandlerRequested.connect(
                self.__registerProtocolHandlerRequested)
        except AttributeError:
            # defined for Qt >= 5.11
            pass
        
        self.__sslConfiguration = None
        
        # Workaround for changing webchannel world inside
        # acceptNavigationRequest not working
        self.__channelUrl = QUrl()
        self.__channelWorldId = -1
        self.__setupChannelTimer = QTimer(self)
        self.__setupChannelTimer.setSingleShot(True)
        self.__setupChannelTimer.setInterval(100)
        self.__setupChannelTimer.timeout.connect(self.__setupChannelTimeout)
    
    @pyqtSlot()
    def __setupChannelTimeout(self):
        """
        Private slot to initiate the setup of the web channel.
        """
        self.__setupWebChannelForUrl(self.__channelUrl)
    
    def acceptNavigationRequest(self, url, type_, isMainFrame):
        """
        Public method to determine, if a request may be accepted.
        
        @param url URL to navigate to
        @type QUrl
        @param type_ type of the navigation request
        @type QWebEnginePage.NavigationType
        @param isMainFrame flag indicating, that the request originated from
            the main frame
        @type bool
        @return flag indicating acceptance
        @rtype bool
        """
        scheme = url.scheme()
        if scheme == "mailto":
            QDesktopServices.openUrl(url)
            return False
        
        # AdBlock
        if url.scheme() == "abp":
            if WebBrowserWindow.adBlockManager().addSubscriptionFromUrl(url):
                return False
        
        # GreaseMonkey
        try:
            # PyQtWebEngine >= 5.14.0
            navigationType = type_ in [
                QWebEnginePage.NavigationType.NavigationTypeLinkClicked,
                QWebEnginePage.NavigationType.NavigationTypeRedirect
            ]
        except AttributeError:
            navigationType = (
                type_ ==
                QWebEnginePage.NavigationType.NavigationTypeLinkClicked
            )
        if navigationType and url.toString().endswith(".user.js"):
            WebBrowserWindow.greaseMonkeyManager().downloadScript(url)
            return False
        
        if url.scheme() == "eric":
            if url.path() == "AddSearchProvider":
                query = QUrlQuery(url)
                self.view().mainWindow().openSearchManager().addEngine(
                    QUrl(query.queryItemValue("url")))
                return False
            elif url.path() == "PrintPage":
                self.printPageRequested.emit()
                return False
        
        # Safe Browsing
        self.__badSite = False
        from WebBrowser.SafeBrowsing.SafeBrowsingManager import (
            SafeBrowsingManager
        )
        if (
            SafeBrowsingManager.isEnabled() and
            url.scheme() not in SafeBrowsingManager.getIgnoreSchemes()
        ):
            threatLists = (
                WebBrowserWindow.safeBrowsingManager().lookupUrl(url)[0]
            )
            if threatLists:
                threatMessages = (
                    WebBrowserWindow.safeBrowsingManager()
                    .getThreatMessages(threatLists)
                )
                res = E5MessageBox.warning(
                    WebBrowserWindow.getWindow(),
                    self.tr("Suspicuous URL detected"),
                    self.tr("<p>The URL <b>{0}</b> was found in the Safe"
                            " Browsing database.</p>{1}").format(
                        url.toString(), "".join(threatMessages)),
                    E5MessageBox.StandardButtons(
                        E5MessageBox.Abort |
                        E5MessageBox.Ignore),
                    E5MessageBox.Abort)
                if res == E5MessageBox.Abort:
                    self.safeBrowsingAbort.emit()
                    return False
                
                self.__badSite = True
                threatType = (
                    WebBrowserWindow.safeBrowsingManager()
                    .getThreatType(threatLists[0])
                )
                self.safeBrowsingBad.emit(threatType, "".join(threatMessages))
        
        result = QWebEnginePage.acceptNavigationRequest(
            self, url, type_, isMainFrame)
        
        if result:
            if isMainFrame:
                isWeb = url.scheme() in ("http", "https", "ftp", "ftps",
                                         "file")
                globalJsEnabled = WebBrowserWindow.webSettings().testAttribute(
                    QWebEngineSettings.WebAttribute.JavascriptEnabled)
                if isWeb:
                    enable = globalJsEnabled
                else:
                    enable = True
                self.settings().setAttribute(
                    QWebEngineSettings.WebAttribute.JavascriptEnabled, enable)
                
                self.__channelUrl = url
                self.__setupChannelTimer.start()
            self.navigationRequestAccepted.emit(url, type_, isMainFrame)
        
        return result
    
    @pyqtSlot(QUrl)
    def __urlChanged(self, url):
        """
        Private slot to handle changes of the URL.
        
        @param url new URL
        @type QUrl
        """
        if (
            not url.isEmpty() and
            url.scheme() == "eric" and
            not self.isJavaScriptEnabled()
        ):
            self.settings().setAttribute(
                QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            self.triggerAction(QWebEnginePage.WebAction.Reload)
    
    @classmethod
    def userAgent(cls, resolveEmpty=False):
        """
        Class method to get the global user agent setting.
        
        @param resolveEmpty flag indicating to resolve an empty
            user agent (boolean)
        @return user agent string (string)
        """
        agent = Preferences.getWebBrowser("UserAgent")
        if agent == "" and resolveEmpty:
            agent = cls.userAgentForUrl(QUrl())
        return agent
    
    @classmethod
    def setUserAgent(cls, agent):
        """
        Class method to set the global user agent string.
        
        @param agent new current user agent string (string)
        """
        Preferences.setWebBrowser("UserAgent", agent)
    
    @classmethod
    def userAgentForUrl(cls, url):
        """
        Class method to determine the user agent for the given URL.
        
        @param url URL to determine user agent for (QUrl)
        @return user agent string (string)
        """
        agent = WebBrowserWindow.userAgentsManager().userAgentForUrl(url)
        if agent == "":
            # no agent string specified for the given host -> use global one
            agent = Preferences.getWebBrowser("UserAgent")
            if agent == "":
                # no global agent string specified -> use default one
                agent = WebBrowserWindow.webProfile().httpUserAgent()
        return agent
    
    def __featurePermissionRequested(self, url, feature):
        """
        Private slot handling a feature permission request.
        
        @param url url requesting the feature
        @type QUrl
        @param feature requested feature
        @type QWebEnginePage.Feature
        """
        manager = WebBrowserWindow.featurePermissionManager()
        manager.requestFeaturePermission(self, url, feature)
    
    def execJavaScript(self, script,
                       worldId=QWebEngineScript.ScriptWorldId.MainWorld,
                       timeout=500):
        """
        Public method to execute a JavaScript function synchroneously.
        
        @param script JavaScript script source to be executed
        @type str
        @param worldId ID to run the script under
        @type QWebEngineScript.ScriptWorldId
        @param timeout max. time the script is given to execute
        @type int
        @return result of the script
        @rtype depending upon script result
        """
        loop = QEventLoop()
        resultDict = {"res": None}
        QTimer.singleShot(timeout, loop.quit)
        
        def resultCallback(res, resDict=resultDict):
            if loop and loop.isRunning():
                resDict["res"] = res
                loop.quit()
        
        self.runJavaScript(script, worldId, resultCallback)
        
        loop.exec()
        return resultDict["res"]
    
    def runJavaScript(self, script, worldId=-1, callback=None):
        """
        Public method to run a script in the context of the page.
        
        @param script JavaScript script source to be executed
        @type str
        @param worldId ID to run the script under
        @type int
        @param callback callback function to be executed when the script has
            ended
        @type function
        """
        if worldId > -1:
            if callback is None:
                QWebEnginePage.runJavaScript(self, script, worldId)
            else:
                QWebEnginePage.runJavaScript(self, script, worldId, callback)
        else:
            if callback is None:
                QWebEnginePage.runJavaScript(self, script)
            else:
                QWebEnginePage.runJavaScript(self, script, callback)
    
    def isJavaScriptEnabled(self):
        """
        Public method to test, if JavaScript is enabled.
        
        @return flag indicating the state of the JavaScript support
        @rtype bool
        """
        return self.settings().testAttribute(
            QWebEngineSettings.WebAttribute.JavascriptEnabled)
    
    def scroll(self, x, y):
        """
        Public method to scroll by the given amount of pixels.
        
        @param x horizontal scroll value
        @type int
        @param y vertical scroll value
        @type int
        """
        self.runJavaScript(
            "window.scrollTo(window.scrollX + {0}, window.scrollY + {1})"
            .format(x, y),
            WebBrowserPage.SafeJsWorld
        )
    
    def scrollTo(self, pos):
        """
        Public method to scroll to the given position.
        
        @param pos position to scroll to
        @type QPointF
        """
        self.runJavaScript(
            "window.scrollTo({0}, {1});".format(pos.x(), pos.y()),
            WebBrowserPage.SafeJsWorld
        )
    
    def mapToViewport(self, pos):
        """
        Public method to map a position to the viewport.
        
        @param pos position to be mapped
        @type QPoint
        @return viewport position
        @rtype QPoint
        """
        return QPoint(pos.x() // self.zoomFactor(),
                      pos.y() // self.zoomFactor())
    
    def hitTestContent(self, pos):
        """
        Public method to test the content at a specified position.
        
        @param pos position to execute the test at
        @type QPoint
        @return test result object
        @rtype WebHitTestResult
        """
        return WebHitTestResult(self, pos)
    
    def __setupWebChannelForUrl(self, url):
        """
        Private method to setup a web channel to our external object.
        
        @param url URL for which to setup the web channel
        @type QUrl
        """
        channel = self.webChannel()
        if channel is None:
            channel = QWebChannel(self)
            ExternalJsObject.setupWebChannel(channel, self)
        
        worldId = -1
        if url.scheme() in ("eric", "qthelp"):
            worldId = self.UnsafeJsWorld
        else:
            worldId = self.SafeJsWorld
        if worldId != self.__channelWorldId:
            self.__channelWorldId = worldId
            try:
                self.setWebChannel(channel, self.__channelWorldId)
            except TypeError:
                # pre Qt 5.7.0
                self.setWebChannel(channel)
    
    def certificateError(self, error):
        """
        Public method to handle SSL certificate errors.
        
        @param error object containing the certificate error information
        @type QWebEngineCertificateError
        @return flag indicating to ignore this error
        @rtype bool
        """
        return WebBrowserWindow.networkManager().certificateError(
            error, self.view())
    
    def __fullScreenRequested(self, request):
        """
        Private slot handling a full screen request.
        
        @param request reference to the full screen request
        @type QWebEngineFullScreenRequest
        """
        self.view().requestFullScreen(request.toggleOn())
        
        accepted = request.toggleOn() == self.view().isFullScreen()
        
        if accepted:
            request.accept()
        else:
            request.reject()
    
    def execPrintPage(self, printer, timeout=1000):
        """
        Public method to execute a synchronous print.
        
        @param printer reference to the printer object
        @type QPrinter
        @param timeout timeout value in milliseconds
        @type int
        @return flag indicating a successful print job
        @rtype bool
        """
        loop = QEventLoop()
        resultDict = {"res": None}
        QTimer.singleShot(timeout, loop.quit)
        
        def printCallback(res, resDict=resultDict):
            if loop and loop.isRunning():
                resDict["res"] = res
                loop.quit()
        
        self.print(printer, printCallback)
        
        loop.exec()
        return resultDict["res"]
    
    def __contentsSizeChanged(self, size):
        """
        Private slot to work around QWebEnginePage not scrolling to anchors
        when opened in a background tab.
        
        @param size changed contents size (unused)
        @type QSize
        """
        fragment = self.url().fragment()
        self.runJavaScript(Scripts.scrollToAnchor(fragment))
    
    ##############################################
    ## Methods below deal with JavaScript messages
    ##############################################
    
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        """
        Public method to show a console message.
        
        @param level severity
        @type QWebEnginePage.JavaScriptConsoleMessageLevel
        @param message message to be shown
        @type str
        @param lineNumber line number of an error
        @type int
        @param sourceId source URL causing the error
        @type str
        """
        self.view().mainWindow().javascriptConsole().javaScriptConsoleMessage(
            level, message, lineNumber, sourceId)
    
    ###########################################################################
    ## Methods below implement safe browsing related functions
    ###########################################################################
    
    def getSafeBrowsingStatus(self):
        """
        Public method to get the safe browsing status of the current page.
        
        @return flag indicating a safe site
        @rtype bool
        """
        return not self.__badSite
    
    ##################################################
    ## Methods below implement compatibility functions
    ##################################################
    
    if not hasattr(QWebEnginePage, "icon"):
        def icon(self):
            """
            Public method to get the web site icon.
            
            @return web site icon
            @rtype QIcon
            """
            return self.view().icon()
    
    if not hasattr(QWebEnginePage, "scrollPosition"):
        def scrollPosition(self):
            """
            Public method to get the scroll position of the web page.
            
            @return scroll position
            @rtype QPointF
            """
            pos = self.execJavaScript(
                "(function() {"
                "var res = {"
                "    x: 0,"
                "    y: 0,"
                "};"
                "res.x = window.scrollX;"
                "res.y = window.scrollY;"
                "return res;"
                "})()",
                WebBrowserPage.SafeJsWorld
            )
            if pos is not None:
                pos = QPointF(pos["x"], pos["y"])
            else:
                pos = QPointF(0.0, 0.0)
            
            return pos
    
    #############################################################
    ## Methods below implement protocol handler related functions
    #############################################################
    
    try:
        @pyqtSlot("QWebEngineRegisterProtocolHandlerRequest")
        def __registerProtocolHandlerRequested(self, request):
            """
            Private slot to handle the registration of a custom protocol
            handler.
            
            @param request reference to the registration request
            @type QWebEngineRegisterProtocolHandlerRequest
            """
            from PyQt5.QtWebEngineCore import (
                QWebEngineRegisterProtocolHandlerRequest
            )
            
            if self.__registerProtocolHandlerRequest:
                del self.__registerProtocolHandlerRequest
                self.__registerProtocolHandlerRequest = None
            self.__registerProtocolHandlerRequest = (
                QWebEngineRegisterProtocolHandlerRequest(request)
            )
    except TypeError:
        # this is supported with Qt 5.12 and later
        pass
    
    def registerProtocolHandlerRequestUrl(self):
        """
        Public method to get the registered protocol handler request URL.
        
        @return registered protocol handler request URL
        @rtype QUrl
        """
        if (
            self.__registerProtocolHandlerRequest and
            (self.url().host() ==
             self.__registerProtocolHandlerRequest.origin().host())
        ):
            return self.__registerProtocolHandlerRequest.origin()
        else:
            return QUrl()
    
    def registerProtocolHandlerRequestScheme(self):
        """
        Public method to get the registered protocol handler request scheme.
        
        @return registered protocol handler request scheme
        @rtype str
        """
        if (
            self.__registerProtocolHandlerRequest and
            (self.url().host() ==
             self.__registerProtocolHandlerRequest.origin().host())
        ):
            return self.__registerProtocolHandlerRequest.scheme()
        else:
            return ""
    
    #############################################################
    ## SSL configuration handling below
    #############################################################
    
    def setSslConfiguration(self, sslConfiguration):
        """
        Public slot to set the SSL configuration data of the page.
        
        @param sslConfiguration SSL configuration to be set
        @type QSslConfiguration
        """
        self.__sslConfiguration = QSslConfiguration(sslConfiguration)
        self.__sslConfiguration.url = self.url()
        self.sslConfigurationChanged.emit()
    
    def getSslConfiguration(self):
        """
        Public method to return a reference to the current SSL configuration.
        
        @return reference to the SSL configuration in use
        @rtype QSslConfiguration
        """
        return self.__sslConfiguration
    
    def clearSslConfiguration(self):
        """
        Public slot to clear the stored SSL configuration data.
        """
        self.__sslConfiguration = None
        self.sslConfigurationChanged.emit()
    
    def getSslCertificate(self):
        """
        Public method to get a reference to the SSL certificate.
        
        @return amended SSL certificate
        @rtype QSslCertificate
        """
        if self.__sslConfiguration is None:
            return None
        
        sslCertificate = self.__sslConfiguration.peerCertificate()
        sslCertificate.url = QUrl(self.__sslConfiguration.url)
        return sslCertificate
    
    def getSslCertificateChain(self):
        """
        Public method to get a reference to the SSL certificate chain.
        
        @return SSL certificate chain
        @rtype list of QSslCertificate
        """
        if self.__sslConfiguration is None:
            return []
        
        chain = self.__sslConfiguration.peerCertificateChain()
        return chain
    
    def showSslInfo(self, pos):
        """
        Public slot to show some SSL information for the loaded page.
        
        @param pos position to show the info at
        @type QPoint
        """
        if SSL_AVAILABLE and self.__sslConfiguration is not None:
            from E5Network.E5SslInfoWidget import E5SslInfoWidget
            widget = E5SslInfoWidget(self.url(), self.__sslConfiguration,
                                     self.view())
            widget.showAt(pos)
        else:
            E5MessageBox.warning(
                self.view(),
                self.tr("SSL Info"),
                self.tr("""This site does not contain SSL information."""))
    
    def hasValidSslInfo(self):
        """
        Public method to check, if the page has a valid SSL certificate.
        
        @return flag indicating a valid SSL certificate
        @rtype bool
        """
        if self.__sslConfiguration is None:
            return False
        
        certList = self.__sslConfiguration.peerCertificateChain()
        if not certList:
            return False
        
        certificateDict = Globals.toDict(
            Preferences.Prefs.settings.value("Ssl/CaCertificatesDict"))
        for server in certificateDict:
            localCAList = QSslCertificate.fromData(certificateDict[server])
            for cert in certList:
                if cert in localCAList:
                    return True
        
        for cert in certList:
            if cert.isBlacklisted():
                return False
        
        return True
