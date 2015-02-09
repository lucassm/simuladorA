# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogRecloser.ui'
#
# Created: Sun Feb  8 22:33:29 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys
class RecloserDialog(QtGui.QWidget):

    def __init__(self, item):
        super(RecloserDialog, self).__init__()
        self.dialog = QtGui.QDialog(self)
        self.item = item
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(396, 222) 
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(150, 180, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 30, 341, 128))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.identificaOLabel = QtGui.QLabel(self.formLayoutWidget)
        self.identificaOLabel.setObjectName("identificaOLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.identificaOLabel)
        self.identificaOLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.identificaOLineEdit.setObjectName("identificaOLineEdit")
        self.identificaOLineEdit.setPlaceholderText(str(self.item.chave.nome))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.identificaOLineEdit)
        self.correnteNominalLabel = QtGui.QLabel(self.formLayoutWidget)
        self.correnteNominalLabel.setObjectName("correnteNominalLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.correnteNominalLabel)
        self.correnteNominalLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.correnteNominalLineEdit.setObjectName("correnteNominalLineEdit")
        self.correnteNominalLineEdit.setPlaceholderText(str(self.item.chave.ratedCurrent))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.correnteNominalLineEdit)
        self.capacidadeDeInterrupOLabel = QtGui.QLabel(self.formLayoutWidget)
        self.capacidadeDeInterrupOLabel.setObjectName("capacidadeDeInterrupOLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.capacidadeDeInterrupOLabel)
        self.capacidadeDeInterrupOLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.capacidadeDeInterrupOLineEdit.setObjectName("capacidadeDeInterrupOLineEdit")
        self.capacidadeDeInterrupOLineEdit.setPlaceholderText(str(self.item.chave.breakingCapacity))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.capacidadeDeInterrupOLineEdit)
        self.nDeSequNciasDeReligamentoLabel = QtGui.QLabel(self.formLayoutWidget)
        self.nDeSequNciasDeReligamentoLabel.setObjectName("nDeSequNciasDeReligamentoLabel")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.nDeSequNciasDeReligamentoLabel)
        self.nDeSequNciasDeReligamentoLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.nDeSequNciasDeReligamentoLineEdit.setObjectName("nDeSequNciasDeReligamentoLineEdit")
        self.nDeSequNciasDeReligamentoLineEdit.setPlaceholderText(str(self.item.chave.recloseSequences))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.nDeSequNciasDeReligamentoLineEdit)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Religador - Propriedades", None, QtGui.QApplication.UnicodeUTF8))
        self.identificaOLabel.setText(QtGui.QApplication.translate("Dialog", "Identificação:", None, QtGui.QApplication.UnicodeUTF8))
        self.correnteNominalLabel.setText(QtGui.QApplication.translate("Dialog", "Corrente Nominal (A): ", None, QtGui.QApplication.UnicodeUTF8))
        self.capacidadeDeInterrupOLabel.setText(QtGui.QApplication.translate("Dialog", "Capacidade de Interrupção (kA):", None, QtGui.QApplication.UnicodeUTF8))
        self.nDeSequNciasDeReligamentoLabel.setText(QtGui.QApplication.translate("Dialog", "Nº de Sequências de Religamento:", None, QtGui.QApplication.UnicodeUTF8))


    if __name__ == '__main__':
        app = QtGui.QApplication(sys.argv)
        dialogReligador = RecloserDialog()
        sys.exit(app.exec_())