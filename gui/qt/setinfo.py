# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg

from utils.mana import downloadsvg

class SetInfo(QtWidgets.QWidget):
    def __init__(self, parent=None, windowflags=0):
        super().__init__(parent, QtCore.Qt.WindowFlags(windowflags))
        self.setObjectName("Form")
        #Form.resize(725, 518)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblIcon = QtWidgets.QLabel(self)
        self.lblIcon.setScaledContents(False)
        self.lblIcon.setAlignment(QtCore.Qt.AlignCenter)
        self.lblIcon.setObjectName("label")
        self.verticalLayout.addWidget(self.lblIcon)
        self.lblSetNameVal = QtWidgets.QLabel(self)
        self.lblSetNameVal.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lblSetNameVal.setObjectName("lblSetNameVal")
        self.verticalLayout.addWidget(self.lblSetNameVal)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblBlock = QtWidgets.QLabel(self)
        self.lblBlock.setObjectName("lblBlock")
        self.horizontalLayout_2.addWidget(self.lblBlock)
        self.lblBlockVal = QtWidgets.QLabel(self)
        self.lblBlockVal.setObjectName("lblBlockVal")
        self.horizontalLayout_2.addWidget(self.lblBlockVal)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lblSetType = QtWidgets.QLabel(self)
        self.lblSetType.setObjectName("lblSetType")
        self.horizontalLayout_6.addWidget(self.lblSetType)
        self.lblSetTypeVal = QtWidgets.QLabel(self)
        self.lblSetTypeVal.setObjectName("lblSetTypeVal")
        self.horizontalLayout_6.addWidget(self.lblSetTypeVal)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lblReleaseDate = QtWidgets.QLabel(self)
        self.lblReleaseDate.setObjectName("lblReleaseDate")
        self.horizontalLayout_4.addWidget(self.lblReleaseDate)
        self.lblReleaseDateVal = QtWidgets.QLabel(self)
        self.lblReleaseDateVal.setObjectName("lblReleaseDateVal")
        self.horizontalLayout_4.addWidget(self.lblReleaseDateVal)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lblGathererCode = QtWidgets.QLabel(self)
        self.lblGathererCode.setObjectName("lblGathererCode")
        self.horizontalLayout_3.addWidget(self.lblGathererCode)
        self.lblGathererCodeVal = QtWidgets.QLabel(self)
        self.lblGathererCodeVal.setObjectName("lblGathererCodeVal")
        self.horizontalLayout_3.addWidget(self.lblGathererCodeVal)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lblCount = QtWidgets.QLabel(self)
        self.lblCount.setObjectName("lblCount")
        self.horizontalLayout_5.addWidget(self.lblCount)
        self.lblCountVal = QtWidgets.QLabel(self)
        self.lblCountVal.setObjectName("lblCountVal")
        self.horizontalLayout_5.addWidget(self.lblCountVal)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.btnDownload = QtWidgets.QPushButton(self)
        self.btnDownload.setObjectName("btnDownload")
        self.verticalLayout.addWidget(self.btnDownload)

        self.lblIcon.setText("TextLabel")
        self.lblSetNameVal.setText("None")
        self.lblBlock.setText("Block:")
        self.lblBlockVal.setText("None")
        self.lblSetType.setText("Type:")
        self.lblSetTypeVal.setText("None")
        self.lblReleaseDate.setText("Released:")
        self.lblReleaseDateVal.setText("None")
        self.lblGathererCode.setText("Gatherer Code:")
        self.lblGathererCodeVal.setText("None")
        self.lblCount.setText("Count:")
        self.lblCountVal.setText("0")
        self.btnDownload.setText("Download Set")

        self.set = None

        #self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        #Form.setWindowTitle(_translate("Form", "Form"))
        self.lblIcon.setText(_translate("Form", "TextLabel"))
        self.lblSetNameVal.setText(_translate("Form", "None"))
        self.lblBlock.setText(_translate("Form", "Block:"))
        self.lblBlockVal.setText(_translate("Form", "None"))
        self.lblSetType.setText(_translate("Form", "Type:"))
        self.lblSetTypeVal.setText(_translate("Form", "None"))
        self.lblReleaseDate.setText(_translate("Form", "Released:"))
        self.lblReleaseDateVal.setText(_translate("Form", "None"))
        self.lblGathererCode.setText(_translate("Form", "Gatherer Code:"))
        self.lblGathererCodeVal.setText(_translate("Form", "None"))
        self.lblCount.setText(_translate("Form", "Count:"))
        self.lblCountVal.setText(_translate("Form", "0"))
        self.btnDownload.setText(_translate("Form", "Download Set"))

    def load_set(self, set):
        self.lblSetNameVal.setText(set.name)
        if set.block:
            self.lblBlock.setVisible(True)
            self.lblBlockVal.setText(set.block)
            self.lblBlockVal.setVisible(True)
        else:
            self.lblBlock.setVisible(False)
            self.lblBlockVal.setVisible(False)
        self.lblSetTypeVal.setText(set.set_type)
        self.lblReleaseDateVal.setText(str(set.release_date))
        if set.block:
            self.lblGathererCodeVal.setText(str(set.gatherer_code))
            self.lblGathererCode.setVisible(True)
            self.lblGathererCodeVal.setVisible(True)
        else:
            self.lblGathererCode.setVisible(False)
            self.lblGathererCodeVal.setVisible(False)

        self.lblCountVal.setText(str(set.card_count))

        #renderer = QtSvg.QSvgRenderer(downloadsvg(set))
        #painter = QtGui.QPainter(self.lblIcon)
        #painter.restore()
        #renderer.render(painter)

        svg = QtGui.QPixmap(downloadsvg(set))
        self.btnDownload.setIcon(QtGui.QIcon(svg))
        self.lblIcon.setPixmap(svg.scaled(QtCore.QSize(75,75), QtCore.Qt.KeepAspectRatio))

        self.set = set

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #Form = QtWidgets.QWidget()
    ui = SetInfo()
    #ui.setupUi(Form)
    ui.show()
    sys.exit(app.exec_())
