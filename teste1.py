from PySide import QtCore, QtGui
import sys
import weakref
import math


class Edge(QtGui.QGraphicsItem):
    
    Pi = math.pi
    TwoPi = 2.0*Pi

    Type = QtGui.QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode):
        QtGui.QGraphicsItem.__init__(self)
        
        self.arrowSize = 10.0
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.source = weakref.ref(sourceNode)
        self.dest = weakref.ref(destNode)
        self.source().addEdge(self)
        self.dest().addEdge(self)
        self.adjust()
        
    def type(self):
        return self.Type
    
    def sourceNode(self):
        return self.source()
    
    def setSourceNode(self, node):
        self.source = weakref.ref(node)
        self.adjust()
        
    def destNode(self):
        return self.dest()
    
    def setDestNode(self, node):
        self.dest = weakref.ref(node)
        self.adjust()
        
    def adjust(self):
        if not self.dest() or not self.source():
            return
        
        line = QtCore.QLineF(self.mapFromItem(self.source(), 20, 20), self.mapFromItem(self.dest(), 20, 20))
        length = line.length()
        
        if length == 0.0:
            return
        
        edgeOffset = QtCore.QPointF((line.dx() * 5)/length, (line.dy() * 5) / length)
        
        self.prepareGeometryChange()
        self.sourcePoint = line.p1() + edgeOffset
        self.destPoint = line.p2() - edgeOffset
    
    def boundingRect(self):
        if not self.source() or not self.dest():
            return QtCore.QRectF()
        
        penWidth = 10
        extra = (penWidth + self.arrowSize) / 2.0
        
        return QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)
    
    def paint(self, painter, option, widget):
        if not self.source() or not self.dest():
            return
        
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)
        
        if line.length() == 0.0:
            return
        
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 3, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)

        # Draw the arrows if there's enough room.
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = Edge.TwoPi - angle

        sourceArrowP1 = self.sourcePoint + QtCore.QPointF(math.sin(angle + Edge.Pi / 3) * self.arrowSize,
                                                          math.cos(angle + Edge.Pi / 3) * self.arrowSize)
        sourceArrowP2 = self.sourcePoint + QtCore.QPointF(math.sin(angle + Edge.Pi - Edge.Pi / 3) * self.arrowSize,
                                                          math.cos(angle + Edge.Pi - Edge.Pi / 3) * self.arrowSize);
        destArrowP1 = self.destPoint + QtCore.QPointF(math.sin(angle - Edge.Pi / 3) * self.arrowSize,
                                                      math.cos(angle - Edge.Pi / 3) * self.arrowSize)
        destArrowP2 = self.destPoint + QtCore.QPointF(math.sin(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize,
                                                      math.cos(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize)

        painter.setBrush(QtCore.Qt.black)
        #painter.drawPolygon(QtGui.QPolygonF([line.p1(), sourceArrowP1, sourceArrowP2]))
        #painter.drawPolygon(QtGui.QPolygonF([line.p2(), destArrowP1, destArrowP2]))

        
class NodeRect(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 1

    def __init__(self, graphWidget):
        QtGui.QGraphicsItem.__init__(self)
        self.graph = weakref.ref(graphWidget)
        self.edgeList = []
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)

    def addEdge(self, edge):
        self.edgeList.append(weakref.ref(edge))
        edge.adjust()

    def edges(self):
        return self.edgeList

    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(0 - adjust, 0 - adjust, 43 + adjust, 43 + adjust)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(0, 0, 40, 40)
        return path

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 3, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.setBrush(QtCore.Qt.white)
        painter.drawRect(0, 0, 40, 40)

        painter.setBrush(QtCore.Qt.black)

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            for edge in self.edgeList:
                edge().adjust()
            self.graph().itemMoved()
        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)
        

class GraphWidget(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        
        self.timerId = 0

        scene = QtGui.QGraphicsScene(self)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        scene.setSceneRect(-200, -200, 400, 400)
        #scene.setForegroundBrush(QtGui.QBrush(QtCore.Qt.lightGray, QtCore.Qt.CrossPattern))
        self.setScene(scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        
        node1 = NodeRect(self)
        node2 = NodeRect(self)
        
        scene.addItem(node1)
        scene.addItem(node2)
        edge = Edge(node1, node2)
        scene.addItem(edge)
        
        node1.setPos(0, 0)
        node2.setPos(100, 100)
        
        self.scale(0.8, 0.8)
        self.setMinimumSize(400, 400)
        self.setWindowTitle(self.tr("SMD"))
        
    def itemMoved(self):
        if not self.timerId:
            self.timerId = self.startTimer(1000/25)
            
    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.delta() / 240.0))
            
    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)

    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    widget = GraphWidget()
    widget.show()
    
    sys.exit(app.exec_())
    