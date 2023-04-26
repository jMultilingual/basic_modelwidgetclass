from PySide6.QtWidgets import (
                                QApplication,
                               QTreeWidget,
                                QTreeWidgetItem,
                                QTableWidgetItem,
                                QListWidgetItem,
                                QTreeWidgetItemIterator,
                               QWidget,
                               QHBoxLayout
                               )

from PySide6.QtGui import QIcon, QFont, QBrush, QColor
from PySide6.QtCore import (QSize,
                            Qt,
                            QFile, QIODevice, QSaveFile,
                            QByteArray,
                            QDataStream,QMimeData)
import sys
import resources

from listwidget_06 import ListWidgetItem, ListWidget
from tablewidget_01 import TableWidget

class QDataStream(QDataStream):

    def __lshift__(self, data):

        if isinstance(data, QTreeWidgetItem):
            super().__lshift__(data)
            self.writeUInt16(data.flags().value)

        elif isinstance(data, QListWidgetItem):
            super().__lshift__(data)
            self.writeUInt16(data.flags().value)
        
        elif isinstance(data, QTreeWidgetItem):
            super().__lshift__(data)
            self.writeUInt16(data.flags().value)

        else:
            super().__lshift__(data)

    def __rshift__(self, data):
        
        if isinstance(data, (QListWidgetItem, QTableWidgetItem, QTreeWidgetItem)):
           
            super().__rshift__(data)  
            data.setFlags(Qt.ItemFlags(self.readUInt16()))

        else:
            super().__rshift__(data)
            
class TreeWidget(QTreeWidget):

    def __init__(self, parent=None):

        super().__init__( parent)


        self.setDragDropMode(QTreeWidget.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setColumnCount(3)
    

    def mimeData(self, indexes):

        qb = QByteArray()
        out = QDataStream(qb, QIODevice.WriteOnly)

        for index in indexes:
            
            out << index

        mimeData = QMimeData()
        mimeData.setData(self.mimeTypes()[0], qb)
        return mimeData

    def dropMimeData(self, parent, index, data, action):

        if data.hasFormat(self.mimeTypes()[0]):

            data = data.data(self.mimeTypes()[0])
            out = QDataStream(data, QIODevice.ReadOnly)

            while not out.atEnd():
                
                listItem = QListWidgetItem()
                out >> listItem               
                item = QTreeWidgetItem()
                item.setFont(0, listItem.font())
                item.setText(0, listItem.text())
                item.setIcon(0, listItem.icon())
                item.setTextAlignment(0, Qt.AlignmentFlag(listItem.textAlignment()))
                item.setForeground(0, listItem.foreground())
                item.setBackground(0, listItem.background())
                item.setSizeHint(0, listItem.sizeHint())
                item.setCheckState(0, listItem.checkState())
                item.setFlags(listItem.flags()|Qt.ItemIsDropEnabled)
                if parent is None:
                    self.insertTopLevelItem(index, item)
                else:          
                    
                    parent.insertChild(index, item)
                    
            if action == Qt.CopyAction:
                return False

            elif action == Qt.MoveAction:
                return True

        return False


class CloseWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

    
    

    
def main():

    app = QApplication()
    widget = CloseWidget()
    hlayout = QHBoxLayout()
    listWidget = ListWidget()
    tableWidget = TableWidget(12, 10)
    treeWidget = TreeWidget()
    hlayout.addWidget(listWidget)
    hlayout.addWidget(tableWidget)
    hlayout.addWidget(treeWidget)
    widget.setLayout(hlayout)
    widget.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
