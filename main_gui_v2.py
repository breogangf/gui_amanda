import sys
from pathlib import Path
from dotenv import load_dotenv
from PyQt6.QtCore import QSize, Qt, QStringListModel, QDir
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QBoxLayout, QWidget, QFileDialog, QPlainTextEdit
from PyQt6 import QtCore, QtGui, QtWidgets

env_variables_path = Path(__file__).resolve().with_name(".env")
load_dotenv(dotenv_path=env_variables_path)

from src.setup_logger import logger
from src.assets import Assets
from src.jobs import Jobs
from src.utils import get_workflow_by_name




class Ui_MainWindow(object):

    def __init__(self):
        self.selectedFile = None
        self.asset = None
        self.job = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(931, 545)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(290, 80, 289, 239))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.selectedButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.selectedButton.setObjectName("pushButton")
        self.selectedButton.clicked.connect(self.getFiles)
        self.verticalLayout.addWidget(self.selectedButton)
        self.listView = QtWidgets.QListView(self.verticalLayoutWidget)
        self.listView.setEnabled(True)
        self.listView.setObjectName("listView")
        self.verticalLayout.addWidget(self.listView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.uploadButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.uploadButton.setObjectName("pushButtonUpload")
        self.uploadButton.setEnabled(False)
        self.uploadButton.clicked.connect(self.upload)
        self.horizontalLayout.addWidget(self.uploadButton)
        self.processButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.processButton.setEnabled(False)
        self.processButton.setObjectName("pushButton_2")
        self.processButton.clicked.connect(self.process)
        self.horizontalLayout.addWidget(self.processButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(810, 30, 103, 32))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.workflowLabel = QtWidgets.QLabel(self.centralwidget)
        self.workflowLabel.setGeometry(QtCore.QRect(750, 40, 58, 16))
        self.workflowLabel.setObjectName("label")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 370, 911, 131))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.textArea = QtWidgets.QPlainTextEdit()
        self.textArea.setGeometry(QtCore.QRect(0, 0, 909, 129))
        self.textArea.setObjectName("scrollAreaWidgetContents")
        self.textArea.setReadOnly(True)
        self.scrollArea.setWidget(self.textArea)
        self.logsLabel = QtWidgets.QLabel(self.centralwidget)
        self.logsLabel.setGeometry(QtCore.QRect(20, 350, 58, 16))
        self.logsLabel.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 931, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.selectedButton.setText(_translate("MainWindow", "Select Your Media"))
        self.uploadButton.setText(_translate("MainWindow", "Upload"))
        self.processButton.setText(_translate("MainWindow", "Process"))
        self.comboBox.setItemText(0, _translate("MainWindow", "analysis-transcoder"))
        self.comboBox.setItemText(1, _translate("MainWindow", "amanda-wf-euw4-dev-001-image-width-resize"))
        self.workflowLabel.setText(_translate("MainWindow", "Workflow:"))
        self.logsLabel.setText(_translate("MainWindow", "Logs"))

    def getFiles(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.AnyFile)
        dlg.setFilter(QDir.Filter.Files)
        dlg.setNameFilter("*.mp4")
        dlg.setViewMode(QFileDialog.ViewMode.Detail)
        filename = QStringListModel()

        if dlg.exec():
            filename = dlg.selectedFiles()
            if self.asset:
                del self.asset
            if self.job:
                del self.job
            self.selectedFile = filename[0]
            self.asset = Assets(self.selectedFile)

            model = QtGui.QStandardItemModel()
            model.appendRow(QtGui.QStandardItem(self.asset.asset_name))
            self.listView.setModel(model)

            self.textArea.appendPlainText(f'Selected video {self.asset.asset_name}')
            self.enableButton(self.uploadButton)

    def upload(self):
        self.disableButton(self.selectedButton)
        self.disableButton(self.uploadButton)
        self.asset.upload(self.uploadedAssetCallback)
        self.textArea.appendPlainText(f'Uploading video {self.asset.asset_name} with asset_id {self.asset.asset_id}')

    def process(self):
        self.disableButton(self.processButton)
        self.textArea.appendPlainText(f'Requesting job for video {self.asset.asset_name} with asset_id {self.asset.asset_id}')
        self.job = Jobs(get_workflow_by_name('analysis-transcoder'))
        self.job.process(self.completedJobCallback, assets=[self.asset])
        self.textArea.appendPlainText(f'Requested job by job_id {self.job.job_id} for video {self.asset.asset_name} with asset_id {self.asset.asset_id}')
        self.textArea.appendPlainText(f'Waiting for the job_id {self.job.job_id} to be finished...')

    def enableButton(self, button):
        button.setEnabled(True)

    def disableButton(self, button):
        button.setEnabled(False)

    def uploadedAssetCallback(self):
        self.enableButton(self.processButton),
        self.textArea.appendPlainText(f'Uploaded video {self.asset.asset_name} with asset_id {self.asset.asset_id}')

    def completedJobCallback(self):
        self.enableButton(self.selectedButton)
        self.textArea.appendPlainText(f'Finished job_id {self.job.job_id}'),
        self.textArea.appendPlainText(f'Delivery Urls by jobId "{self.job.job_id}":'),
        [self.textArea.appendPlainText(f'* {delivery_url}') for delivery_url in self.job.get_delivery_urls()],
        self.textArea.appendPlainText('\n'),

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec())
    except Exception as ex:
        print(f'[ERROR] > {ex}')