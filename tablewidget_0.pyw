from PySide6.QtWidgets import (
                                QApplication,
                               QTableWidget,
                                QTableWidgetItem,
                               QWidget,
                               QHBoxLayout
                               )

from PySide6.QtGui import QIcon, QFont, QBrush, QColor
from PySide6.QtCore import (QSize, Qt, QFile, QIODevice, QSaveFile,
                            QByteArray, QDataStream,QMimeData)

import sys
import resources

from listwidget import ListWidgetItem, ListWidget

class TableWidget(QTableWidget):

    def __init__(self, row, col, parent=None):

        super().__init__(row, col, parent)


        self.setDragDropMode(QTableWidget.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)



    def mimeTypes(self):
        

        return ['application/x-qabstractitemmodeldatalist',
                "application/x-qt-windows-mime;value=\"Shell IDList Array\"",
                'application/x-qabstracttablewidgetdatalist'
                ]

        

    def mimeData(self, indexes):

        qb = QByteArray()
        out = QDataStream(qb, QIODevice.WriteOnly)
        
        for num, index in enumerate(indexes):

    
            if index is None:
                out.writeBool(False)
                continue

            else:
                out.writeBool(True)
            out << index.font()
            out << index.icon()
            out.writeQString(index.text())
            out << index.foreground()
            out << index.background()
            out.writeUInt16(index.textAlignment())
            out.writeQString(index.toolTip())
            out.writeUInt8(index.checkState().value)
            out << index.sizeHint()
            out.writeUInt32(index.flags().value)

        mimeData = QMimeData()
        mimeData.setData('application/x-qabstracttablewidgetdatalist', qb)
        return mimeData

    def dropMimeData(self, row, column, data, action):

   
        qb = data.data('application/x-qabstractitemmodeldatalist')
        out = QDataStream(qb, QIODevice.ReadOnly)

        count = row
        while not out.atEnd():

            font = QFont()
            icon = QIcon()
            foreground = QBrush()
            background = QBrush()
            size = QSize()

            item = QTableWidgetItem()
            out >> font
            item.setFont(font)
            out >> icon
            item.setIcon(icon)
            item.setText(out.readQString())
            out >> foreground
            out >> background
            item.setForeground(foreground)
            item.setBackground(background)
            item.setTextAlignment(Qt.Alignment(out.readUInt16()))
            item.setToolTip(out.readQString())
            item.setCheckState(Qt.CheckState(out.readUInt8()))

            out >> size
            item.setSizeHint(size)
            item.setFlags(Qt.ItemFlags(out.readUInt32()))
            self.setItem(count, column, item)
            count += 1

        return True

##    def save(self):
##
##        file = QSaveFile("dummy_table.dat")
##        if file.open(QIODevice.WriteOnly):
##            out = QDataStream(file)
##            out.writeUInt16(self.rowCount())
##            out.writeUInt16(self.columnCount())
##            for r in range(self.rowCount()):
##                for c in range(self.columnCount()):
##                    item = self.item(r, c)
##
##                    if item:
##                        out.writeBool(True)
##                        item.write(out)
##                    else:
##                        out.writeBool(False)
##
##        file.commit()
##
##    def load(self):
##
##        file = QFile("dummy_table.dat")
##        if file.exists():
##
##            if file.open(QIODevice.ReadOnly):
##                out = QDataStream(file)
##                row = out.readUInt16()
##                col = out.readUInt16()
##                for r in range(row):
##                    for c in range(col):
##                        item = QTableWidgetItem()
##                        isItem = out.readBool()
##
##                        if isItem:
##                            item.read(out)
##                            self.setItem(r, c, item)
##        file.close()
##
##    def showEvent(self, event):
##
##        self.load()
##        return super().showEvent(event)
##    
##    def closeEvent(self, event):
##
##        self.show()
##        return super().closeEvent(event)

class CloseWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    def closeEvent(self, event):

        children = self.children()
        for child in children:

            if isinstance(child, TableWidget):
                child.save()
                print(222)

        return super().closeEvent(event)
    

    
def main():

    app = QApplication()

    widget = CloseWidget()
    hlayout = QHBoxLayout()
    listWidget = ListWidget()
    tableWidget = TableWidget(12, 10)
    hlayout.addWidget(listWidget)
    hlayout.addWidget(tableWidget)
    widget.setLayout(hlayout)
    widget.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
