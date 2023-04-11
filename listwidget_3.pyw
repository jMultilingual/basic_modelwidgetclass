from PySide6.QtWidgets import (QApplication,
                               QListWidgetItem,
                               QListWidget,
                               QStyledItemDelegate,
                               QSpinBox,
                               QComboBox,
                               QItemEditorFactory,
                               QItemEditorCreatorBase
                               )
from PySide6.QtGui import QIcon, QFont, QBrush, QColor
from PySide6.QtCore import (QSaveFile, QFile, QIODevice, QDataStream,
                            QSize, Qt, QMetaType, QByteArray)
import sys
import resources

class RangeSpinBoxItemEditorCreatorBase(QItemEditorCreatorBase):

    def __init__(self):
        super().__init__()

        self.propertyName = QByteArray(
            QSpinBox.staticMetaObject.userProperty().name()
            )

    def createWidget(self, parent):

        rangeSpinBox = QSpinBox(minimum=0, maximum=10, parent=parent)

        return rangeSpinBox

    def valuePropertyName(self, userType):

        return self.propertyName
        

class ItemEditorFactory(QItemEditorFactory):

    def __init__(self):

        super().__init__()

        self.registerEditor(
            QMetaType.User,
             RangeSpinBoxItemEditorCreatorBase()
            )
        

class StyledItemDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super().__init__(parent)

        itemEditorFactory = ItemEditorFactory()
        self.setItemEditorFactory(itemEditorFactory)

    def initStyleOption(self, option, index):

        super().initStyleOption(option, index)
     
        toolTip = index.data(Qt.ToolTipRole)
   
        option.toolTip = toolTip

        option.decorationSize = self.sizeHint(option, index)
        
            

    def paint(self, painter, option, index):
        

        super().paint(painter, option, index)

    def sizeHint(self, option, index):

        row = index.row()
        if row == 0:
            return QSize(50, 50)

        elif row == 1:
            return QSize(100, 100)

        elif row == 2:
            return QSize(150, 150)

        return super().sizeHint(option, index)

    def createEditor(self, parent, option, index):

        self.initStyleOption(option, index)
        if index.row() == 0:
            
            lineEdit = super().createEditor(parent, option, index)

            return lineEdit
        
        elif index.row() == 1:
            spinBox = self.itemEditorFactory().createEditor(
                QMetaType.User, parent
                )
            
            spinBox.setFont(option.font)
            return spinBox

        elif index.row() == 2:
            comboBox =  self.itemEditorFactory().createEditor(
                QMetaType.Bool, parent
                )
            comboBox.clear()
            comboBox.addItems(["0", "1", "2"])
            comboBox.setFont(option.font)
            return comboBox

        return super().createEditor(parent, option, index)

class ListWidgetItem(QListWidgetItem):

    def __init__(self, icon=QIcon(), text="", parent=None):
        super().__init__(icon, text, parent)

    def write(self, out):
        super().write(out)
        out.writeUInt32(self.flags().value)

    def read(self, out):
        super().read(out)
        self.setFlags(Qt.ItemFlag(out.readUInt32()))
        
                      
class ListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDragDropOverwriteMode(True)
        

        delegate = StyledItemDelegate()
        self.setItemDelegate(delegate)

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
            Qt.ItemIsEditable|Qt.ItemIsUserTristate|Qt.ItemIsDropEnabled)     
        

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
            Qt.ItemIsEditable|Qt.ItemIsUserTristate|Qt.ItemIsDropEnabled)   
        
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
            Qt.ItemIsEditable|Qt.ItemIsUserTristate|Qt.ItemIsDropEnabled)

    def mimeTypes(self):

        return ["application/x-qabstractitemmodeldtalist",
                "application/x-qt-windows-mime;value=\"Shell IDList Array\""
                ]
    

    def dragEnterEvent(self, event):

        return super().dragEnterEvent(event)

    def dragMoveEvent(self, event):

        return super().dragMoveEvent(event)

    def dropEvent(self, event):

        return super().dropEvent(event)

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
            print(action)
            if action == Qt.MoveAction:
                print(self.dragDropOverwriteMode())
                if self.dragDropOverwriteMode():
                 
                    item = self.clone(icon,
                           text,
                           font,
                           foreground,
                           background,
                           alignment,
                           toolTip,
                           checkState,
                           sizeHint,
                           flags=Qt.ItemIsEditable|
                           Qt.ItemIsUserTristate|Qt.ItemIsDropEnabled
                                      )
                    self.takeItem(index)
                    self.addItem(item)
         
                    
                else:
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
                           Qt.ItemIsUserTristate|Qt.ItemIsDropEnabled
                           )

            elif action == Qt.CopyAction:                
                    
                if self.dropIndicatorPosition() == QListWidget.OnItem:                    

                    item = self.clone(icon,
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
                    if self.dragDropOverwriteMode():
                        self.takeItem(index)
                        self.insertItem(index, item)
                        return True
                    
                    else:
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
                           Qt.ItemIsUserTristate|Qt.ItemIsDropEnabled
                           )
                        return False
                        
                else:
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
                           Qt.ItemIsUserTristate|Qt.ItemIsDropEnabled
                           )


                
                
            return True

        return False
            
    

    def save(self):

        file = QSaveFile("dummy.dat")

        if file.open(QIODevice.WriteOnly):

            out = QDataStream(file)
            for i in range(self.count()):
                item = self.item(i)
                item.write(out)
        file.commit()

    def load(self):        
        
        file = QFile("dummy.dat")
        if file.exists():
            if file.open(QIODevice.ReadOnly):

                self.clear()
                out = QDataStream(file)

                while not out.atEnd():
                    item = ListWidgetItem()
                    item.read(out)

                    self.addItem(item)
        file.close()
        
    def showEvent(self, event):

        self.load()
        super().showEvent(event)

    def closeEvent(self, event):

        self.save()
        super().closeEvent(event)

    def clone(self, icon,
                          text,
                          font,
                          foreground,
                          background,
                          alignment,
                          toolTip,
                          checkState,
                          sizeHint,
                          flags=Qt.ItemIsEnabled|Qt.ItemIsUserTristate|Qt.ItemIsDropEnabled):
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

        return item
        
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
                          flags=Qt.ItemIsEnabled|Qt.ItemIsDropEnabled):
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

    
        
        
        
def main():

    app = QApplication()

    listWidget = ListWidget()   
    
    listWidget.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

