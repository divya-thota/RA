import MainWindowFunctions as mwf
import DifferentialGeneAnalysis as dgf
import sys
from PyQt5.QtWidgets import QApplication,QFileDialog,QMenu, QAction,QMainWindow
from PyQt5.QtCore import QFile, QTextStream,Qt
from PyQt5.QtGui import QIcon
import scanpy as sc
import os
# import pyqtcss

# class Worker(QObject):
#     finished = pyqtSignal()
#     def __init__(self, folderpath):
#         super().__init__()
#         self.folderpath = folderpath

#     def run(self):
#         try:
#             adata = sc.read_10x_mtx(
#                     self.folderpath,  # the directory with the `.mtx` file
#                     var_names='gene_symbols',                # use gene symbols for the variable names (variables-axis index)
#                     cache=False) 
#             adata = mwf.preprocessAnnData(adata)
#             self.mainWindow = dgf.Window(adata)
#             self.mainWindow.show()
#             self.finished.emit()
#         except Exception as e:
#              print('ERROR: ',e)
#              self.finished.emit()

if os.path.isfile('./PreprocessedData/adata.h5ad'):
    adata = sc.read('./PreprocessedData/adata.h5ad') 
    adata.uns['log1p']["base"] = None
else:
    adata = sc.read_10x_mtx(
        'sc_example_data/aggr_iHPF_pHPF_N1_SFT/outs/filtered_feature_bc_matrix/',  # the directory with the `.mtx` file
        var_names='gene_symbols',                # use gene symbols for the variable names (variables-axis index)
        cache=False) 
    adata = mwf.preprocessAnnData(adata)

class MainWindow(QMainWindow):
    # constructor
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Cell Visualization App')
        # self.setFixedSize(QSize(400, 500))
        # self.setStyleSheet("background-color: White;")
        #ELEPHANT : Restore down
        
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        # f = QFile('homeScreen.qss')                                
        # f.open(QFile.ReadOnly | QFile.Text)
        # ts = QTextStream(f)
        # stylesheet = ts.readAll()    
        # self.setStyleSheet(stylesheet)
        self._createActions()
        self._createMenuBar()
        self._connectActions()
        self._createStatusBar()
        self.table_widget = dgf.Window(self,adata)
        self.setCentralWidget(self.table_widget)
        # genes = pd.DataFrame(adata.var.gene_ids)
        # gene_ids = genes['gene_ids'].to_numpy()
        # self.typeComboBox = QComboBox(self)
        # self.typeComboBox.addItems(['PCA', 'UMAP'])
        # self.typeLabel = QLabel("Type:")
        # self.typeLabel.setBuddy(self.typeComboBox)
        # uploadButtonshadow = QGraphicsDropShadowEffect()
        # uploadButtonshadow.setBlurRadius(90)
        # self.uploadButton = QPushButton("Select Folder with Files", self)
        # self.uploadButton.pressed.connect(self.upload)
        # self.uploadButton.setGraphicsEffect(uploadButtonshadow)
        # uploadh5adButtonshadow = QGraphicsDropShadowEffect()
        # uploadh5adButtonshadow.setBlurRadius(90)
        # self.uploadh5adButton = QPushButton("Upload New h5ad File", self)
        # self.uploadh5adButton.pressed.connect(self.uploadh5ad)
        # self.uploadh5adButton.setGraphicsEffect(uploadh5adButtonshadow)
        # existingFileButtonshadow = QGraphicsDropShadowEffect()
        # existingFileButtonshadow.setBlurRadius(90)
        # self.existingFileButton = QPushButton("Use Existing File", self)
        # self.existingFileButton.pressed.connect(self.existingFile)
        # self.existingFileButton.setGraphicsEffect(existingFileButtonshadow)
        # self.uploadButton.setObjectName("uploadButton")
        # self.uploadh5adButton.setObjectName("uploadButton")
        # self.existingFileButton.setObjectName("uploadButton")
        # self.label = QLabel("lbl")
        # self.movie = QMovie("images/loading-gif.gif")
        # self.movie.setScaledSize(QSize(50, 50))
        # self.label.setAlignment(Qt.AlignCenter)
        # self.label.setMovie(self.movie)
        

        # self.outerLayout = QVBoxLayout()
        # self.outerLayout.addWidget(self.uploadButton)
        # self.outerLayout.addWidget(self.uploadh5adButton)
        # self.outerLayout.addWidget(self.existingFileButton)
        # self.outerLayout.addWidget(self.label)
        # self.outerLayout.setContentsMargins(50, 20, 50, 50)
        # self.outerLayout.setAlignment(Qt.AlignCenter)
        # self.setLayout(self.outerLayout)

    def upload(self, *args):
        folderpath  = QFileDialog.getExistingDirectory(self,'Select folder consisting of mtx and .tsv files')
        # self.thread = QThread()
        # self.worker = Worker(folderpath)
        # self.worker.moveToThread(self.thread)
        # self.thread.started.connect(self.worker.run)
        # # self.worker.finished.connect(self.worker.deleteLater)
        # # self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.finished.connect(self.thread.quit)
        # self.thread.start()
        # # self.startAnimation()
        try:
            adata = sc.read_10x_mtx(
                    folderpath,  # the directory with the `.mtx` file
                    var_names='gene_symbols',                # use gene symbols for the variable names (variables-axis index)
                    cache=False) 
            adata = mwf.preprocessAnnData(adata)
            self.table_widget = dgf.Window(adata)
            self.setCentralWidget(self.table_widget)
        except Exception as e:
             print('ERROR: ',e)

    def uploadh5ad(self):
        try:
            # self.startAnimation()
            filename = QFileDialog.getOpenFileName()
            path = filename[0]
            adata = sc.read(path)
            adata = mwf.preprocessAnnData(adata)
            self.table_widget = dgf.Window(adata)
            self.setCentralWidget(self.table_widget)
            # self.stopAnimation()
        except Exception as e:
             print('ERROR: ',e)
    
    # def startAnimation(self):
    #     self.movie.start()
    
    # def stopAnimation(self):
    #     self.movie.stop()
    
    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.openh5adAction)
        fileMenu.addAction(self.openFolderAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)
        # Creating menus using a title
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")
    
    def _createStatusBar(self):
        self.statusbar = self.statusBar()

    def _createActions(self):
        # Creating action using the first constructor
        self.openh5adAction = QAction(self)
        self.openh5adAction.setText("&Open new h5ad file")
        # Creating actions using the second constructor
        self.openFolderAction = QAction("&Open folder with mtx and tsv files", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
    
    def _connectActions(self):
        # Connect File actions
        self.openh5adAction.triggered.connect(self.uploadh5ad)
        self.openFolderAction.triggered.connect(self.upload)
        # self.saveAction.triggered.connect(self.saveFile)
        # self.exitAction.triggered.connect(self.close)

if __name__ == '__main__':
    # creating apyqt5 application
    app = QApplication(sys.argv)
    app.setStyleSheet("QLabel{font-size: 1pt;}")
    f = QFile('style.qss')                                
    f.open(QFile.ReadOnly | QFile.Text)
    ts = QTextStream(f)
    stylesheet = ts.readAll()    
    app.setStyleSheet(stylesheet)
    app.setWindowIcon(QIcon('images/RNALogo.png'))
    main = MainWindow()
    main.showMaximized()
    main.show()
    sys.exit(app.exec_())