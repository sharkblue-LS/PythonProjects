# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the snapshot widget.
"""

#
# SnapWidget and its associated modules are PyQt5 ports of Ksnapshot.
#

import os
import re

from PyQt5.QtCore import (
    pyqtSlot, Qt, QFile, QFileInfo, QTimer, QPoint, QMimeData, QLocale,
    QStandardPaths
)
from PyQt5.QtGui import QImageWriter, QPixmap, QDrag, QKeySequence
from PyQt5.QtWidgets import QWidget, QApplication, QShortcut

from E5Gui import E5FileDialog, E5MessageBox

from .Ui_SnapWidget import Ui_SnapWidget

import UI.PixmapCache
import Preferences
import Globals

from .SnapshotModes import SnapshotModes


class SnapWidget(QWidget, Ui_SnapWidget):
    """
    Class implementing the snapshot widget.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(SnapWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.saveButton.setIcon(UI.PixmapCache.getIcon("fileSaveAs"))
        self.takeButton.setIcon(UI.PixmapCache.getIcon("cameraPhoto"))
        self.copyButton.setIcon(UI.PixmapCache.getIcon("editCopy"))
        self.copyPreviewButton.setIcon(UI.PixmapCache.getIcon("editCopy"))
        self.setWindowIcon(UI.PixmapCache.getIcon("ericSnap"))
        
        if Globals.isWaylandSession():
            from .SnapshotWaylandGrabber import SnapshotWaylandGrabber
            self.__grabber = SnapshotWaylandGrabber(self)
        else:
            from .SnapshotDefaultGrabber import SnapshotDefaultGrabber
            self.__grabber = SnapshotDefaultGrabber(self)
            self.decorationsCheckBox.hide()
            self.mouseCursorCheckBox.hide()
        self.__grabber.grabbed.connect(self.__captured)
        supportedModes = self.__grabber.supportedModes()
        
        if SnapshotModes.Fullscreen in supportedModes:
            self.modeCombo.addItem(self.tr("Fullscreen"),
                                   SnapshotModes.Fullscreen)
        if SnapshotModes.SelectedScreen in supportedModes:
            if len(QApplication.screens()) > 1:
                self.modeCombo.addItem(self.tr("Select Screen"),
                                       SnapshotModes.SelectedScreen)
        if SnapshotModes.SelectedWindow in supportedModes:
            self.modeCombo.addItem(self.tr("Select Window"),
                                   SnapshotModes.SelectedWindow)
        if SnapshotModes.Rectangle in supportedModes:
            self.modeCombo.addItem(self.tr("Rectangular Selection"),
                                   SnapshotModes.Rectangle)
        if SnapshotModes.Ellipse in supportedModes:
            self.modeCombo.addItem(self.tr("Elliptical Selection"),
                                   SnapshotModes.Ellipse)
        if SnapshotModes.Freehand in supportedModes:
            self.modeCombo.addItem(self.tr("Freehand Selection"),
                                   SnapshotModes.Freehand)
        mode = int(Preferences.Prefs.settings.value("Snapshot/Mode", 0))
        index = self.modeCombo.findData(SnapshotModes(mode))
        if index == -1:
            index = 0
        self.modeCombo.setCurrentIndex(index)
        
        delay = int(Preferences.Prefs.settings.value("Snapshot/Delay", 0))
        self.delaySpin.setValue(delay)
        
        picturesLocation = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.PicturesLocation)
        self.__filename = Preferences.Prefs.settings.value(
            "Snapshot/Filename",
            os.path.join(picturesLocation,
                         self.tr("snapshot") + "1.png"))
        
        self.__snapshot = QPixmap()
        self.__savedPosition = QPoint()
        self.__modified = False
        self.__locale = QLocale()
        
        self.__initFileFilters()
        self.__initShortcuts()
        
        self.preview.startDrag.connect(self.__dragSnapshot)
        
        self.__updateTimer = QTimer()
        self.__updateTimer.setSingleShot(True)
        self.__updateTimer.timeout.connect(self.__updatePreview)
        
        self.__updateCaption()
        self.takeButton.setFocus()
    
    def __initFileFilters(self):
        """
        Private method to define the supported image file filters.
        """
        filters = {
            'bmp': self.tr("Windows Bitmap File (*.bmp)"),
            'gif': self.tr("Graphic Interchange Format File (*.gif)"),
            'ico': self.tr("Windows Icon File (*.ico)"),
            'jpg': self.tr("JPEG File (*.jpg)"),
            'mng': self.tr("Multiple-Image Network Graphics File (*.mng)"),
            'pbm': self.tr("Portable Bitmap File (*.pbm)"),
            'pcx': self.tr("Paintbrush Bitmap File (*.pcx)"),
            'pgm': self.tr("Portable Graymap File (*.pgm)"),
            'png': self.tr("Portable Network Graphics File (*.png)"),
            'ppm': self.tr("Portable Pixmap File (*.ppm)"),
            'sgi': self.tr("Silicon Graphics Image File (*.sgi)"),
            'svg': self.tr("Scalable Vector Graphics File (*.svg)"),
            'tga': self.tr("Targa Graphic File (*.tga)"),
            'tif': self.tr("TIFF File (*.tif)"),
            'xbm': self.tr("X11 Bitmap File (*.xbm)"),
            'xpm': self.tr("X11 Pixmap File (*.xpm)"),
        }
        
        outputFormats = []
        writeFormats = QImageWriter.supportedImageFormats()
        for writeFormat in writeFormats:
            try:
                outputFormats.append(filters[bytes(writeFormat).decode()])
            except KeyError:
                pass
        outputFormats.sort()
        self.__outputFilter = ';;'.join(outputFormats)
        
        self.__defaultFilter = filters['png']
    
    def __initShortcuts(self):
        """
        Private method to initialize the keyboard shortcuts.
        """
        self.__quitShortcut = QShortcut(
            QKeySequence(QKeySequence.StandardKey.Quit), self, self.close)
        
        self.__copyShortcut = QShortcut(
            QKeySequence(QKeySequence.StandardKey.Copy), self,
            self.copyButton.animateClick)
        
        self.__quickSaveShortcut = QShortcut(
            QKeySequence(Qt.Key.Key_Q), self, self.__quickSave)
        
        self.__save1Shortcut = QShortcut(
            QKeySequence(QKeySequence.StandardKey.Save), self,
            self.saveButton.animateClick)
        self.__save2Shortcut = QShortcut(
            QKeySequence(Qt.Key.Key_S), self, self.saveButton.animateClick)
        
        self.__grab1Shortcut = QShortcut(
            QKeySequence(QKeySequence.StandardKey.New),
            self, self.takeButton.animateClick)
        self.__grab2Shortcut = QShortcut(
            QKeySequence(Qt.Key.Key_N), self, self.takeButton.animateClick)
        self.__grab3Shortcut = QShortcut(
            QKeySequence(Qt.Key.Key_Space), self, self.takeButton.animateClick)
    
    def __quickSave(self):
        """
        Private slot to save the snapshot bypassing the file selection dialog.
        """
        if not self.__snapshot.isNull():
            while os.path.exists(self.__filename):
                self.__autoIncFilename()
            
            if self.__saveImage(self.__filename):
                self.__modified = False
                self.__autoIncFilename()
                self.__updateCaption()
    
    @pyqtSlot()
    def on_saveButton_clicked(self):
        """
        Private slot to save the snapshot.
        """
        if not self.__snapshot.isNull():
            while os.path.exists(self.__filename):
                self.__autoIncFilename()
            
            fileName, selectedFilter = E5FileDialog.getSaveFileNameAndFilter(
                self,
                self.tr("Save Snapshot"),
                self.__filename,
                self.__outputFilter,
                self.__defaultFilter,
                E5FileDialog.Options(E5FileDialog.DontConfirmOverwrite))
            if not fileName:
                return
            
            ext = QFileInfo(fileName).suffix()
            if not ext:
                ex = selectedFilter.split("(*")[1].split(")")[0]
                if ex:
                    fileName += ex
            
            if self.__saveImage(fileName):
                self.__modified = False
                self.__filename = fileName
                self.__autoIncFilename()
                self.__updateCaption()
    
    def __saveImage(self, fileName):
        """
        Private method to save the snapshot.
        
        @param fileName name of the file to save to (string)
        @return flag indicating success (boolean)
        """
        if QFileInfo(fileName).exists():
            res = E5MessageBox.yesNo(
                self,
                self.tr("Save Snapshot"),
                self.tr("<p>The file <b>{0}</b> already exists."
                        " Overwrite it?</p>").format(fileName),
                icon=E5MessageBox.Warning)
            if not res:
                return False
        
        file = QFile(fileName)
        if not file.open(QFile.WriteOnly):
            E5MessageBox.warning(
                self, self.tr("Save Snapshot"),
                self.tr("Cannot write file '{0}:\n{1}.")
                .format(fileName, file.errorString()))
            return False
        
        ok = self.__snapshot.save(file)
        file.close()
        
        if not ok:
            E5MessageBox.warning(
                self, self.tr("Save Snapshot"),
                self.tr("Cannot write file '{0}:\n{1}.")
                .format(fileName, file.errorString()))
        
        return ok
    
    def __autoIncFilename(self):
        """
        Private method to auto-increment the file name.
        """
        # Extract the file name
        name = os.path.basename(self.__filename)
        
        # If the name contains a number, then increment it.
        numSearch = re.compile("(^|[^\\d])(\\d+)")
        # We want to match as far left as possible, and when the number is
        # at the start of the name.
        
        # Does it have a number?
        matches = list(numSearch.finditer(name))
        if matches:
            # It has a number, increment it.
            match = matches[-1]
            start = match.start(2)
            # Only the second group is of interest.
            numAsStr = match.group(2)
            number = "{0:0{width}d}".format(
                int(numAsStr) + 1, width=len(numAsStr))
            name = name[:start] + number + name[start + len(numAsStr):]
        else:
            # no number
            start = name.rfind('.')
            if start != -1:
                # has a '.' somewhere, e.g. it has an extension
                name = name[:start] + '-1' + name[start:]
            else:
                # no extension, just tack it on to the end
                name += '-1'
        
        self.__filename = os.path.join(os.path.dirname(self.__filename), name)
        self.__updateCaption()
    
    @pyqtSlot()
    def on_takeButton_clicked(self):
        """
        Private slot to take a snapshot.
        """
        self.__savedPosition = self.pos()
        self.hide()
        
        self.__grabber.grab(
            self.modeCombo.itemData(self.modeCombo.currentIndex()),
            self.delaySpin.value(),
            self.mouseCursorCheckBox.isChecked(),
            self.decorationsCheckBox.isChecked(),
        )
    
    def __redisplay(self):
        """
        Private method to redisplay the window.
        """
        self.__updatePreview()
        if not self.__savedPosition.isNull():
            self.move(self.__savedPosition)
        self.show()
        self.raise_()
        
        self.saveButton.setEnabled(not self.__snapshot.isNull())
        self.copyButton.setEnabled(not self.__snapshot.isNull())
        self.copyPreviewButton.setEnabled(not self.__snapshot.isNull())
    
    @pyqtSlot()
    def on_copyButton_clicked(self):
        """
        Private slot to copy the snapshot to the clipboard.
        """
        if not self.__snapshot.isNull():
            QApplication.clipboard().setPixmap(QPixmap(self.__snapshot))
    
    @pyqtSlot()
    def on_copyPreviewButton_clicked(self):
        """
        Private slot to copy the snapshot preview to the clipboard.
        """
        QApplication.clipboard().setPixmap(self.preview.pixmap())
    
    def __captured(self, pixmap):
        """
        Private slot to show a preview of the snapshot.
        
        @param pixmap pixmap of the snapshot (QPixmap)
        """
        self.__snapshot = QPixmap(pixmap)
        
        self.__redisplay()
        self.__modified = not pixmap.isNull()
        self.__updateCaption()
    
    def __updatePreview(self):
        """
        Private slot to update the preview picture.
        """
        self.preview.setToolTip(self.tr(
            "Preview of the snapshot image ({0} x {1})").format(
            self.__locale.toString(self.__snapshot.width()),
            self.__locale.toString(self.__snapshot.height()))
        )
        self.preview.setPreview(self.__snapshot)
        self.preview.adjustSize()
    
    def resizeEvent(self, evt):
        """
        Protected method handling a resizing of the window.
        
        @param evt resize event (QResizeEvent)
        """
        self.__updateTimer.start(200)
    
    def __dragSnapshot(self):
        """
        Private slot handling the dragging of the preview picture.
        """
        drag = QDrag(self)
        mimeData = QMimeData()
        mimeData.setImageData(self.__snapshot)
        drag.setMimeData(mimeData)
        drag.setPixmap(self.preview.pixmap())
        drag.exec(Qt.DropAction.CopyAction)
    
    def closeEvent(self, evt):
        """
        Protected method handling the close event.
        
        @param evt close event (QCloseEvent)
        """
        if self.__modified:
            res = E5MessageBox.question(
                self,
                self.tr("eric Snapshot"),
                self.tr(
                    """The application contains an unsaved snapshot."""),
                E5MessageBox.StandardButtons(
                    E5MessageBox.Abort |
                    E5MessageBox.Discard |
                    E5MessageBox.Save))
            if res == E5MessageBox.Abort:
                evt.ignore()
                return
            elif res == E5MessageBox.Save:
                self.on_saveButton_clicked()
        
        Preferences.Prefs.settings.setValue(
            "Snapshot/Delay", self.delaySpin.value())
        modeData = self.modeCombo.itemData(self.modeCombo.currentIndex())
        if modeData is not None:
            Preferences.Prefs.settings.setValue(
                "Snapshot/Mode",
                modeData.value)
        Preferences.Prefs.settings.setValue(
            "Snapshot/Filename", self.__filename)
        Preferences.Prefs.settings.sync()
    
    def __updateCaption(self):
        """
        Private method to update the window caption.
        """
        self.setWindowTitle("{0}[*] - {1}".format(
            os.path.basename(self.__filename),
            self.tr("eric Snapshot")))
        self.setWindowModified(self.__modified)
        self.pathNameEdit.setText(os.path.dirname(self.__filename))
    
    @pyqtSlot(int)
    def on_modeCombo_currentIndexChanged(self, index):
        """
        Private slot handling the selection of a screenshot mode.
        
        @param index index of the selection
        @type int
        """
        isWindowMode = False
        if index >= 0:
            mode = self.modeCombo.itemData(index)
            isWindowMode = (mode == SnapshotModes.SelectedWindow)
        
        self.decorationsCheckBox.setEnabled(isWindowMode)
        self.decorationsCheckBox.setChecked(isWindowMode)
