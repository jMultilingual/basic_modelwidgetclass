from PySide6.QtWidgets import (QApplication,
                               QListWidgetItem,
                               QListWidget,
                               QStyledItemDelegate)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import QSize, Qt
import sys
import resources

class StyledItemDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super().__init__(parent)
        
            
    
    def paint(self, painter, option, index):

        row = index.row()
        if row == 0:
            option.decorationSize = QSize(50, 50)
            option.font = QFont("Times New Roman", 18)

        elif row == 1:
            option.decorationSize = QSize(100, 100)
            option.font = QFont("Segoe UI Light", 36)

        elif row == 2:
            option.decorationSize = QSize(150, 150)
            option.font = QFont("Segoe UI Black", 54)

        super().paint(painter, option, index)

    def sizeHint(self, option, index):

        row = index.row()
        if row == 0:
            return QSize(50, 50)

        elif row == 1:
            return QSize(100, 100)

        elif row == 2:
            return QSize(150, 150)

        return super().sizeHint(option, index)

    def createEditor(self, parent, option, index):


        lineEdit = super().createEditor(parent, option, index)

        return lineEdit

    

def main():

    app = QApplication()

    listWidget = QListWidget()

    l1 = QListWidgetItem(
        QIcon(":/images/cat458A8400_TP_V4.jpg"),
        "item0",
        listWidget)
    
    l1.setFlags(l1.flags()|Qt.ItemIsEditable)


    l2 = QListWidgetItem(
        QIcon(":/images/HIRAkotatuneko_TP_V4.jpg"),
        "item1",
        listWidget)
    
    l2.setFlags(l2.flags()|Qt.ItemIsEditable)
    
    l3 = QListWidgetItem(
        QIcon(":/images/PPW_utatanewosuruneko_TP_V4.jpg"),
        "item2",
        listWidget)
    
    l3.setFlags(l3.flags()|Qt.ItemIsEditable)
    
    delegate = StyledItemDelegate()
    listWidget.setItemDelegate(delegate)

    listWidget.setIconSize(QSize(150, 150))  
    listWidget.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

