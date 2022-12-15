import MainWindowFunctions as mwf
import DifferentialGeneAnalysis as dgf
import sys
from PyQt5.QtWidgets import QApplication,QFileDialog,QMenu, QAction,QMainWindow,QWidget,QLabel,QFrame,QVBoxLayout,QPushButton,QComboBox,QLineEdit
from PyQt5.QtCore import QFile, QTextStream,Qt
from PyQt5.QtGui import QIcon
import scanpy as sc
import os

if os.path.isfile('./PreprocessedData/adata.h5ad'):
    adata = sc.read('./PreprocessedData/adata.h5ad') 
    adata.uns['log1p']["base"] = None
else:
    adata = sc.read_10x_mtx(
        'sc_example_data/aggr_iHPF_pHPF_N1_SFT/outs/filtered_feature_bc_matrix/',  
        var_names='gene_symbols',            
        cache=False) 
    adata = mwf.preprocessAnnData(adata)

class PreProcessingPopup(QWidget):
    def __init__(self,parent, adata):
        QWidget.__init__(self)
        self.parent=parent
        self.adata = adata
        self.setStyleSheet('background-color:white;')
        self.setWindowTitle('PreProcessing Specifications')
        self.subtitle1Label = QLabel("Principal component analysis",self)
        self.subtitle1Label.move(20, 20)
        self.subtitle1Label.resize(280,40)
        self.plotLabel = QLabel("SVD solver to use:", self)
        self.plotLabel.move(20, 80)
        self.plotLabel.resize(280,40)
        self.plotComboBox = QComboBox(self)
        self.plotComboBox.addItems(['arpack','randomized', 'auto', 'lobpcg'])
        self.plotLabel.setBuddy(self.plotComboBox)
        self.plotComboBox.move(20, 140)
        self.plotComboBox.resize(280,40)
        
        self.Separator = QFrame(self)
        self.Separator.setFrameShape(QFrame.HLine)
        self.Separator.setLineWidth(1)
        self.Separator.move(20, 180)
        self.Separator.resize(500,40)
        self.subtitle2Label = QLabel("Uniform Manifold Approximation and Projection for Dimension Reduction",self)
        self.subtitle2Label.move(20, 240)
        self.subtitle2Label.resize(500,40)
        self.clusters = QLabel("Number of Clusters",self)
        self.clusters.move(20, 300)
        self.clusters.resize(280,40)
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 360)
        self.textbox.resize(280,40)
        
        self.button = QPushButton('OK', self)
        self.button.setStyleSheet('background-color: #7ad0eb;')
        self.button.move(20,420)
        self.button.resize(280,40)
        # self.c1Label = c1Label
        # self.c2Label = c2Label
        self.button.clicked.connect(self.on_click)
        grid = QVBoxLayout()
        grid.addWidget(self.subtitle1Label)
        grid.addWidget(self.plotLabel)
        grid.addWidget(self.plotComboBox)
        grid.addWidget(self.Separator)
        grid.addWidget(self.subtitle2Label)
        grid.addWidget(self.clusters)
        grid.addWidget(self.textbox)
        grid.addWidget(self.button)
        
        
        

    def on_click(self):
        self.centralwidget = dgf.Window(self,self.adata)
        self.parent.setCentralWidget(self.centralwidget)
        self.close()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Cell Visualization App')
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self._createActions()
        self._createMenuBar()
        self._connectActions()
        self._createStatusBar()

        self.PreProcessingWindow = PreProcessingPopup(self,adata)
        self.PreProcessingWindow.setGeometry(500, 300, 700, 500)
        self.PreProcessingWindow.show()

    def upload(self, *args):
        folderpath  = QFileDialog.getExistingDirectory(self,'Select folder consisting of mtx and .tsv files')
        try:
            adata = sc.read_10x_mtx(
                    folderpath,
                    var_names='gene_symbols',
                    cache=False) 
            adata = mwf.preprocessAnnData(adata)
            self.centralwidget = dgf.Window(adata)
            self.setCentralWidget(self.centralwidget)
        except Exception as e:
             print('ERROR: ',e)

    def uploadh5ad(self):
        try:
            filename = QFileDialog.getOpenFileName()
            path = filename[0]
            adata = sc.read(path)
            adata = mwf.preprocessAnnData(adata)
            self.centralwidget = dgf.Window(adata)
            self.setCentralWidget(self.centralwidget)
        except Exception as e:
             print('ERROR: ',e)
    
    def _createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.openh5adAction)
        fileMenu.addAction(self.openFolderAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")
    
    def _createStatusBar(self):
        self.statusbar = self.statusBar()

    def _createActions(self):
        self.openh5adAction = QAction(self)
        self.openh5adAction.setText("&Open new h5ad file")
        self.openFolderAction = QAction("&Open folder with mtx and tsv files", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
    
    def _connectActions(self):
        self.openh5adAction.triggered.connect(self.uploadh5ad)
        self.openFolderAction.triggered.connect(self.upload)
        # self.saveAction.triggered.connect(self.saveFile)
        # self.exitAction.triggered.connect(self.close)

if __name__ == '__main__':
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


