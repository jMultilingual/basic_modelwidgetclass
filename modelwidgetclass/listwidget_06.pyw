from PySide6.QtWidgets import (QApplication,
                               QListWidgetItem,
                               QListWidget,
                               QStyledItemDelegate,
                               QItemEditorFactory,
                               QItemEditorCreatorBase)
from PySide6.QtGui import QIcon, QFont, QBrush, QColor
from PySide6.QtCore import (QSize, Qt, QMetaType, QSaveFile, QFile,
                            QIODevice, QByteArray, QMimeData,QDataStream)
                            
import sys
import resources

QListWidgetItem.FlagIsReadWrite = QListWidgetItem.UserType

class QDataStream(QDataStream):

    def __lshift__(self, data):

        if isinstance(data, QListWidgetItem):
            super().__lshift__(data)
            self.writeUInt16(data.flags().value)

        else:
            super().__lshift__(data)

    def __rshift__(self, data):

        if isinstance(data, QListWidgetItem):
            super().__rshift__(data)
            data.setFlags(Qt.ItemFlags(self.readUInt16()))
            
    

class RangeSpinBoxItemEditorCreatorBase(QItemEditorCreatorBase):

    def __init__(self):
        super().__init__()

        self.propertyName = QByteArray(
            QSpinBox.staticMetaObject.userProperty().name()
            )

    def createWidget(self, parent):

        rangeSpinBox = QSpinBox(minimum=0, maximum=0, parent=parent)
        return rangeSpinBox

    def valuePropertyName(self, userType):

        return self.propertyName

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
                            QMetaType.User, parent)
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

        self.setSelectionMode(QListWidget.ContiguousSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDefaultDropAction(Qt.MoveAction)
        

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
            Qt.ItemIsEditable|Qt.ItemIsUserTristate)     
        

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
            Qt.ItemIsEditable|Qt.ItemIsUserTristate)   
        
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
            Qt.ItemIsEditable|Qt.ItemIsUserTristate)
        
        delegate = StyledItemDelegate()
        self.setItemDelegate(delegate)

        self.setIconSize(QSize(150, 150))  
        

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
        item = ListWidgetItem(
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

    def mimeTypes(self):

        return ['application/x-qabstractitemmodeldatalist',
                'text/uri-list']

      
    def mimeData(self, indexes):

        qb = QByteArray()
        out = QDataStream(qb, QIODevice.WriteOnly)

        for index in indexes:
            out << index
            
        mimeData = QMimeData()
        mimeData.setData(self.mimeTypes()[0], qb)
        return mimeData

    def dropMimeData(self, index, data, action):

  
        if data.hasUrls():
            url = data.urls()[0]
            font = QFont("Arial", 72)
            icon = QIcon(url.fileName())
            text = "item3"
            foreground = QBrush(QColor(230, 123, 249))
            background = QBrush(QColor(123, 240, 111))
            alignment = Qt.AlignLeft
            toolTip = "External Drop Neko"
            checkState = Qt.CheckState.Checked
            sizeHint = QSize(200, 200)
            
            self.addListWidgetItem(icon,
                           text,
                           font,
                           foreground,
                           background,
                           alignment,
                           toolTip,
                           checkState,
                           sizeHint,
                           flags=Qt.ItemIsEditable|
                           Qt.ItemIsUserTristate
                           )

            return True

        else:
            qb = data.data(self.mimeTypes()[0])
            out = QDataStream(qb, QIODevice.ReadOnly)

            while not out.atEnd():
                item = ListWidgetItem()
                out >> item
                
                self.insertItem(index, item)

            return True

        

        return False

##    def showEvent(self, event):
##
##        self.load()
##        super().showEvent(event)
##
##    def closeEvent(self, event):
##
##        self.save()
##        super().closeEvent(event)
##
##    def save(self):
##
##        file = QSaveFile("dummy.dat")
##
##        if file.open(QIODevice.WriteOnly):
##
##            out = QDataStream(file)
##            for i in range(self.count()):
##                item = self.item(i)
##                item.write(out)
##        file.commit()
##
##    def load(self):        
##        
##        file = QFile("dummy.dat")
##        if file.exists():
##            if file.open(QIODevice.ReadOnly):
##
##                self.clear()
##                out = QDataStream(file)
##
##                while not out.atEnd():
##                    item = ListWidgetItem()
##                    item.read(out)
##                    item.setFlags(item.flags()|
##                                  Qt.ItemIsEditable|
##                                  Qt.ItemIsUserTristate)
##
##                    self.addItem(item)
##        file.close()


class ListWidgetItem(QListWidgetItem):

    def __init__(self, icon=QIcon(),
                         text="",
                         parent=None):
        super().__init__(icon ,
                         text ,
                         parent,
                         type=QListWidgetItem.FlagIsReadWrite)

        def write(self, out):

            super().write(out)
            out.writeUInt16(
                            self.flags().value
                            )

        def read(self, out):

            super().read(out)
            self.setFlags(Qt.ItemFlag(
                            out.readUInt16())
                          )
    
            
        
def main():

    app = QApplication()

    listWidget = ListWidget()
    listWidget.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

