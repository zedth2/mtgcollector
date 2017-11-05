# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'collection.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class CollectionInfo(QtWidgets.QWidget):
    def __init__(self, parent=None, flags=0):
        super().__init__(parent, QtCore.Qt.WindowFlags(flags))
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lyhCsvFile = QtWidgets.QHBoxLayout()
        self.lyhCsvFile.setObjectName("lyhCsvFile")
        self.lblCsvFile = QtWidgets.QLabel(self)
        self.lblCsvFile.setObjectName("lblCsvFile")
        self.lyhCsvFile.addWidget(self.lblCsvFile)
        self.txtCsvFile = QtWidgets.QLineEdit(self)
        self.txtCsvFile.setObjectName("txtCsvFile")
        self.lyhCsvFile.addWidget(self.txtCsvFile)
        self.verticalLayout.addLayout(self.lyhCsvFile)
        self.lyhName = QtWidgets.QHBoxLayout()
        self.lyhName.setObjectName("lyhName")
        self.lblName = QtWidgets.QLabel(self)
        self.lblName.setObjectName("lblName")
        self.lyhName.addWidget(self.lblName)
        self.txtName = QtWidgets.QLineEdit(self)
        self.txtName.setObjectName("txtName")
        self.lyhName.addWidget(self.txtName)
        self.verticalLayout.addLayout(self.lyhName)
        self.lyhPath = QtWidgets.QHBoxLayout()
        self.lyhPath.setObjectName("lyhPath")
        self.lblPath = QtWidgets.QLabel(self)
        self.lblPath.setObjectName("lblPath")
        self.lyhPath.addWidget(self.lblPath)
        self.cbxPath = QtWidgets.QComboBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbxPath.sizePolicy().hasHeightForWidth())
        self.cbxPath.setSizePolicy(sizePolicy)
        self.cbxPath.setEditable(True)
        self.cbxPath.setObjectName("cbxPath")
        self.lyhPath.addWidget(self.cbxPath)
        self.verticalLayout.addLayout(self.lyhPath)
        self.lyhFormat = QtWidgets.QHBoxLayout()
        self.lyhFormat.setObjectName("lyhFormat")
        self.lblFormat = QtWidgets.QLabel(self)
        self.lblFormat.setObjectName("lblFormat")
        self.lyhFormat.addWidget(self.lblFormat)
        self.cbxFormat = QtWidgets.QComboBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbxFormat.sizePolicy().hasHeightForWidth())
        self.cbxFormat.setSizePolicy(sizePolicy)
        self.cbxFormat.setEditable(True)
        self.cbxFormat.setObjectName("cbxFormat")
        self.lyhFormat.addWidget(self.cbxFormat)
        self.verticalLayout.addLayout(self.lyhFormat)
        self.lblTableName = QtWidgets.QLabel(self)
        self.lblTableName.setObjectName("lblTableName")
        self.verticalLayout.addWidget(self.lblTableName)
        self.lblType = QtWidgets.QLabel(self)
        self.lblType.setObjectName("lblType")
        self.verticalLayout.addWidget(self.lblType)
        self.btnCsvImport = QtWidgets.QPushButton(self)
        self.btnCsvImport.setObjectName("btnCsvImport")
        self.verticalLayout.addWidget(self.btnCsvImport)

        self.retranslateUi()
        #QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        #Form.setWindowTitle(_translate("Form", "Form"))
        self.lblCsvFile.setText(_translate("Form", "CSV:"))
        self.lblName.setText(_translate("Form", "Name:"))
        self.lblPath.setText(_translate("Form", "Path:"))
        self.lblFormat.setText(_translate("Form", "Format:"))
        self.lblTableName.setText(_translate("Form", "Table Name:"))
        self.lblType.setText(_translate("Form", "Type:"))
        self.btnCsvImport.setText(_translate("Form", "Import CSV"))

    def collection_show(self):
        self.lblCsvFile.setVisible(False)
        self.txtCsvFile.setVisible(False)

        self.lblFormat.setVisible(False)
        self.cbxFormat.setVisible(False)

        self.btnCsvImport.setVisible(False)

    def deck_show(self):
        self.lblFormat.setVisible(True)
        self.cbxFormat.setVisible(True)

        self.btnCsvImport.setVisible(False)

    def csv_show(self):
        self.lblCsvFile.setVisible(True)
        self.txtCsvFile.setVisible(True)

        self.lblFormat.setVisible(True)
        self.cbxFormat.setVisible(True)

        self.btnCsvImport.setVisible(True)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #Form = QtWidgets.QWidget()
    ui = Ui_Form()
    #ui.setupUi(Form)
    ui.show()
    sys.exit(app.exec_())
