from PySide6.QtWidgets import (QApplication,
                               QListWidgetItem,
                               QListWidget,
                               QStyledItemDelegate,
                               QItemEditorFactory)
from PySide6.QtGui import QIcon, QFont, QBrush, QColor
from PySide6.QtCore import QSize, Qt, QMetaType
import sys
import resources

class ItemEditorFactory(QItemEditorFactory):

    def __init__(self):
        super().__init__()
        

class StyledItemDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super().__init__(parent)

        itemEditorFactory = ItemEditorFactory()
        self.setItemEditorFactory(itemEditorFactory)
        

    def initStyleOption(self, option, index):

        super().initStyleOption(option, index)
        option.toolTip = index.data(Qt.ToolTipRole)
        option.decorationSize = self.sizeHint(option, index)
        
    def paint(self, painter, option, index):
        

        super().paint(painter, option, index)

    def sizeHint(self, option, index):

        return index.data(Qt.SizeHintRole)

    def createEditor(self, parent, option, index):

        self.initStyleOption(option, index)
        if index.row() == 0:
            lineEdit = self.itemEditorFactory().createEditor(
                            QMetaType.QString, parent)
            lineEdit.setFont(option.font)
            return lineEdit

        elif index.row() == 1:
            spinBox = self.itemEditorFactory().createEditor(
                            QMetaType.Int, parent)
            spinBox.setFont(option.font)
            return spinBox

        elif index.row() == 2:
            comboBox = self.itemEditorFactory().createEditor(
                            QMetaType.Bool, parent)
            comboBox.addItems(["0", "1", "2"])
            comboBox.setFont(option.font)
            return comboBox

    def updateEditorGeometry(self, editor, option, index):

        editor.setGeometry(option.rect)
    
class ListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.addListWidgetItem(
            QIcon(":/images/cat458A8400_TP_V4.jpg"),
            "item0",
            QFont("Times New Roman", 18),
            QBrush(QColor(105, 171, 197)),
            QBrush(QColor(237, 232, 150)),
            Qt.AlignVCenter|Qt.AlignLeft,
            "Tool Tip Neko1",
            Qt.CheckState.Checked,
            QSize(50, 50),
            Qt.ItemIsEditable)     
        

        self.addListWidgetItem(
            QIcon(":/images/HIRAkotatuneko_TP_V4.jpg"),
            "item1",
            QFont("Segoe UI Light", 36),
            QBrush(QColor(246, 241, 214)),
            QBrush(QColor(117, 101, 93)),
            Qt.AlignVCenter|Qt.AlignHCenter,
            "Tool Tip Neko1",
            Qt.CheckState.PartiallyChecked,
            QSize(100, 100),
            Qt.ItemIsEditable)   
        
        self.addListWidgetItem(
            QIcon(":/images/PPW_utatanewosuruneko_TP_V4.jpg"),
            "item2",
            QFont("Segoe UI Black", 72),
            QBrush(QColor(176, 229, 213)),
            QBrush(QColor(213, 187, 216)),
            Qt.AlignVCenter|Qt.AlignRight,
            "Tool Tip Neko1",
            Qt.CheckState.PartiallyChecked,
            QSize(150, 150),
            Qt.ItemIsEditable)
        
        delegate = StyledItemDelegate()
        self.setItemDelegate(delegate)

        self.setIconSize(QSize(150, 150))  
        self.show()

    def addListWidgetItem(self,
                          icon,
                          text,
                          font,
                          foreground,
                          background,
                          alignment,
                          toolTip,
                          checkState,
                          sizeHint,
                          flags=Qt.ItemIsEnabled):
        item = QListWidgetItem(
            QIcon(icon), text)

        item.setFont(font)
        item.setForeground(foreground)
        item.setBackground(background)
        item.setTextAlignment(alignment)
        item.setToolTip(toolTip)
        item.setCheckState(checkState)
        item.setSizeHint(sizeHint)
        item.setFlags(item.flags()|flags)

        self.addItem(item)
        
def main():

    app = QApplication()

    listWidget = ListWidget()  

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

