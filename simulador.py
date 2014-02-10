# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulador.ui'
#
# Created: Sun Jan 26 16:58:45 2014
#      by: Lucas S Melo
#

from PySide import QtCore, QtGui
from graphics import SceneWidget, ViewWidget
import sys

class Ui_MainWindow(object):
    '''
        Esta classe implementa a inteface grafica do simulador
    '''
    
    def __init__(self):
        pass
        #self.createActions()
        #self.createMenus()
    
    def setupUi(self, MainWindow):
        '''
            Este metodo implementa os componentes da inteface grafica
        '''
        
        # objeto define a janela pricipal do aplicativo
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        
        # define o widget central do aplicativo
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # define o tipo de layout do widget central como gridLayout
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
        # define a classe SceneWidget e ViewWidget como containers dos widgets
        self.sceneWidget = SceneWidget()
        self.graphicsView = ViewWidget(self.sceneWidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(256, 0))
        self.graphicsView.setObjectName("graphicsView")
        
        # adiciona os sinais ao objeto sceneWidget
        self.sceneWidget.itemInserted.connect(self.itemInserted)
        
        
        # conecta os botoes aos signals da sceneWidget
        #self.sceneWidget.InsertItem.connect(self.itemInserted)
        
        # seta o objeto QGraphicsView no gridLayout
        self.gridLayout.addWidget(self.graphicsView, 0, 0)
        MainWindow.setCentralWidget(self.centralwidget)
        
        # define a barra de menus
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        # define a barra de status
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        # define a barra de ferramentas
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setEnabled(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        
        # define o widget dockWidget dockWidget_Buttons e configura seu conteudo dockWidget_Buttons_Contents
        self.dockWidget_Buttons = QtGui.QDockWidget(MainWindow)
        self.dockWidget_Buttons.setObjectName("dockWidget_Buttons")
        self.dockWidget_Buttons_Contents = QtGui.QWidget()
        self.dockWidget_Buttons_Contents.setMinimumWidth(230)
        self.dockWidget_Buttons_Contents.setObjectName("dockWidget_Buttons_Contents")
        
        #  define o layput dos botoes no dockWidget  gridLayout
        self.gridLayout_dockWidget = QtGui.QGridLayout(self.dockWidget_Buttons_Contents)
        self.gridLayout_dockWidget.setObjectName("gridLayout_dockWidget")
        
        # define o objeto QToolBox que comportara as abas de botoes
        self.toolBox = QtGui.QToolBox(self.dockWidget_Buttons_Contents)
        self.toolBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolBox.setObjectName("toolBox")
        
        # define a primeira pagina do dockWidget
        self.page_1 = QtGui.QWidget()
        self.page_1.setGeometry(QtCore.QRect(0, 0, 100, 50))
        
        # configura a primeira pagina do dockWidget
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page_1.sizePolicy().hasHeightForWidth())
        self.page_1.setSizePolicy(sizePolicy)
        self.page_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.page_1.setAutoFillBackground(True)
        self.page_1.setObjectName("page_1")
        
        # define o Layout da primeira pagina do dockWidget
        self.gridlayout_page_1 = QtGui.QGridLayout(self.page_1)
        self.gridlayout_page_1.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridlayout_page_1.setObjectName("gridlayout_page_1")
        
        # define os botoes da primeira pagina do dockWidget e insere no FormLayout
        self.substationButton = QtGui.QPushButton(self.page_1)
        self.substationButton.setObjectName("substationButton")
        self.substationButton.setCheckable(True)
        self.busButton = QtGui.QPushButton(self.page_1)
        self.busButton.setObjectName("busButton")
        self.busButton.setCheckable(True)
        self.recloserButton = QtGui.QPushButton(self.page_1)
        self.recloserButton.setObjectName("recloserButton")
        self.recloserButton.setCheckable(True)
        self.lineButton = QtGui.QPushButton(self.page_1)
        self.lineButton.setObjectName("lineButton")
        self.lineButton.setCheckable(True)        
        
        
        # define o grupo de botoes da pagina 1 do notebook
        self.buttonGroup = QtGui.QButtonGroup()
        self.buttonGroup.addButton(self.substationButton, 0)
        self.buttonGroup.addButton(self.recloserButton, 1)
        self.buttonGroup.addButton(self.busButton, 2)
        self.buttonGroup.addButton(self.lineButton, 3)
        self.buttonGroup.setExclusive(False)
        
        self.buttonGroup.buttonClicked[int].connect(self.buttonGroupClicked)
        
        # define labels da primeira pagina do dockWidget
        self.substationLabel = QtGui.QLabel('')
        self.substationLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.substationLabel.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.substationLabel.setObjectName("substationLabel")
        self.recloserLabel = QtGui.QLabel('')
        self.recloserLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.recloserLabel.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.recloserLabel.setObjectName("recloserLabel")
        self.busLabel = QtGui.QLabel('')
        self.busLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.busLabel.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.busLabel.setObjectName("busLabel")
        self.lineLabel = QtGui.QLabel('')
        self.lineLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.lineLabel.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.lineLabel.setObjectName("lineLabel")
        
        # adiciona os botoes ao gridLayout_3
        self.gridlayout_page_1.addWidget(self.substationButton, 0, 0)
        self.gridlayout_page_1.addWidget(self.recloserButton, 0, 1)
        self.gridlayout_page_1.addWidget(self.substationLabel, 1, 0)
        self.gridlayout_page_1.addWidget(self.recloserLabel, 1, 1)
        self.gridlayout_page_1.addWidget(self.busButton, 2, 0)
        self.gridlayout_page_1.addWidget(self.lineButton, 2, 1)
        self.gridlayout_page_1.addWidget(self.busLabel, 3, 0)
        self.gridlayout_page_1.addWidget(self.lineLabel, 3, 1)
        
        # adiciona o gridLayout_3 a pagina_1 do dockWidget
        self.page_1.setLayout(self.gridlayout_page_1)
        
        # seta a primeira pagina do dockWidget 
        self.toolBox.addItem(self.page_1, "")
        
        # define a segunda pagina do dockWidget
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 100, 50))
        self.page_2.setObjectName("page_2")
        self.toolBox.addItem(self.page_2, "")
        
        
        self.gridLayout_dockWidget.addWidget(self.toolBox, 0, 0)
        self.dockWidget_Buttons.setWidget(self.dockWidget_Buttons_Contents)
        
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_Buttons)
        
        
        # configura os botoes da barra de ferramentas
        self.actionExit = QtGui.QAction(MainWindow)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon)
        self.actionExit.setObjectName("actionExit")
        self.toolBar.addAction(self.actionExit)
        
        # configuracoes adicionais
        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def itemInserted(self, itemType):
        '''
            Callback chamada no momento em que um item e iserido
            no diagrama grafico
        '''
        self.buttonGroup.button(itemType).setChecked(False)
        self.sceneWidget.setMode(self.sceneWidget.MoveItem)
    
    def buttonGroupClicked(self, id):
        '''
            Callback chamada no momento em que um botao de insersao
            de itens e pressionado 
        '''
        print id
        buttons = self.buttonGroup.buttons()
        for button in buttons:
            if self.buttonGroup.button(id) != button:
                button.setChecked(False)
        
        if id == 3:
            self.sceneWidget.setMode(SceneWidget.InsertLine)
        else:
            self.sceneWidget.setItemType(id)
            self.sceneWidget.setMode(SceneWidget.InsertItem)
        

    def retranslateUi(self, MainWindow):
        
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        
        self.substationButton.setText(QtGui.QApplication.translate("MainWindow", "Subestação", None, QtGui.QApplication.UnicodeUTF8))
        
        self.busButton.setText(QtGui.QApplication.translate("MainWindow", "Barra", None, QtGui.QApplication.UnicodeUTF8))
        
        self.busLabel.setText(QtGui.QApplication.translate("MainWindow", "Barra", None, QtGui.QApplication.UnicodeUTF8))
        
        self.substationLabel.setText(QtGui.QApplication.translate("MainWindow", "Subestação", None, QtGui.QApplication.UnicodeUTF8))
        
        self.recloserButton.setText(QtGui.QApplication.translate("MainWindow", "Religador", None, QtGui.QApplication.UnicodeUTF8))
        
        self.recloserLabel.setText(QtGui.QApplication.translate("MainWindow", "Religador", None, QtGui.QApplication.UnicodeUTF8))
        
        self.lineButton.setText(QtGui.QApplication.translate("MainWindow", "Linha", None, QtGui.QApplication.UnicodeUTF8))
        
        self.lineLabel.setText(QtGui.QApplication.translate("MainWindow", "Linha", None, QtGui.QApplication.UnicodeUTF8))
        
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_1), QtGui.QApplication.translate("MainWindow", "Pagina 1", None, QtGui.QApplication.UnicodeUTF8))
        
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QtGui.QApplication.translate("MainWindow", "Pagina 2", None, QtGui.QApplication.UnicodeUTF8))
        
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        
        self.actionExit.setToolTip(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        
        self.actionExit.setShortcut(QtGui.QApplication.translate("MainWindow", "4, Backspace", None, QtGui.QApplication.UnicodeUTF8))


class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self)
   
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())