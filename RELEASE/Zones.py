import sys
import os
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QPushButton, QWidget, QApplication, QWidget, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QLineEdit, QLineEdit, QWidget, QDesktopWidget,
                             QLabel, QListWidget, QListWidgetItem)

from functools import partial

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Zones'
        self.width = 1280
        self.height = 900

        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)

        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.center()

        #set colors
        self.setStyleSheet("background-color: #2d2d2d; color: #ffffff; font-size: 20px;")
    
        # Settings
        settingsLayout = QHBoxLayout()

        #describtion text
        layout.addWidget(Describtion("Zone edit", self))

        # variables

        self.label = QLabel(self)
        self.label.setText("Client: ")
        settingsLayout.addWidget(self.label)
        self.EditInputC = QLineEdit(self)
        settingsLayout.addWidget(self.EditInputC)

        self.label = QLabel(self)
        self.label.setText("Zone ID: ")
        settingsLayout.addWidget(self.label)
        self.EditInputZ = QLineEdit(self)
        settingsLayout.addWidget(self.EditInputZ)

        layout.addLayout(settingsLayout)

        # launch button
        self.buttonEdit = QPushButton('Launch', self)
        self.buttonEdit.setStyleSheet("background-color: #3d3d3d; color: #ffffff;font-size: 20px;")
        self.buttonEdit.setMinimumHeight(40)
        layout.addWidget(self.buttonEdit)
        self.buttonEdit.clicked.connect(self.onZoneEdit)

        # Extract list
        extractLayout = QHBoxLayout()

        #describtion text
        layout.addWidget(Describtion("Zone extract", self))

        #variables

        self.label = QLabel(self)
        self.label.setText("Client: ")
        extractLayout.addWidget(self.label)
        self.ExtractInputC = QLineEdit(self)
        extractLayout.addWidget(self.ExtractInputC)

        self.label = QLabel(self)
        self.label.setText("Zone ID: ")
        extractLayout.addWidget(self.label)
        self.ExtractInputZ = QLineEdit(self)
        extractLayout.addWidget(self.ExtractInputZ)

        self.label = QLabel(self)
        self.label.setText("Target Dir: ")
        extractLayout.addWidget(self.label)
        self.ExtractInputT = QLineEdit(self)
        extractLayout.addWidget(self.ExtractInputT)

        layout.addLayout(extractLayout)

        # launch button
        self.buttonExtract = QPushButton('Launch', self)
        self.buttonExtract.setStyleSheet("background-color: #3d3d3d; color: #ffffff;font-size: 20px;")
        self.buttonExtract.setMinimumHeight(40)
        layout.addWidget(self.buttonExtract)
        self.buttonExtract.clicked.connect(self.onExtractZone)

        # Models paths
        modelsLayout = QHBoxLayout()

        #describtion text
        layout.addWidget(Describtion("Models paths", self))

        # input text box with a plus botton next to it
        self.EditInputM = QLineEdit(self)
        modelsLayout.addWidget(self.EditInputM)

        self.buttonM = QPushButton('+', self)
        self.buttonM.setStyleSheet("background-color: #3d3d3d; color: #ffffff;font-size: 20px;")
        self.buttonM.setMinimumHeight(40)
        modelsLayout.addWidget(self.buttonM)
        self.buttonM.clicked.connect(self.onListAdd)

        layout.addLayout(modelsLayout)

        # list of already added paths with an option to delete and edit them
        self.listWidget = QListWidget(self)
        self.listWidget.setStyleSheet("background-color: #3d3d3d; color: #ffffff;font-size: 20px;")
        layout.addWidget(self.listWidget)
        self.loadList()

        # save button
        self.buttonSave = QPushButton('Save', self)
        self.buttonSave.setStyleSheet("background-color: #3d3d3d; color: #ffffff;font-size: 20px;")
        self.buttonSave.setMinimumHeight(40)
        layout.addWidget(self.buttonSave)
        self.buttonSave.clicked.connect(self.onSave)

        self.setLayout(layout)
        self.loadSettings()

        self.show()
    
    def center(self):
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())

    def loadList(self):
        with open("../HMapEdit/Tools/GameData.cs", "r") as f:
            for line in f:
                if "NIFFolders {" in line:
                    for line in f:
                        if "get {" in line:
                            for line in f:
                                if "}" in line:
                                    break
                                else:
                                    self.addToList(self.getPath(line))
    def getPath(self, line):
        line = line.split('"')
        path = ""
        for i in range(1, len(line)-1):
            path += line[i].replace(", ", "/")
        return path
    def loadSettings(self):
        with open("settings.cmd", "r") as f:
            for line in f:
                if "set CLIENT=" in line:
                    self.EditInputC.setText(line.split("=")[1])
                    self.ExtractInputC.setText(line.split("=")[1])
                if "set ZONE_ID=" in line:
                    self.EditInputZ.setText(line.split("=")[1])
                    self.ExtractInputZ.setText(line.split("=")[1])
                if "set TARGET_DIR=" in line:
                    self.ExtractInputT.setText(line.split("=")[1])
    @pyqtSlot()
    def onZoneEdit(self):
        #load all previous lines from settings
        with open("settings.cmd", "r") as f:
            lines = f.readlines()

        #edit set variables in settings.cmd
        with open("settings.cmd", "w") as f:
            f.write("@echo off\n")
            f.write("set CLIENT=" + self.EditInputC.text() + "\n")
            f.write("set ZONE_ID=" + self.EditInputZ.text() + "\n")
            #add lines that are not already in settings
            for line in lines:
                if "echo off" not in line and "set CLIENT=" not in line and "set ZONE_ID=" not in line:
                    f.write(line)
        #run start_zoeedit.bat
        os.system("start_zoneedit.bat")
        self.loadSettings()
    @pyqtSlot()
    def onExtractZone(self):
        #load all previous lines from settings
        with open("settings.cmd", "r") as f:
            lines = f.readlines()
        #edit set variables in settings.cmd
        with open("settings.cmd", "w") as f:
            f.write("@echo off\n")
            f.write("set CLIENT=" + self.ExtractInputC.text() + "\n")
            f.write("set ZONE_ID=" + self.ExtractInputZ.text() + "\n")
            f.write("set TARGET_DIR=" + self.ExtractInputT.text() + "\n")
            #add lines that are not already in settings
            for line in lines:
                if "echo off" not in line and "set CLIENT=" not in line and "set ZONE_ID=" not in line and "set TARGET_DIR=" not in line:
                    f.write(line)
        #run start_zoeedit.bat
        os.system("extract_zone.bat")
        self.loadSettings()
    @pyqtSlot()
    def onSave(self):
        with open("../HMapEdit/Tools/GameData.cs", "r") as f:
            #clean lines used in loadList and add paths like:  yield return Path.Combine("zones", "nifs"); 
            lines = f.readlines()
            for i in range(len(lines)):
                if "NIFFolders {" in lines[i]:
                    for j in range(i+1, len(lines)):
                        if "get {" in lines[j]:
                            for k in range(j+1, len(lines)):
                                if "}" in lines[k]:
                                    break
                                else:
                                    lines[k] = ""
            #add paths
            for i in range(len(lines)):
                if "NIFFolders {" in lines[i]:
                    for j in range(i+1, len(lines)):
                        if "get {" in lines[j]:
                            for k in range(self.listWidget.count()):
                                text = self.listWidget.itemWidget(self.listWidget.item(self.listWidget.count()-1-k)).children()[0].itemAt(0).widget().text()
                                lines.insert(j+k+1, 'yield return Path.Combine("'+ text.replace("/", '", "')+'");\n')
            #save to file
            with open("../HMapEdit/Tools/GameData.cs", "w") as f:
                for line in lines:
                    f.write(line)
    @pyqtSlot()
    def onListAdd(self):
        self.addToList(self.EditInputM.text())
        self.EditInputM.setText("")

    def addToList(self, text):
        item = QListWidgetItem()
        item_widget = QWidget()
        line_text = QLineEdit(text)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        line_push_button = QPushButton("X")
        line_push_button.setMaximumWidth(30)
        line_push_button.clicked.connect(partial(self.deleteFromList, item))
        item_layout = QHBoxLayout()
        item_layout.addWidget(line_text)
        item_layout.addWidget(line_push_button)
        item_widget.setLayout(item_layout)
        item.setSizeHint(item_widget.sizeHint())
        self.listWidget.insertItem(0, item)
        self.listWidget.setItemWidget(item, item_widget)

    def deleteFromList(self, who):
        self.listWidget.takeItem(self.listWidget.row(who))

class Describtion(QLabel):
    def __init__(self, text, parent=None):
        super(Describtion, self).__init__(parent)
        self.setText(text)
        self.setStyleSheet("font-weight: bold;")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())