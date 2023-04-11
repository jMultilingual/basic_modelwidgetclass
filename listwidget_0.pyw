from PySide6.QtWidgets import (QApplication,
                               QListWidgetItem,
                               QListWidget)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
import sys
import resources

def main():

    app = QApplication()

    listWidget = QListWidget()

    l1 = QListWidgetItem(
        QIcon(":/images/cat458A8400_TP_V4.jpg"),
        "item0",
        listWidget)

    l2 = QListWidgetItem(
        QIcon(":/images/HIRAkotatuneko_TP_V4.jpg"),
        "item1",
        listWidget)
    l3 = QListWidgetItem(
        QIcon(":/images/PPW_utatanewosuruneko_TP_V4.jpg"),
        "item2",
        listWidget)

    size = QSize(50, 50)
    l1.setSizeHint(size)
    l2.setSizeHint(size)
    l3.setSizeHint(size)
    listWidget.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
