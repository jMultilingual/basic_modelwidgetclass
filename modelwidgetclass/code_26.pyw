from PySide6.QtWidgets import (
                                QApplication,
                               QTableWidget,
                                QTableWidgetItem,
                               QWidget,
                               QHBoxLayout,
                                QListWidgetItem
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

class QDataStream(QDataStream):

    def __lshift__(self, data):

        if isinstance(data, QTableWidgetItem):
            super().__lshift__(data)
            self.writeUInt16(data.flags().value)

        else:
            super().__lshift__(data)

    def __rshift__(self, data):

        if isinstance(data, QTableWidgetItem):
            super().__rshift__(data)
            data.setFlags(Qt.ItemFlags(self.readUInt16()))
            
class TableWidget(QTableWidget):

    def __init__(self, row, col, parent=None):

        super().__init__(row, col, parent)


        self.setDragDropMode(QTableWidget.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)

    def showEvent(self, event):

        self.load()

        return super().showEvent(event)

    def closeEvent(self, event):

        self.save()

        return super().closeEvent(event)

    def save(self):

        file = QSaveFile("dummy_table.dat")
        if file.open(QIODevice.WriteOnly):
            out = QDataStream(file)
            out.writeUInt16(self.rowCount())
            out.writeUInt16(self.columnCount())
            for r in range(self.rowCount()):
                for c in range(self.columnCount()):
                    item = self.item(r, c)
                    
                    out << item
        file.commit()

    def load(self):

        file = QFile("dummy_table.dat")
        if file.exists():

            if file.open(QIODevice.ReadOnly):

                out = QDataStream(file)
                row = out.readUInt16()
                col = out.readUInt16()
                for r in range(row):
                    for c in range(col):
                        item = QTableWidgetItem()
                        out >> item
                        self.setItem(r, c, item)
        file.close()
    def mimeData(self, indexes):

        qb = QByteArray()
        out = QDataStream(qb, QIODevice.WriteOnly)

        for index in indexes:
            
            out << index

        mimeData = QMimeData()
        mimeData.setData(self.mimeTypes()[0], qb)
        return mimeData

    def dropMimeData(self, row, column, data, action):

        qb = data.data(self.mimeTypes()[0])
        out = QDataStream(qb, QIODevice.ReadOnly)

        count = row
        while not out.atEnd():
            item = QTableWidgetItem()
            out >> item           
            self.setItem(count, column, item)
            count += 1
        return False


class CloseWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

    def closeEvent(self, event):

        for child in self.children():
            if isinstance(child, QTableWidget):
                child.save()

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
    
