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

from listwidget_01 import ListWidgetItem, ListWidget

class TableWidget(QTableWidget):

    def __init__(self, row, col, parent=None):

        super().__init__(row, col, parent)


        self.setDragDropMode(QTableWidget.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)

    
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
    
