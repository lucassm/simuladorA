#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
import math
import sys
from DialogReligador import DialogReligador
from time import sleep

class Edge(QtGui.QGraphicsLineItem):
    '''
        Classe que implementa o objeto Edge que liga dois objetos Node um ao outro
    '''
    def __init__(self, w1, w2, edgeMenu, parent=None, scene=None):
        '''
            Metodo inicial da classe Edge
            Recebe como parâmetros os objetos Node Inicial e Final
            Define o objeto QtCore.QLineF que define a linha que representa o objeto QtGui.QGraphicsLineItem
        '''
        super(Edge, self).__init__()
        
        self.w1 = w1
        self.w2 = w2
        self.w1.addEdge(self) # adiciona o objeto Edge a lista de Edges do objeto w1
        self.w2.addEdge(self) # adiciona o objeto Edge a lista de Edges do objeto w2
        
        self.myEdgeMenu = edgeMenu
        
        line = QtCore.QLineF(self.w1.pos(), self.w2.pos())
        self.setLine(line)
        self.setZValue(-1)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
    
    def updatePosition(self):
        '''
            Metodo de atualizacao da posicao do objeto edge implementado pela classe Edge
            Sempre que um dos objetos Nodes w1 ou w2 modifica sua posicao este metodo 
            e chamado para que o objeto edge possa acompanhar o movimento dos Objetos Node
        '''
        if not self.w1 or not self.w2:
            return
        
        line = QtCore.QLineF(self.w1.pos(), self.w2.pos())
        length = line.length()
        
        if length == 0.0:
            return
        
        self.prepareGeometryChange()
        self.setLine(line)
    
    def setColor(self, color):
        self.setPen(QtGui.QPen(color))
        
    def boundingRect(self):
        '''
            Metodo de definicao da borda do objeto edge implementado pela classe Edge
        '''
        extra = (self.pen().width() + 10) / 2.0
        p1 = self.line().p1()  # ponto inicial do objeto QtCore.QLineF associado ao objeto QtGui.QGraphicsLine
        p2 = self.line().p2()  # ponto final do objeto QtCore.QLineF associado ao objeto QtGui.QGraphicsLine
        
        return QtCore.QRectF(p1,                                    # topleft associada ao objeto QRectF 
                                    QtCore.QSizeF(p2.x() - p1.x(),  # comprimento no eixo x associado ao objeto QtCore.QSizeF
                                                  p2.y() - p1.y()   # comprimento no eixo y associado ao objeto QtCore.QSizeF
                                                  )                 # size associado ao objeto QRectF
                                 ).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        '''
            Metodo de desenho do objeto edge implementado pela classe Edge
        '''
        
        if (self.w1.collidesWithItem(self.w2)):
            return
        
        
        if self.w1.myItemType == Node.Barra and self.w2.myItemType != Node.Subestacao:
            if len(self.w1.edges) > 1:
                line = QtCore.QLineF(self.mapFromItem(self.w1, self.w1.rect().center().x(), self.w1.edgePosition(self)) , self.mapFromItem(self.w2, self.w2.rect().center()))
            else:
                line = QtCore.QLineF(self.mapFromItem(self.w1, self.w1.rect().center()) , self.mapFromItem(self.w2, self.w2.rect().center()))
        elif self.w2.myItemType == Node.Barra and self.w1.myItemType != Node.Subestacao:
            if len(self.w2.edges) > 1:
                line = QtCore.QLineF(self.mapFromItem(self.w1, self.w1.rect().center()) , self.mapFromItem(self.w2, self.w2.rect().center().x(), self.w2.edgePosition(self)))
            else:
                line = QtCore.QLineF(self.mapFromItem(self.w1, self.w1.rect().center()) , self.mapFromItem(self.w2, self.w2.rect().center()))
        else:
            line = QtCore.QLineF(self.mapFromItem(self.w1, self.w1.rect().center()) , self.mapFromItem(self.w2, self.w2.rect().center()))
                
        #line = QtCore.QLineF(self.mapFromItem(self.w1, self.w1.rect().center()) , self.mapFromItem(self.w2, self.w2.rect().center()))
        
        self.setLine(line)
        
        painter.setPen(QtGui.QPen(QtCore.Qt.black,  # QPen Brush
                               1,  # QPen width
                               QtCore.Qt.SolidLine,  # QPen style
                               QtCore.Qt.SquareCap,  # QPen cap style
                               QtCore.Qt.RoundJoin)  # QPen join style
                       )
        painter.setBrush(QtCore.Qt.black)
        painter.drawLine(self.line())
        
        if self.isSelected():
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.DashLine))
            myLine = QtCore.QLineF(line)
            myLine.translate(0, 4.0)
            painter.drawLine(myLine)
            myLine.translate(0,-8.0)
            painter.drawLine(myLine)
        
    def mousePressEvent(self, mouseEvent):
        self.setSelected(True)
        super(Edge, self).mousePressEvent(mouseEvent)
        return
        
    def contextMenuEvent(self, event):
        self.scene().clearSelection()
        self.setSelected(True)
        self.myEdgeMenu.exec_(event.screenPos())
            


