import MainWindowFunctions as mwf
import DifferentialGeneAnalysis as dgf
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout,QFileDialog,QGraphicsDropShadowEffect
from PyQt5.QtCore import QFile, QTextStream,Qt
from PyQt5.QtGui import QFont,QIcon
import scanpy as sc
import os
# import pyqtcss

class Window(QDialog):

    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('Cell Visualization App')
        # self.setFixedSize(QSize(400, 500))
        # self.setStyleSheet("background-color: White;")
        self.showMaximized()
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        f = QFile('homeScreen.qss')                                
        f.open(QFile.ReadOnly | QFile.Text)
        ts = QTextStream(f)
        stylesheet = ts.readAll()    
        self.setStyleSheet(stylesheet)
        
        # uploadButtonshadow = QGraphicsDropShadowEffect()
        # uploadButtonshadow.setBlurRadius(90)
        self.uploadButton = QPushButton("Select Folder with Files", self)
        self.uploadButton.pressed.connect(self.upload)
        # self.uploadButton.setGraphicsEffect(uploadButtonshadow)
        # uploadh5adButtonshadow = QGraphicsDropShadowEffect()
        # uploadh5adButtonshadow.setBlurRadius(90)
        self.uploadh5adButton = QPushButton("Upload New h5ad File", self)
        self.uploadh5adButton.pressed.connect(self.uploadh5ad)
        # self.uploadh5adButton.setGraphicsEffect(uploadh5adButtonshadow)
        # existingFileButtonshadow = QGraphicsDropShadowEffect()
        # existingFileButtonshadow.setBlurRadius(90)
        self.existingFileButton = QPushButton("Use Existing File", self)
        self.existingFileButton.pressed.connect(self.existingFile)
        # self.existingFileButton.setGraphicsEffect(existingFileButtonshadow)
        self.uploadButton.setObjectName("uploadButton")
        self.uploadh5adButton.setObjectName("uploadButton")
        self.existingFileButton.setObjectName("uploadButton")
        

        self.outerLayout = QVBoxLayout()
        self.outerLayout.addWidget(self.uploadButton)
        self.outerLayout.addWidget(self.uploadh5adButton)
        self.outerLayout.addWidget(self.existingFileButton)
        self.outerLayout.setContentsMargins(50, 20, 50, 50)
        self.outerLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.outerLayout)

    def upload(self, *args):
        try:
            folderpath  = QFileDialog.getExistingDirectory(self,'Select folder consisting of mtx and .tsv files')
            adata = sc.read_10x_mtx(
                    folderpath,  # the directory with the `.mtx` file
                    var_names='gene_symbols',                # use gene symbols for the variable names (variables-axis index)
                    cache=False) 
            adata = mwf.preprocessAnnData(adata)
            self.mainWindow = dgf.Window(adata)
            self.mainWindow.show()
        except Exception as e:
             print('ERROR: ',e)
    
    
    def uploadh5ad(self, *args):
        try:
            filename = QFileDialog.getOpenFileName()
            path = filename[0]
            adata = sc.read(path)
            adata = mwf.preprocessAnnData(adata)
            self.mainWindow = dgf.Window(adata)
            self.mainWindow.show()
        except Exception as e:
             print('ERROR: ',e)


    def existingFile(self, *args):
        try:
            if os.path.isfile('./PreprocessedData/adata.h5ad'):
                adata = sc.read('./PreprocessedData/adata.h5ad') 
                adata.uns['log1p']["base"] = None
            else:
                adata = sc.read_10x_mtx(
                    'sc_example_data/aggr_iHPF_pHPF_N1_SFT/outs/filtered_feature_bc_matrix/',  # the directory with the `.mtx` file
                    var_names='gene_symbols',                # use gene symbols for the variable names (variables-axis index)
                    cache=False) 
                adata = mwf.preprocessAnnData(adata)
            self.mainWindow = dgf.Window(adata)
            self.mainWindow.show()
        except Exception as e:
            print('ERROR: ',e)

if __name__ == '__main__':
    # creating apyqt5 application
    app = QApplication(sys.argv)
    # app.setStyleSheet("QLabel{font-size: 1pt;}")
    f = QFile('style.qss')                                
    f.open(QFile.ReadOnly | QFile.Text)
    ts = QTextStream(f)
    stylesheet = ts.readAll()    
    app.setStyleSheet(stylesheet)
    app.setWindowIcon(QIcon('images/RNALogo.png'))
    main = Window()
    main.show()
    sys.exit(app.exec_())