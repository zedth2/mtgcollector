# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cardprev.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!
import json

from PyQt5 import QtCore, QtGui, QtWidgets

from utils.mana import downloadimg


class CardPreview(QtWidgets.QWidget):
    def __init__(self, parent=None, flags=0):
        super().__init__(parent, QtCore.Qt.WindowFlags(flags))
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblImg = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblImg.sizePolicy().hasHeightForWidth())
        self.lblImg.setSizePolicy(sizePolicy)
        self.lblImg.setText("")
        self.lblImg.setPixmap(QtGui.QPixmap("media/template.png"))
        self.lblImg.setScaledContents(True)
        self.lblImg.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblImg.setObjectName("lblImg")
        self.verticalLayout.addWidget(self.lblImg)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblName = QtWidgets.QLabel(self)
        self.lblName.setObjectName("lblName")
        self.horizontalLayout.addWidget(self.lblName)
        self.lblMana = QtWidgets.QLabel(self)
        self.lblMana.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblMana.setObjectName("lblMana")
        self.horizontalLayout.addWidget(self.lblMana)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lblTypeLine = QtWidgets.QLabel(self)
        self.lblTypeLine.setObjectName("lblTypeLine")
        self.verticalLayout.addWidget(self.lblTypeLine)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblSetName = QtWidgets.QLabel(self)
        self.lblSetName.setObjectName("lblSetName")
        self.horizontalLayout_2.addWidget(self.lblSetName)
        self.lblRarity = QtWidgets.QLabel(self)
        self.lblRarity.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblRarity.setObjectName("lblRarity")
        self.horizontalLayout_2.addWidget(self.lblRarity)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.lblOracle = QtWidgets.QLabel(self)
        self.lblOracle.setWordWrap(True)
        self.lblOracle.setObjectName("lblOracle")
        self.verticalLayout.addWidget(self.lblOracle)
        self.lblPowers = QtWidgets.QLabel(self)
        self.lblPowers.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblPowers.setObjectName("lblPowers")
        self.verticalLayout.addWidget(self.lblPowers)
        self.lblLegals = QtWidgets.QLabel(self)
        self.lblLegals.setObjectName("lblLegals")
        self.verticalLayout.addWidget(self.lblLegals)
        self.lblExtras = QtWidgets.QLabel(self)
        self.lblExtras.setObjectName("lblExtras")
        self.verticalLayout.addWidget(self.lblExtras)

        #self.retranslateUi(Form)
        #QtCore.QMetaObject.connectSlotsByName(Form)

    def change_card(self, card):
        self.card = card
        self.lblImg.setPixmap(QtGui.QPixmap(downloadimg(self.card)))
        self.lblName.setText(self.card.name)
        self.lblMana.setText(self.card.mana_cost)
        self.lblTypeLine.setText(self.card.type_line)
        self.lblSetName.setText(self.card.set_code)
        self.lblRarity.setText(self.card.rarity)
        self.lblOracle.setText(self.card.oracle_text)
        if self.card.loyalty:
            self.lblPowers.setVisible(True)
            self.lblPowers.setText(self.card.loyalty)
        elif self.card.power or self.card.toughness:
            self.lblPowers.setVisible(True)
            self.lblPowers.setText(self.card.power + '/' + self.card.toughness)
        else:
            self.lblPowers.setVisible(False)
        try:
            self.lblLegals.setVisible(True)
            self.lblLegals.setText(json.dumps(self.card.legalities['legalities'], indent=2))
        except KeyError:
            self.lblLegals.setVisible(False)
        if self.card.extras != '{}' or self.card.layout != 'normal':
            self.lblExtras.setVisible(True)
            self.lblExtras.setText('Layout: ' + self.card.layout + '\n' + self.card.extras)
        else:
            self.lblExtras.setText('')
            self.lblExtras.setVisible(False)



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lblName.setText(_translate("Form", "NAME"))
        self.lblMana.setText(_translate("Form", "MANA"))
        self.lblTypeLine.setText(_translate("Form", "TYPE LINE"))
        self.lblSetName.setText(_translate("Form", "SET NAME"))
        self.lblRarity.setText(_translate("Form", "RARITY"))
        self.lblOracle.setText(_translate("Form", "ORACLE"))
        self.lblPowers.setText(_translate("Form", "POWERSTOUGHNESS"))
        self.lblLegals.setText(_translate("Form", "LEGALS"))
        self.lblExtras.setText(_translate("Form", "EXTRAS"))
