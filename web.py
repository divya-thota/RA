from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

import sys

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        # file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'temporary_files', "map.html"))
        # self.browser.load(QUrl.fromLocalFile(file_path))
        self.setCentralWidget(self.browser)
        self.browser.setHtml("Hello World... Hello World")
        self.show()



app = QApplication(sys.argv)
window = MainWindow()

app.exec_()