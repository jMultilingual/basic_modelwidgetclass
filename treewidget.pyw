from PySide6.QtWidgets import (
                                QApplication,
                               QTreeWidget,
                                QTreeWidgetItem,
                                QTreeWidgetItemIterator,
                                
                               QWidget,
                               QHBoxLayout
                               )

from PySide6.QtGui import QIcon, QFont, QBrush, QColor
from PySide6.QtCore import (QSize, Qt, QFile, QIODevice, QSaveFile,
                            QByteArray, QDataStream,QMimeData)

import sys, uuid
import resources

from listwidget import ListWidgetItem, ListWidget
from tablewidget import TableWidgetItem, TableWidget


class TreeWidget(QTreeWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragDropMode(QTreeWidget.DragDrop)

    def mimeTypes(self):
        

        return ['application/x-qabstractitemmodeldatalist',
                "application/x-qt-windows-mime;value=\"Shell IDList Array\"",
                'application/x-qabstracttablewidgetdatalist'
                ]

    def dropMimeRead(self, index, out, parent):

        font = QFont()
        icon = QIcon()
        foreground = QBrush()
        background = QBrush()
        sizeHint = QSize()

        out >> font
        out >> icon
        text = out.readQString()
        out >> foreground
        out >> background

        alignment = Qt.Alignment(out.readUInt16())
        toolTip = out.readQString()
        checkState = Qt.CheckState(out.readInt8())
        out >> sizeHint
        flags = Qt.ItemFlag(out.readUInt32())

        _index = self.indexFromItem(index)
        column = _index.column()
        item = TreeWidgetItem()
        item.setIcon(column, icon)
        item.setText(column, text)
        item.setFont(column, font)
        item.setForeground(column, foreground)
        item.setBackground(column, background)
        item.setTextAlignment(column, alignment)
        item.setToolTip(column, toolTip)
        item.setSizeHint(column, sizeHint)
        item.setFlags(flags|Qt.ItemIsDropEnabled)
        if parent is None:
            self.insertTopLevelItem(index, item)
        else:
            parent.insertChild(index, item)

    def mimeData(self, indexes):

        qb = QByteArray()
        out = QDataStream(qb, QIODevice.WriteOnly)

        
        
        for  index in indexes:            
            _index = self.indexFromItem(index)
 
            column = _index.column()
            out << index.font(column)
            out << index.icon(column)
            out.writeQString(index.text(column))
            out << index.foreground(column)
            out << index.background(column)
            out.writeUInt16(index.textAlignment(column))
            out.writeQString(index.toolTip(column))
            out.writeUInt8(index.checkState(column).value)
            out << index.sizeHint(column)
            out.writeUInt32(index.flags().value)

        mimeData = QMimeData()
        mimeData.setData('application/x-qabstractitemmodeldatalist', qb)
        return mimeData
        
        
    

    def dropMimeData(self, parent, index, data, action):


        if data.hasFormat('application/x-qabstractitemmodeldatalist'):

            data = data.data('application/x-qabstractitemmodeldatalist')
            out = QDataStream(data, QIODevice.ReadOnly)

            while not out.atEnd():
                
                self.dropMimeRead(index, out, parent)
            

            if action == Qt.CopyAction:
                return False

            elif action == Qt.MoveAction:
                return True

        elif data.hasFormat('application/x-qabstracttablewidgetdatalist'):

            data = data.data('application/x-qabstracttablewidgetdatalist')
            out = QDataStream(data, QIODevice.ReadOnly)

            while not out.atEnd():

                if out.readBool():
                
                    self.dropMimeRead(index, out, parent)

            if action == Qt.CopyAction:
                return False

            elif action == Qt.MoveAction:
                return True

        return False

    

    def showEvent(self, event):

        self.load()
        
        return super().showEvent(event)
    
    def closeEvent(self, event):

        self.save()

        
        return super().closeEvent(event)

    def save(self):

        it = QTreeWidgetItemIterator(self)
        f = QSaveFile("dummy_tree.dat")
        if f.open(QIODevice.WriteOnly):

            out = QDataStream(f)

            while it.value():

                treeitem = it.value()
                treeitem.write(out)

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
                    treeitem.read(out)
                    dic[treeitem._id] = treeitem
                    if treeitem._expanded:
                        expanded.append(treeitem._id)

                    if dic[treeitem._pid] != -1:
                        if dic[treeitem._pid].indexOfChild(treeitem):
                            dic[treeitem._pid].addChild(treeitem)


                    else:
                        self.addTopLevelItem(treeitem)

      
                for t in expanded:
                    dic[t].setExpanded(True)
                    
class Dic(dict):

    def __missing__(self, key):
        return -1


class TreeWidgetItem(QTreeWidgetItem):

    def __init__(self, type=QTreeWidgetItem.UserType):
        super().__init__(type)

        self._id = str(uuid.uuid4())
        self._pid = ""

    def write(self, out):

        super().write(out)
        out.writeQString(self._id)
        out.writeQString(self._pid)
        out.writeBool(self.isExpanded())
        out.writeUInt32(self.flags().value)

    def read(self, out):

        super().read(out)
        self._id = out.readQString()
        self._pid = out.readQString()
        self._expanded = out.readBool()        
        self.setFlags(Qt.ItemFlags(out.readUInt32()))
        
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

        


class CloseWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    def closeEvent(self, event):

        children = self.children()
        for child in children:

            if isinstance(child, TreeWidget):
                child.save()


        return super().closeEvent(event)
    

    
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
    
