from PySide6.QtWidgets import (
                                QApplication,
                               QTableWidget,
                                QTableWidgetItem,
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

from listwidget_04 import ListWidgetItem, ListWidget

class TableWidget(QTableWidget):

    def __init__(self, row, col, parent=None):

        super().__init__(row, col, parent)


        self.setDragDropMode(QTableWidget.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)

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

        while not out.atEnd():

            item = QTableWidgetItem()
            out >> item
            self.setItem(row, column, item)

        return False

    
def main():

    app = QApplication()
    widget = QWidget()
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
    
