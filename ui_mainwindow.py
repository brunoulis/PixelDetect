# ui_mainwindow.py
from PySide6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Establecer estilo oscuro para el fondo
        self.centralwidget.setStyleSheet("background-color: #212121; color: #FFFFFF;")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.image_view = QtWidgets.QGraphicsView(self.centralwidget)
        self.image_view.setObjectName("image_view")
        self.gridLayout.addWidget(self.image_view, 0, 0, 1, 2)
        self.load_image_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_image_button.setObjectName("load_image_button")
        self.gridLayout.addWidget(self.load_image_button, 1, 0, 1, 1)
        self.recognition_type = QtWidgets.QComboBox(self.centralwidget)
        self.recognition_type.setObjectName("recognition_type")
        self.recognition_type.addItem("Objetos")
        self.recognition_type.addItem("Caras")
        self.recognition_type.addItem("Patrones")
        self.gridLayout.addWidget(self.recognition_type, 1, 1, 1, 1)
        self.recognize_button = QtWidgets.QPushButton(self.centralwidget)
        self.recognize_button.setObjectName("recognize_button")
        self.gridLayout.addWidget(self.recognize_button, 2, 0, 1, 1)
        self.results_text = QtWidgets.QTextEdit(self.centralwidget)
        self.results_text.setObjectName("results_text")
        self.gridLayout.addWidget(self.results_text, 3, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Recognition App"))
        self.load_image_button.setText(_translate("MainWindow", "Cargar Imagen"))
        self.recognize_button.setText(_translate("MainWindow", "Iniciar Reconocimiento"))