class Text(QtGui.QGraphicsTextItem):
    '''
        Classe que implementa o objeto Text Generico
    '''
    
    def __init__(self, text, parent=None, scene=None):
        
        super(Text, self).__init__(text, parent, scene)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
    
    def mouseDoubleClickEvent(self, event):
        '''
            Metodo que trata o evento de duplo click no item grafico texto
            para edicao de seu conteudo
        '''
        if self.textInteractionFlags() == QtCore.Qt.NoTextInteraction:
            self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        super(Text, self).mouseDoubleClickEvent(event)

class Node(QtGui.QGraphicsRectItem):
    '''
       Classe que implementa o objeto Node Generico 
    '''
    
    # tipos de itens possiveis
    Subestacao, Religador, Barra, Agent = range(4)
    
    def __init__(self, itemType, nodeMenu, parent=None, scene=None):
    
        '''
            Metodo inicial da classe Node
            Recebe como parâmetros os objetos myItemType que define o tipo de Node desejado e x, y a posicao do objeto Node
            Define o objeto QtCore.QRectF que define o retangulo que representa o objeto QtGui.QGraphicsRectItem
        '''
        super(Node, self).__init__()
        
        self.edges = {}
        self.edges_no_sub = {}
        
        self.myItemType = itemType
        
        # caso o item a ser inserido seja do tipo subestacao
        if self.myItemType == self.Subestacao:
            rect = QtCore.QRectF(0, 0, 50.0, 50.0)
            # definine e ajusta a posicao do label do item grafico
            self.text = Text('Subestacao', self, self.scene())
            self.text.setPos(self.mapFromItem(self.text, 0, rect.height()))
        # caso o item a ser inserido seja do tipo religador
        elif self.myItemType == self.Religador:
            rect = QtCore.QRectF(0, 0, 50.0, 50.0)
            # definine e ajusta a posicao do label do item grafico
            self.text = Text('Religador', self, self.scene())
            self.text.setPos(self.mapFromItem(self.text, 0, rect.height()))
        # caso o item a ser inserido seja do tipo barra
        elif self.myItemType == self.Barra:
            rect = QtCore.QRectF(0, 0, 10.0, 100.0)
            # definine e ajusta a posicao do label do item grafico
            self.text = Text('Barra', self, self.scene())
            self.text.setPos(self.mapFromItem(self.text, 0, rect.height()))
        # caso o item a ser inserido seja do tipo agent
        elif self.myItemType == self.Agent:
            rect = QtCore.QRectF(0, 0, 50.0, 50.0)
            # definine e ajusta a posicao do label do item grafico
            self.text = Text('Agente', self, self.scene())
            self.text.setPos(self.mapFromItem(self.text, 0, rect.height()))
        
        self.setRect(rect)
        self.myNodeMenu = nodeMenu
        
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, True)
        self.setZValue(0)
    
    def removeEdges(self):
        '''
            Metodo de remocao de todos objetos edge associados ao objeto node
        '''
        for edge in self.edges:
            self.scene().removeItem(edge)
        
        self.edges.clear()
        self.edges_no_sub.clear()
 
    def addEdge(self, edge):
        '''
            Metodo de adicao de objetos edge associados ao objeto node
        '''
        self.edges[edge] = len(self.edges)
        
        if edge.w1.myItemType != Node.Subestacao and edge.w2.myItemType != Node.Subestacao:
            self.edges_no_sub[edge] = len(self.edges_no_sub)
    
    def edgePosition(self, edge):
        
        height = self.rect().height()
        print 'bus width', height
        height = height - 2.0 * height/8.0
        
        numEdges = len(self.edges_no_sub)
                
        numEdges -= 1
        
        dw = height/float(numEdges)
        
        pos = height/8.0 + self.edges_no_sub[edge]*dw
        
        print 'espaco entre bus', dw
        print 'id da edge: ', self.edges_no_sub[edge]
        print 'pos da linha', pos
        return pos
            
    
    def boundingRect(self):
        '''
            Metodo que especifica a borda do objeto node
        '''
        extra = 5.0
        return self.rect().adjusted(-extra, -extra, extra, extra)
    
    def paint(self, painter, option, widget):
        '''
            Metodo de desenho do objeto node implementado pela classe Node
        '''
        
        self.text.setPos(0, self.rect().height())
        
        # caso o item a ser inserido seja do tipo subestacao
        if self.myItemType == self.Subestacao:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 1.5))
            painter.setBrush(QtCore.Qt.white)
            painter.drawEllipse(self.rect())
        # caso o item a ser inserido seja do tipo religador
        elif self.myItemType == self.Religador:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 1.5))
            painter.setBrush(QtCore.Qt.white)
            painter.drawRect(self.rect())
        # caso o item a ser inserido seja do tipo barra
        elif self.myItemType == self.Barra:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 1.5))
            painter.setBrush(QtCore.Qt.black)
            painter.drawRect(self.rect())
        # caso o item a ser inserido seja do tipo agent
        elif self.myItemType == self.Agent:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 1.5))
            painter.setBrush(QtCore.Qt.white)
            painter.drawRect(self.rect())
        
        if self.isSelected():                
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.DashLine))
            painter.setBrush(QtCore.Qt.NoBrush)
            adjust = 2
            rect = self.rect().adjusted(-adjust, -adjust, adjust, adjust)
            painter.drawRect(rect)   
                    
    def itemChange(self, change, value):
        '''
            Metodo que detecta mudancas na posicao do objeto node
        '''
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            for edge in self.edges:
                edge.updatePosition()
        return QtGui.QGraphicsItem.itemChange(self, change, value)
    
    def mousePressEvent(self, mouseEvent):
        
        self.setSelected(True)        
        super(Node, self).mousePressEvent(mouseEvent)
        return
    
    def contextMenuEvent(self, event):
            self.scene().clearSelection()
            self.setSelected(True)
            self.myNodeMenu.exec_(event.screenPos())
        
