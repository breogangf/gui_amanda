import sys
import threading
from pathlib import Path
from dotenv import load_dotenv
from PyQt6.QtCore import QSize, Qt, QStringListModel, QDir
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QBoxLayout, QWidget, QFileDialog, QPlainTextEdit

env_variables_path = Path(__file__).resolve().with_name(".env")
load_dotenv(dotenv_path=env_variables_path)

from src.setup_logger import logger
from src.assets import Assets
from src.jobs import Jobs
from src.utils import get_workflow_by_name

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Amanda GUI")
        self.setFixedSize(QSize(800, 600))

        self.selectedFile = ''
        self.asset = None
        self.job = None

        buttonSelect = QPushButton("Select video")
        buttonSelect.clicked.connect(self.getFiles)
        self.buttonSelect = buttonSelect

        buttonUpload = QPushButton("Upload")
        buttonUpload.clicked.connect(self.upload)
        buttonUpload.setEnabled(False)
        self.buttonUpload = buttonUpload

        buttonProcess = QPushButton("Process")
        buttonProcess.clicked.connect(self.process)
        buttonProcess.setEnabled(False)
        self.buttonProcess = buttonProcess

        textArea = QPlainTextEdit(self)
        textArea.setReadOnly(True)
        self.textArea = textArea

        verticalLayout = QBoxLayout(QBoxLayout.Direction(2), self)

        verticalLayout.addWidget(buttonSelect)
        verticalLayout.addWidget(buttonUpload)
        verticalLayout.addWidget(buttonProcess)
        verticalLayout.addWidget(textArea)

        widget = QWidget()
        widget.setLayout(verticalLayout)
        self.setCentralWidget(widget)

    def upload(self):
        self.disableButton(self.buttonSelect)
        self.disableButton(self.buttonUpload)
        self.asset.upload(self.uploadedAssetCallback)
        self.textArea.appendPlainText(f'Uploading video {self.asset.asset_name} with asset_id {self.asset.asset_id}')

    def process(self):
        self.disableButton(self.buttonProcess)
        self.textArea.appendPlainText(f'Requesting job for video {self.asset.asset_name} with asset_id {self.asset.asset_id}')
        self.job = Jobs(get_workflow_by_name('analysis-transcoder'))
        self.job.process(self.completedJobCallback, assets=[self.asset])
        self.textArea.appendPlainText(f'Requested job by job_id {self.job.job_id} for video {self.asset.asset_name} with asset_id {self.asset.asset_id}')
        self.textArea.appendPlainText(f'Waiting for the job_id {self.job.job_id} to be finished...')

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
            self.textArea.appendPlainText(f'Selected video {self.asset.asset_name}')
            self.enableButton(self.buttonUpload)

    def uploadedAssetCallback(self):
        self.enableButton(self.buttonProcess),
        self.textArea.appendPlainText(f'Uploaded video {self.asset.asset_name} with asset_id {self.asset.asset_id}')

    def completedJobCallback(self):
        self.enableButton(self.buttonSelect)
        self.textArea.appendPlainText(f'Finished job_id {self.job.job_id}'),
        self.textArea.appendPlainText(f'Delivery Urls by jobId "{self.job.job_id}":'),
        [self.textArea.appendPlainText(f'* {delivery_url}') for delivery_url in self.job.get_delivery_urls()],
        self.textArea.appendPlainText('\n'),

    def enableButton(self, button):
        button.setEnabled(True)

    def disableButton(self, button):
        button.setEnabled(False)

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec()
    except Exception as ex:
        print(f'[ERROR] > {ex}')