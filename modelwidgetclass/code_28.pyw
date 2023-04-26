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
import uuid

from listwidget_06 import ListWidgetItem, ListWidget
from tablewidget_01 import TableWidget

class Dic(dict):

    def __missing__(self, key):

        return -1

class QDataStream(QDataStream):

    def __lshift__(self, data):
        
        if isinstance(data, TreeWidgetItem):
            
            super().__lshift__(data)                           
            self.writeUInt16(
                data.flags().value
                )
            self.writeQString(
                data._id
                )
            self.writeQString(
                data._pid
                )
            self.writeBool(
                data.isExpanded()
                )
            
        elif isinstance(data, QTreeWidgetItem):
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
        
        if isinstance(data, TreeWidgetItem):
            super().__rshift__(data)
            data.setFlags(
                Qt.ItemFlags(
                    self.readUInt16()
                    )
                )            
            data._id = self.readQString()
            data._pid = self.readQString()            
            data._expanded = self.readBool()
            
            
        elif isinstance(data, (QListWidgetItem, QTableWidgetItem, QTreeWidgetItem)):
           
            super().__rshift__(data)  
            data.setFlags(Qt.ItemFlags(self.readUInt16()))

        else:
            super().__rshift__(data)

class TreeWidgetItem(QTreeWidgetItem):

    def __init__(self, parent=None):
        super().__init__(parent, type=QTreeWidgetItem.UserType)

        self._id = str(uuid.uuid4())
        self._pid = ""

    def addChild(self, child):
        super().addChild(child)
        child._pid = self._id

    def addChildren(self, children):
        super().addChildren(children)
        for child in children:
            child._pid = self._id

    def insertChild(self, index, child):
        super().insertChild(index, child)
        child._pid = self._id

    def insertChildren(self, index, children):
        super().insertChildren(index, children)
        for child in children:
            self._pid = self._id
    

class TreeWidget(QTreeWidget):

    def __init__(self, parent=None):

        super().__init__( parent)


        self.setDragDropMode(QTreeWidget.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)

    def closeEvent(self, event):

        self.save()

        return super().closeEvent(event)

    def showEvent(self, event):

        self.load()

        return super().showEvent(event)

    def save(self):
        
        it = QTreeWidgetItemIterator(self)
        f = QSaveFile("dummy_tree.dat")
        if f.open(QIODevice.WriteOnly):

            out = QDataStream(f)

            while it.value():
                
                treeitem = it.value()
                
                out << treeitem
                it += 1

        f.commit()
        
    def load(self):
        expanded = []
        dic = Dic()
        f = QFile("dummy_tree.dat")
        if f.exists():
            if f.open(QIODevice.ReadOnly):
                out = QDataStream(f)              
                while not out.atEnd():
                    treeitem = TreeWidgetItem()
                    out >> treeitem
                    dic[
                        treeitem._id
                        ] = treeitem
                    if treeitem._expanded:
                        expanded.append(treeitem._id)
                    if dic[treeitem._pid] != -1:
                        if dic[
                            treeitem._pid
                            ].indexOfChild(
                                treeitem
                                ):
                            dic[
                                treeitem._pid
                                ].addChild(
                                    treeitem
                                    )                        
                    else:
                        self.addTopLevelItem(
                            treeitem
                            )
            for t in expanded:
                dic[t].setExpanded(True)
                del dic[t]._expanded
    
    

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
                item = TreeWidgetItem()
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

    def closeEvent(self, event):

        for child in self.children():

            if isinstance(child, QTreeWidget):

                child.save()
    
    

    
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
    
