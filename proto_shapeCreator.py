from PySide.QtGui import *
from PySide.QtCore import *

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.view = View(self)
        self.button = QPushButton('Clear View', self)
        self.buttonc = QPushButton('Color', self)
        self.button.clicked.connect(self.handleClearView)
        self.buttonc.clicked.connect(self.changecolor)

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.button)

    def handleClearView(self):
        shape = Shape()
        self.view.shape.append(shape)
        self.view.id += 1
        self.view.scene().addItem(self.view.shape[self.view.id])
        self.view.start_draw = True

    def changecolor(self):
        self.view.scene().selectedItems()[0].color = QColor(255, 255, 255)



class View(QGraphicsView):
    def __init__(self, parent):
        QGraphicsView.__init__(self, parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QColor(70, 70, 70))
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(Qt.IntersectsItemShape)
        self.setScene(QGraphicsScene(self))
        self.setSceneRect(QRectF(self.viewport().rect()))
        self.start_draw = False
        self.shape = []
        self.id = -1

    def mousePressEvent(self, event):
        if not self.start_draw:
            return QGraphicsView.mousePressEvent(self, event)
        if self.shape[self.id].first_point:
            self.shape[self.id].start_point(self.mapToScene(event.pos()))
        else:
            self.shape[self.id].add_point(self.mapToScene(event.pos()))
        self.scene().update()
        QGraphicsView.mousePressEvent(self, event)


    def keyPressEvent(self, event):
        super(View, self).keyPressEvent(event)
        if event.key() == Qt.Key_Return:
            #close the shape
            self.shape[self.id].add_point(self.shape[self.id].begin_point)
            self.start_draw = False
            print self.shape[self.id].vertex



class Shape(QGraphicsItem):
    def __init__(self):
        super(Shape, self).__init__()
        self.setFlags(
            QGraphicsItem.ItemIsFocusable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemSendsGeometryChanges
        )

        # self.setAcceptHoverEvents(True)
        # self.setSelected(True)

        self.rect = QRect()
        self.first_point = True
        self.path_draw = QPainterPath()
        self.color = QColor(0.0, 220.0, 0.0)
        self.light_color = self.color.lighter(150)
        self.begin_point = None
        self.vertex = []

    def start_point(self, point):
        self.begin_point = point
        self.path_draw.moveTo(point)
        self.first_point = False
        self.vertex.append(point)

    def add_point(self, point):
        self.path_draw.lineTo(point)
        self.vertex.append(point)

    def boundingRect(self):
        return QRect(self.path_draw.controlPointRect().toRect())

    def paint(self, painter, option, widget):
        if self.isSelected():
            painter.setBrush(self.light_color)
            painter.setBrush(self.light_color)
        else:
            painter.setPen(self.color)
            painter.setBrush(self.color)
        painter.drawPath(self.path_draw)
        painter.setPen(QColor(255,0,0))
        painter.setBrush(Qt.NoBrush)
        #painter.drawRect(self.path_draw.controlPointRect())



    # def hoverEnterEvent(self, event):
    #     self.setSelected(True)
    #     print "prout"

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())