class SceneWidget(QtGui.QGraphicsScene):
    '''
        Classe que implementa o container Grafico onde os
        widgets residirao
    '''
    
    # tipos de modos de iteracao com o diagrama grafico
    InsertItem, InsertLine, InsertText, MoveItem, SelectItems  = range(5)
    
    # tipos de estilos para o background do diagrama grafico
    GridStyle, NoStyle = range(2) 
    # signal definido para a classe SceneWidget enviado quando um item é inserido no diagrama grafico
    itemInserted = QtCore.Signal(int)
    
    def __init__(self):
        
        super(SceneWidget, self).__init__()
        
        self.setSceneRect(0, 0, 800, 800)
        
        self.myMode = self.MoveItem
        self.myItemType = Node.Subestacao
        
        self.myBackgroundSytle = self.NoStyle
        
        self.keyControlIsPressed = False
        
        self.line = None
        self.selectRect = None
        self.textItem = None
        
        self.createActions()
        self.createMenus()

    def mousePressEvent(self, mouseEvent):
        '''
            Este metodo define as acoes realizadas quando um evento do tipo
            mousePress e detectado no diagrama grafico
        '''
        
        if (mouseEvent.button() != QtCore.Qt.LeftButton):
            return

        if self.myMode == self.InsertItem:
            
            if self.myItemType == Node.Religador:
                item = Node(self.myItemType, self.myRecloserMenu)
            elif self.myItemType == Node.Barra:
                item = Node(self.myItemType, self.myBusMenu)
            elif self.myItemType == Node.Subestacao:
                item = Node(self.myItemType, self.mySubstationMenu)
            
            self.addItem(item)
            item.setPos(mouseEvent.scenePos())
            self.itemInserted.emit(self.myItemType)
            
        elif self.myMode == self.InsertLine:
            
            self.line = QtGui.QGraphicsLineItem(
                                                QtCore.QLineF(
                                                              mouseEvent.scenePos(),
                                                              mouseEvent.scenePos()
                                                              )
                                                )
            self.line.setPen(
                             QtGui.QPen(QtCore.Qt.black, 2)
                             )
            self.addItem(self.line)
            
        elif self.myMode == self.InsertText:
            textItem = Text()
            textItem.setFont(self.myFont)
            textItem.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
            textItem.setZValue(1000.0)
            textItem.lostFocus.connect(self.editorLostFocus)
            textItem.selectedChange.connect(self.itemSelected)
            self.addItem(textItem)
            textItem.setDefaultTextColor(self.myTextColor)
            textItem.setPos(mouseEvent.scenePos())
            self.textInserted.emit(textItem)
        elif self.myMode == self.SelectItems:
            selection = True
            for item in self.items():
                if item.isUnderMouse():
                    selection = False
            if selection:
                initPoint = mouseEvent.scenePos()
                self.selectRect = QtGui.QGraphicsRectItem(QtCore.QRectF(initPoint, initPoint))
                self.selectRect.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.DashLine))
                self.addItem(self.selectRect)
        super(SceneWidget, self).mousePressEvent(mouseEvent)

        return
    
    def mouseMoveEvent(self, mouseEvent):
        '''
            Este medodo define as acoes realizadas quando um evento do tipo mouseMove
            e detectado no diagrama grafico. Neste caso desenha uma linha quando o modo
            self.InsertLine está ativado
        '''
        if self.myMode == self.InsertLine and self.line:
            newLine = QtCore.QLineF(self.line.line().p1(), mouseEvent.scenePos())
            self.line.setLine(newLine)
        elif self.myMode == self.MoveItem:
            super(SceneWidget, self).mouseMoveEvent(mouseEvent)
        elif self.myMode == self.SelectItems and self.selectRect:
            newRect = QtCore.QRectF(self.selectRect.rect().topLeft(), mouseEvent.scenePos())
            self.selectRect.setRect(newRect)
    
    def mouseReleaseEvent(self, mouseEvent):
        '''
            Este medodo define as acoes realizadas quando um evento do tipo mouseRealese
            e detectado no diagrama grafico. Neste caso conecta os dois elementos que estão ligado
            pela linha criada no evento mousePress
        '''
        if self.myMode == self.InsertLine and self.line:
            startItems = self.items(self.line.line().p1())
            if len(startItems) and startItems[0] == self.line:
                startItems.pop(0)
            endItems = self.items(self.line.line().p2())
            if len(endItems) and endItems[0] == self.line:
                endItems.pop(0)

            self.removeItem(self.line)
            self.line = None

            if len(startItems) and len(endItems) and \
                    isinstance(startItems[0], Node) and \
                    isinstance(endItems[0], Node) and \
                    startItems[0] != endItems[0]:
                startItem = startItems[0]
                endItem = endItems[0]
                edge = Edge(startItem, endItem, self.myLineMenu)
                edge.setColor(QtCore.Qt.black)
                self.addItem(edge)
                edge.updatePosition()
        elif self.myMode == self.SelectItems and self.selectRect:
            path = QtGui.QPainterPath()
            path.addRect(self.selectRect.rect())
            self.setSelectionArea(path)
            self.removeItem(self.selectRect)
            self.selectRect = None
                                                                                                          
        self.line = None
        self.itemInserted.emit(3)
        super(SceneWidget, self).mouseReleaseEvent(mouseEvent)
    
    def keyPressEvent(self, event):
        key = event.key()
        
        if key == QtCore.Qt.Key_Up:
            for item in self.selectedItems():
                item.moveBy(0, -5)
        elif key == QtCore.Qt.Key_Down:
            for item in self.selectedItems():
                item.moveBy(0, 5)
        elif key == QtCore.Qt.Key_Left:
            for item in self.selectedItems():
                item.moveBy(-5, 0)
        elif key == QtCore.Qt.Key_Right:
            for item in self.selectedItems():
                item.moveBy(5, 0)
        elif key == QtCore.Qt.Key_Space or key == QtCore.Qt.Key_Enter:
            pass
        elif key == QtCore.Qt.Key_Control:
            self.keyControlIsPressed = True
            print 'Ctrl pressed'
        elif key == QtCore.Qt.Key_Delete:
            self.deleteItem()
        else:
            pass
            #super(SceneWidget, self).keyPressEvent(self, event)
        return
    
    def setItemType(self, type):
        '''
            Define em qual tipo de item sera inserido no diagrama grafico assim que um evento
            do tipo mousePress for detectado, podendo ser:
            Node.Subestacao
            Node.Religador
            Node.Barra
            Node.Agent
        '''
        self.myItemType = type
    
    def setMode(self, mode):
        '''
            Define em qual modo 
        '''
        self.myMode = mode
    
    def createActions(self):
        '''
            Este metodo cria as ações que serão utilizadas nos menus dos itens graficos
        '''
        self.propertysAction = QtGui.QAction('Propriedades', self, shortcut = 'Enter', triggered = self.launchDialog)
        self.deleteAction = QtGui.QAction('Excluir Item', self, shortcut = 'Delete', triggered = self.deleteItem)
        self.increaseBusAction = QtGui.QAction('Aumentar Barra', self, shortcut = 'Ctrl + a',triggered = self.increaseBus)
        self.decreaseBusAction = QtGui.QAction('Diminuir Barra', self, shortcut = 'Ctrl + d', triggered = self.decreaseBus)
        self.alignHLineAction = QtGui.QAction('Alinha Linha H', self, shortcut = 'Ctrl + h',triggered = self.alignLineH)
        self.alignVLineAction = QtGui.QAction('Alinhar Linha V', self, shortcut = 'Ctrl + v', triggered = self)
    
    def createMenus(self):
        '''
            Este metodo cria os menus de cada um dos itens graficos: religador, subestacao, barra e linha
        '''
        self.myBusMenu = QtGui.QMenu('Menu Bus')
        self.myBusMenu.addAction(self.increaseBusAction)
        self.myBusMenu.addAction(self.decreaseBusAction)
        self.myBusMenu.addAction(self.deleteAction)
        self.myBusMenu.addAction(self.propertysAction)
        
        self.myRecloserMenu = QtGui.QMenu('Menu Recloser')
        self.myRecloserMenu.addAction(self.propertysAction)
        self.myRecloserMenu.addAction(self.deleteAction)
        
        self.mySubstationMenu = QtGui.QMenu('Menu Subestacao')
        self.mySubstationMenu.addAction(self.propertysAction)
        self.mySubstationMenu.addAction(self.deleteAction)
        
        self.myLineMenu = QtGui.QMenu('Menu Linha')
        self.myLineMenu.addAction(self.alignHLineAction)
        self.myLineMenu.addAction(self.alignVLineAction)
        self.myLineMenu.addAction(self.propertysAction)
        self.myLineMenu.addAction(self.deleteAction)
    
    def deleteItem(self):
        '''
            Este metodo implementa a acao de exclusão de um item grafico do diagrama
        '''
        for item in self.selectedItems():
            if isinstance(item, Node):
                item.removeEdges()
            self.removeItem(item)
    
    def launchDialog(self):
        '''
            Este metodo inicia os dialogos de configuracao de cada um dos itens graficos do diagrama
        '''
        dialog = DialogReligador()
    
    def increaseBus(self, ):
        '''
            Este metodo implementa a acao de aumentar o tamanho do item grafico barra
        '''
        for item in self.selectedItems():
            if isinstance(item, Node):
                item.prepareGeometryChange()
                item.setRect(item.rect().x(), item.rect().y(), item.rect().width(), item.rect().height()*1.25)
    
    def decreaseBus(self):
        '''
            Este metodo implementa a acao de aumentar o tamanho do item grafico barra
        '''
        for item in self.selectedItems():
            if isinstance(item, Node):
                item.prepareGeometryChange()
                item.setRect(item.rect().x(), item.rect().y(), item.rect().width(), item.rect().height()*0.75)
    
    def alignLineH(self):
        for item in self.selectedItems():
            if isinstance(item, Edge):
                posY = item.w1.y()
                item.w2.setY(posY)
    
    def hAlign(self):
        yPosList = []
        for item in self.selectedItems():
            print 'pos', item.pos()
            print 'scene pos', item.pos()
            if isinstance(item, Node):
                yPosList.append(item.pos().y())
        maxPos = max(yPosList)
        minPos = min(yPosList)
        meanPos = maxPos - abs(maxPos - minPos)/2.0
        
        for item in self.selectedItems():
            if isinstance(item, Node):
                item.setY(meanPos)
                
    def vAlign(self):
        xPosList = []
        for item in self.selectedItems():
            if isinstance(item, Node):
                xPosList.append(item.pos().x())
        maxPos = max(xPosList)
        minPos = min(xPosList)
        meanPos = maxPos - abs(maxPos - minPos)/2.0
        
        for item in self.selectedItems():
            if isinstance(item, Node):
                item.setX(meanPos)
    
    def setGrid(self):
        if self.myBackgroundSytle == self.GridStyle:
            self.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.white, QtCore.Qt.NoBrush))
            self.myBackgroundSytle = self.NoStyle
        elif self.myBackgroundSytle == self.NoStyle:
            self.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.lightGray, QtCore.Qt.CrossPattern))
            self.myBackgroundSytle = self.GridStyle
class ViewWidget(QtGui.QGraphicsView):
    '''
        Esta classe implementa o container QGraphicsView
        onde residira o objeto QGraphicsScene
    '''
    def __init__(self, scene):
        
        super(ViewWidget, self).__init__(scene)
        
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.delta() / 240.0))
    
    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.5 or factor > 3:
            return

        self.scale(scaleFactor, scaleFactor)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    scene = SceneWidget()
    widget = ViewWidget(scene)
    widget.show()
    sys.exit(app.exec_())
