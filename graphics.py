#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
import math
import sys
from rede import Chave
# import models

from DialogReligador import RecloserDialog


class GhostR(QtGui.QGraphicsRectItem):
    def __init__(self, x, y, w, h, edge, event):
        QtGui.QGraphicsRectItem.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.no = None
        self.edge = edge
        self.event = event
        self.setRect(x, y, w, h)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)

    def contextMenuEvent(self, event):
        self.scene().clearSelection()
        self.setSelected(True)
        self.edge.setSelected(True)
        self.edge.myEdgeMenu.exec_(event.screenPos())

        super(GhostR, self).contextMenuEvent(event)

    def mousePressEvent(self, mouse_event):
        if (mouse_event.button() == QtCore.Qt.LeftButton):
            # self.scene().removeItem(self)
            for item in self.scene().items(mouse_event.scenePos()):
                item.grabMouse()
            super(GhostR, self).mousePressEvent(mouse_event)
            return
        # self.setSelected(True)

        super(GhostR, self).mousePressEvent(mouse_event)
        return

    def mouseReleaseEvent(self, mouse_event):
        for item in self.scene().items():
            if isinstance(item, Node):
                item.ungrabMouse()
                item.setSelected(False)
        super(GhostR, self).mouseReleaseEvent(mouse_event)
    def paint(self, painter, option, widget):

        painter.setPen(QtGui.QPen(QtCore.Qt.black,      # QPen Brush
                                  1,                    # QPen width
                                  QtCore.Qt.SolidLine,  # QPen style
                                  QtCore.Qt.SquareCap,  # QPen cap style
                                  QtCore.Qt.RoundJoin)  # QPen join style
                       )
        # painter.setBrush(QtCore.Qt.black)
        painter.drawRect(self.edge.GhostRet)


class Edge(QtGui.QGraphicsLineItem):
    '''
        Classe que implementa o objeto Edge que liga dois objetos Node um ao
        outro
    '''
    def __init__(self, w1, w2, edge_menu, parent=None, scene=None):
        '''
            Metodo inicial da classe Edge
            Recebe como parâmetros os objetos Node Inicial e Final
            Define o objeto QtCore.QLineF que define a linha que
            representa o objeto QtGui.QGraphicsLineItem
        '''
        super(Edge, self).__init__()
        self.w1 = w1
        self.w2 = w2
        self.w1.add_edge(self)  # adiciona o objeto Edge a lista de Edges do
# objeto w1
        self.w2.add_edge(self)  # adiciona o objeto Edge a lista de Edges do
# objeto w2

        self.myEdgeMenu = edge_menu

        line = QtCore.QLineF(self.w1.pos(), self.w2.pos())
        self.setLine(line)
        self.setZValue(-1)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

        self.GhostRet = QtCore.QRectF()
        self.GhostRetItem = GhostR(0, 0, 0, 0, self, self.myEdgeMenu)
        self.isFixed = False
        self.fixFlag = False

    def update_ret(self):
        delta_yo = self.line().p2().y() - self.line().p1().y()
        delta_xo = self.line().p2().x() - self.line().p1().x()
        delta_y = math.fabs(self.line().p2().y() - self.line().p1().y())
        delta_x = math.fabs(self.line().p2().x() - self.line().p1().x())
        if self.line().p2().y() < self.line().p1().y():
            ybase = self.line().p2().y()
            # ytop  = self.line().p1().y()
        else:
            ybase = self.line().p1().y()
            # ytop  = self.line().p2().y()
        if self.line().p2().x() < self.line().p1().x():
            xbase = self.line().p2().x()
            # xtop  = self.line().p1().y()
        else:
            xbase = self.line().p1().x()
            # xtop  = self.line().p2().y()

        # newDeltaY = ytop - ybase
        # newDeltaX = xtop - xbase
        angle = math.degrees(math.atan2(delta_y, delta_x))
        compfix = self.line().length()
        comp = delta_x - 40
        # larg = (delta_y / 2) - 5
        if (delta_x - 40) < (0.7 * compfix):
            if delta_y < 0.5 * compfix:
                xbase = xbase - 5
                pass
            else:
                comp = delta_y - 20
                xbase = xbase - delta_y / 1000
            # print "0,7"
        if (delta_x - 40) < (0.6 * compfix):
            if delta_y < 0.5 * compfix:
                xbase = xbase - 5
                pass
            else:
                comp = delta_y - 20
                xbase = xbase - 100 * delta_y / 1000
            # print "0,6"
        if (delta_x - 40) < (0.5 * compfix):
            if delta_y < 0.5 * compfix:
                xbase = xbase - 5
                comp = comp + 2
                pass
            else:
                comp = delta_y - 20
                xbase = xbase - 100 * delta_y / 1000
            # print "0,5"
        if (delta_x - 40) < (0.4 * compfix):
            if delta_y < 0.5 * compfix:
                xbase = xbase - 5
                comp = comp + 2
                pass
            else:
                comp = delta_y - 20
                xbase = xbase - 50 * delta_y / 1000
            # print "0,4"

        if (delta_x - 40) < (0.3 * compfix):
            if delta_y < 0.5 * compfix:
                xbase = xbase - 5
                comp = comp + 2
                pass
            else:
                comp = delta_y - 20
                xbase = xbase - 100 * delta_y / 1000
            # print "0,25"
        if (delta_x - 40) < (0.15 * compfix):
            if delta_y < 0.5 * compfix:
                xbase = xbase - 5
                comp = comp + 2
                pass
            else:
                comp = delta_y - 20
                xbase = xbase - 70 * delta_y / 1000
            # print "0,1"

        if (delta_x - 40) < (0.05 * compfix):
            if delta_y < 0.5 * compfix:
                xbase = xbase - 5
                comp = comp + 2
                pass
            else:
                comp = delta_y - 20
                xbase = xbase - 70 * delta_y / 1000

            
        self.GhostRet.setRect(xbase + 40, ybase + (delta_y / 2) - 5, comp, 50)
        if self.w1.myItemType == 4 or self.w2.myItemType == 4:
            self.GhostRet.setRect(xbase + 40, ybase + (delta_y / 2) - 5, comp, 50)
        if self.isFixed:
            self.GhostRet.adjust(-20, -20, -20, -20)
        x = self.GhostRet.center().x()
        y = self.GhostRet.center().y()
        self.GhostRetItem.setRect(self.GhostRet)
        self.GhostRetItem.setTransform(
            QtGui.QTransform().translate(x, y).rotate(angle).translate(-x, -y))
        if (delta_xo < 0 and delta_yo > 0) or (delta_xo > 0 and delta_yo < 0):
            self.GhostRetItem.setTransform(
                QtGui.QTransform().translate(x, y).rotate(-angle).translate(
                    -x, -y))
        # if self.GhostRetItem.collidesWithItem(self.w1):
        #     if self.w1.myItemType == 4:
        #         print "bateu no nó"
        #         self.GhostRetItem.setRect(self.GhostRetItem.rect().adjusted(-10,-10,-10,-10))

        # if self.GhostRetItem.collidesWithItem(self.w2):
        #     if self.w2.myItemType == 4:
        #         print "bateu no nó"
        #         self.GhostRetItem.setRect(self.GhostRetItem.rect().adjusted(-10,-10,-10,-10))


    def update_position(self):
        '''
            Metodo de atualizacao da posicao do objeto edge implementado pela
            classe Edge. Sempre que um dos objetos Nodes w1 ou w2 modifica sua
            posicao este método é chamado para que o objeto edge possa
            acompanhar o movimento dos Objetos Node.
        '''
        if not self.w1 or not self.w2:
            return

        line = QtCore.QLineF(self.w1.pos(), self.w2.pos())
        length = line.length()

        if length == 0.0:
            return

        self.prepareGeometryChange()
        self.setLine(line)
        self.update_ret()

    def set_color(self, color):
        self.setPen(QtGui.QPen(color))

    # def drawRec(self):
    #   self.ret = QtCore.QRectF(0,0,self.line().p2.x() - self.line().p1.x())
    #   self.ret.setCoords()

    def boundingRect(self):
        '''
            Metodo de definicao da borda do objeto edge implementado pela
            classe Edge.
        '''
        extra = (self.pen().width() + 100)
        p1 = self.line().p1()  # ponto inicial do objeto QtCore.QLineF
        # associado ao objeto QtGui.QGraphicsLine
        p2 = self.line().p2()  # ponto final do objeto QtCore.QLineF associado
        # ao objeto QtGui.QGraphicsLine

        rec = QtCore.QRectF(p1,
                            QtCore.QSizeF(p2.x() - p1.x(),
                                          p2.y() - p1.y())).normalized()
        rec.adjust(-extra, -extra, extra, extra)
        return rec

    def paint(self, painter, option, widget):
        '''
            Metodo de desenho do objeto edge implementado pela classe Edge
        '''
        if (self.w1.collidesWithItem(self.w2)):
            return

        # if self.w1.myItemType == Node.NoConectivo or self.w2.myItemType == Node.NoConectivo:
        #     return

        # Esta é a logica de distribuicao e alinhamento das linhas conectadas
        # ao item grafico Barra

        # Se o item self.w1 for do tipo barra deve-se alinhar o item self.w2
        if self.w1.myItemType == Node.Barra and self.w2.myItemType != Node.Subestacao:
            self.fixFlag = True
            # se o numero de linhas conectas a barra for maior que 1 deve-se
            # proceder a logica de distribuicao e alinhamento
            if len(self.w1.edges) > 1:
                # insere a linha em seu local de distribuicao calculado pelo
                # item grafico barra
                line = QtCore.QLineF(self.mapFromItem(
                    self.w1, self.w1.rect().center().x(),
                    self.w1.edge_position(
                        self)), self.mapFromItem(
                    self.w2, self.w2.rect().center()))
                # alinha o item religador conectado ao item Barra com alinha
                # que conecta esses dois items
                self.w2.setY(self.mapFromItem(
                    self.w1, self.w1.rect().center().x(),
                    self.w1.edge_position(
                        self)).y() - 20.0)
                if self.w2.myItemType == Node.NoConectivo:
                    self.w2.setY(self.mapFromItem(
                    self.w1, self.w1.rect().center().x(),
                    self.w1.edge_position(
                        self)).y() -5)
                self.w2.fix_item()
            # se não os items são apenas conectados
            else:
                line = QtCore.QLineF(self.mapFromItem(
                    self.w1, self.w1.rect().center()), self.mapFromItem(
                    self.w2, self.w2.rect().center()))

        # Se o item self.w2 for do tipo barra deve-se alinhar o item self.w1
        elif self.w2.myItemType == Node.Barra and self.w1.myItemType != Node.Subestacao:
            self.fixFlag = True
            # se o numero de linhas conectas a barra for maior que 1 deve-se
            # proceder a logica de distribuicao e alinhamento
            if len(self.w2.edges) > 1:
                # insere a linha em seu local de distribuicao calculado pelo
                # item grafico barra
                line = QtCore.QLineF(self.mapFromItem(
                    self.w1, self.w1.rect().center()), self.mapFromItem(
                    self.w2, self.w2.rect().center().x(),
                    self.w2.edge_position(
                        self)))
                # alinha o item religador conectado ao item Barra com alinha
                # que conecta esses dois items
                self.w1.setY(self.mapFromItem(
                    self.w2, self.w2.rect().center().x(),
                    self.w2.edge_position(
                        self)).y() - 20.0)
                self.w1.fix_item()
            # se não os items são apenas conectados
            else:
                line = QtCore.QLineF(self.mapFromItem(
                    self.w1, self.w1.rect().center()), self.mapFromItem(
                    self.w2, self.w2.rect().center()))
        # se nenhum dos items for do tipo Barra então os items são apenas
        # conectados
        else:
            line = QtCore.QLineF(self.mapFromItem(
                self.w1, self.w1.rect().center()), self.mapFromItem(
                self.w2, self.w2.rect().center()))

        # line = QtCore.QLineF(self.mapFromItem(
            # self.w1, self.w1.rect().center()) , self.mapFromItem(
            # self.w2, self.w2.rect().center()))

        self.setLine(line)
        if self.fixFlag:
            self.isFixed = True
            self.update_ret()

        painter.setPen(QtGui.QPen(QtCore.Qt.black,  # QPen Brush
                                                    1,  # QPen width
                                                    QtCore.Qt.SolidLine,
                                                    # QPen style
                                                    QtCore.Qt.SquareCap,
                                                    # QPen cap style
                                                    QtCore.Qt.RoundJoin)
                       # QPen join style
                       )
        painter.setBrush(QtCore.Qt.black)
        painter.drawLine(self.line())

        if self.isSelected():
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.DashLine))
            my_line = QtCore.QLineF(line)
            my_line.translate(0, 4.0)
            painter.drawLine(my_line)
            my_line.translate(0, -8.0)
            painter.drawLine(my_line)

    def mousePressEvent(self, mouse_event):
        self.setSelected(True)
        super(Edge, self).mousePressEvent(mouse_event)
        return

    def contextMenuEvent(self, event):
        self.scene().clearSelection()
        self.setSelected(True)
        self.myEdgeMenu.exec_(event.screenPos())


class Text(QtGui.QGraphicsTextItem):
    '''
        Classe que implementa o objeto Text Generico
    '''

    selectedChange = QtCore.Signal(QtGui.QGraphicsItem)
    lostFocus = QtCore.Signal(QtGui.QGraphicsTextItem)

    def __init__(self, text, parent=None, scene=None):

        super(Text, self).__init__(parent, scene)
        self.setPlainText(text)
        self.setZValue(100)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextEditorInteraction)
        # self.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        # self.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard)

    def mouseDoubleClickEvent(self, event):
        '''
            Metodo que trata o evento de duplo click no item grafico texto
            para edicao de seu conteudo
        '''
        if self.textInteractionFlags() == QtCore.Qt.NoTextInteraction:
            self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        super(Text, self).mouseDoubleClickEvent(event)

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemSelectedChange:
            self.selectedChange.emit(self)
        return value

    def focusOutEvent(self, event):
        # self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.lostFocus.emit(self)
        super(Text, self).focusOutEvent(event)


class Node(QtGui.QGraphicsRectItem):
    '''
       Classe que implementa o objeto Node Genérico.
    '''
    # tipos de itens possiveis
    Subestacao, Religador, Barra, Agent, NoConectivo = range(5)

    def __init__(self, item_type, node_menu, parent=None, scene=None):
        '''
            Método inicial da classe Node
            Recebe como parâmetros os objetos myItemType que define o tipo de
            Node desejado e x, y a posicao do objeto Node. Define o objeto
            QtCore.QRectF que define o retangulo que representa o objeto
            QtGui.QGraphicsRectItem.
        '''
        super(Node, self).__init__()
        self.id = id(self)
        self.edges = {}
        self.l0 = None
        self.edges_no_sub = {}
        self.myItemType = item_type
        self.Fixed = False
        self.edge_counter = 0
        # caso o item a ser inserido seja do tipo subestacao
        if self.myItemType == self.Subestacao:
            rect = QtCore.QRectF(0, 0, 50.0, 50.0)
            # definine e ajusta a posicao do label do item grafico
            self.text = Text('Subestacao', self, self.scene())
            self.text.setPos(self.mapFromItem(self.text, 0, rect.height()))
        # caso o item a ser inserido seja do tipo religador
        elif self.myItemType == self.Religador:
            rect = QtCore.QRectF(0, 0, 40.0, 40.0)
            # Cria o objeto abstrato chave referente ao religador
            self.chave = Chave('religador1', 400, 0.01, 1000, 3)
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
        # caso o item a ser inserido seja do tipo nó conectivo
        elif self.myItemType == self.NoConectivo:
            rect = QtCore.QRectF(0, 0, 7, 7)

        self.setRect(rect)
        self.myNodeMenu = node_menu

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setZValue(0)

    def fix_item(self):
        self.Fixed = True

    def update_count(self):
        self.edge_counter = len(self.edges)
    def remove_edges(self):
        '''
            Metodo de remocao de todos objetos edge associados ao objeto node
        '''
        deleted_list = []
        for edge in self.edges:
            deleted_list.append(edge)
            self.scene().removeItem(edge.GhostRetItem)
            self.scene().removeItem(edge)

        for edge in deleted_list:
            edge.w1.remove_edge(edge)
            edge.w2.remove_edge(edge)

        self.edges.clear()
        self.edges_no_sub.clear()
        self.update_count()

    def remove_edge(self, edge):
        self.edges.pop(edge)
        self.update_count()

    def add_edge(self, edge):
        '''
            Metodo de adicao de objetos edge associados ao objeto node
        '''
        if self.myItemType == self.Religador:
            if self.edge_counter > 2:
                return
            self.edge_counter += 1
        self.edges[edge] = len(self.edges)

        if edge.w1.myItemType != Node.Subestacao and edge.w2.myItemType != Node.Subestacao:
            self.edges_no_sub[edge] = len(self.edges_no_sub)
        self.update_count()
    def edge_position(self, edge):

        height = self.rect().height()
        height = height - 2.0 * height / 8.0

        num_edges = len(self.edges_no_sub)

        num_edges -= 1

        dw = height / float(num_edges)

        pos = height / 8.0 + self.edges_no_sub[edge] * dw

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

        # self.text.setPos(0, self.rect().height())
        # caso o item a ser inserido seja do tipo subestacao
        if self.myItemType == self.Subestacao:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 1.5))
            painter.setBrush(QtCore.Qt.white)
            painter.drawEllipse(self.rect())
        # caso o item a ser inserido seja do tipo religador1
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
        # caso o item a ser inserido seja do tipo nó conectivo
        elif self.myItemType == self.NoConectivo:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 1.5))
            painter.setBrush(QtCore.Qt.black)
            painter.drawEllipse(self.rect())

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
                edge.update_position()
        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def mousePressEvent(self, mouse_event):
        print len(self.edges)
        self.setSelected(True)
        super(Node, self).mousePressEvent(mouse_event)
        return

    def mouseMoveEvent(self, mouse_event):
        super(Node, self).mouseMoveEvent(mouse_event)
        return

    def mouseReleaseEvent(self, mouse_event):
        new_edge = None
        scene = self.scene()
        for edge in self.edges:
            if edge.w1 == self:
                new_obj = edge.w2
            if edge.w2 == self:
                new_obj = edge.w1
        if self.myItemType == 4:
            for item in self.scene().items():
                if isinstance(item, Node):

                    if self.collidesWithItem(item):
                        if item.myItemType == 1:
                            self.remove_edges()
                            self.moveBy(50,50)
                            self.hide()
                            new_edge = Edge(new_obj, item, scene.myLineMenu)
                            scene.addItem(new_edge)
                            scene.addItem(new_edge.GhostRetItem)
                            new_edge.update_position()
                        # if edge.w2 == self:
                        #     edge.w2 = item
                        #     edge.update_position()
                        #     self.scene().removeItem(self)
        super(Node, self).mouseReleaseEvent(mouse_event)
        return


    def contextMenuEvent(self, event):
            self.scene().clearSelection()
            self.setSelected(True)
            self.myNodeMenu.exec_(event.screenPos())


class SceneWidget(QtGui.QGraphicsScene):
    '''
        Classe que implementa o container Grafico onde os
        widgets residirão
    '''

    # tipos de modos de iteracao com o diagrama grafico
    InsertItem, InsertLine, InsertText, MoveItem, SelectItems = range(5)

    # tipos de estilos para o background do diagrama grafico
    GridStyle, NoStyle = range(2)
    # signal definido para a classe SceneWidget enviado quando um item é
    # inserido no diagrama grafico
    itemInserted = QtCore.Signal(int)

    def __init__(self):

        super(SceneWidget, self).__init__()
        self.setSceneRect(0, 0, 800, 800)
        self.myMode = self.MoveItem
        self.myItemType = Node.Subestacao
        self.myBackgroundSytle = self.NoStyle
        self.keyControlIsPressed = False
        self.line = None
        self.no = None
        self.ghost = None
        self.selectRect = None
        self.start_item_is_ghost = False
        self.end_item_is_ghost = False
        self.text_item = None
        self.create_actions()
        self.create_menus()

    def mousePressEvent(self, mouse_event):
        '''
            Este metodo define as acoes realizadas quando um evento do tipo
            mousePress e detectado no diagrama grafico
        '''
        self.pressPos = mouse_event.scenePos()
        if (mouse_event.button() != QtCore.Qt.LeftButton):
            return
        item_oculto = None
        for item in self.items():
            if not item.isVisible():
                item_oculto = item
        if item_oculto == None:
            pass
        else:
            self.removeItem(item_oculto)
        if self.myMode == self.InsertItem:

            if self.myItemType == Node.Religador:
                item = Node(self.myItemType, self.myRecloserMenu)
            elif self.myItemType == Node.Barra:
                item = Node(self.myItemType, self.myBusMenu)
            elif self.myItemType == Node.Subestacao:
                item = Node(self.myItemType, self.mySubstationMenu)

            self.addItem(item)
            item.setPos(mouse_event.scenePos())
            self.itemInserted.emit(self.myItemType)

        elif self.myMode == self.InsertLine:
            passe = False
            add = True
            for item in self.items():
                if item.isUnderMouse():
                    if isinstance(item, GhostR):

                        c_pos = (
                            item.edge.line().p1() + item.edge.line().p2()) / 2
                        self.no = Node(4, self.myLineMenu)
                        self.addItem(self.no)
                        self.no.setPos(c_pos - QtCore.QPointF(3.5, 3.5))
                        item.no = self.no
                        self.ghost = item
                        # self.start_item_is_ghost = True
                        passe = True
                    elif isinstance(item,Node) or isinstance(item, Edge):
                        add = False
            if passe is True:
                self.l0 = c_pos
            else:
                self.l0 = mouse_event.scenePos()
                self.no = Node(4, self.myLineMenu)
                if add is True:
                    self.addItem(self.no)
                self.no.setPos(mouse_event.scenePos())
                self.no_origem = self.no
            self.line = QtGui.QGraphicsLineItem(
                QtCore.QLineF(
                    self.l0,
                    self.l0))
            self.line.setPen(
                QtGui.QPen(QtCore.Qt.black, 2))
            self.addItem(self.line)

        elif self.myMode == self.InsertText:
            text_item = Text()
            text_item.setFont(self.myFont)
            text_item.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
            text_item.setZValue(1000.0)
            text_item.lostFocus.connect(self.editorLostFocus)
            text_item.selectedChange.connect(self.itemSelected)
            self.addItem(text_item)
            text_item.setDefaultTextColor(self.myTextColor)
            text_item.setPos(mouse_event.scenePos())
            self.textInserted.emit(text_item)
        elif self.myMode == self.SelectItems:
            selection = True
            for item in self.items():
                if item.isUnderMouse():
                    if isinstance(item,GhostR):
                        selection = True
                    else:
                        selection = False
            if selection:
                init_point = mouse_event.scenePos()
                self.selectRect = QtGui.QGraphicsRectItem(
                    QtCore.QRectF(init_point, init_point))
                self.selectRect.setPen(
                    QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.DashLine))
                self.addItem(self.selectRect)
        super(SceneWidget, self).mousePressEvent(mouse_event)

        return

    def mouseMoveEvent(self, mouse_event):
        '''
            Este método define as acoes realizadas quando um evento do tipo
            mouseMove é detectado no diagrama grafico. Neste caso desenha uma
            linha quando o modo self.InsertLine está ativado
        '''
        if self.myMode == self.InsertLine and self.line:
            new_line = QtCore.QLineF(
                self.line.line().p1(), mouse_event.scenePos())
            self.line.setLine(new_line)
        elif self.myMode == self.MoveItem:
            super(SceneWidget, self).mouseMoveEvent(mouse_event)
        elif self.myMode == self.SelectItems and self.selectRect:
            new_rect = QtCore.QRectF(
                self.selectRect.rect().topLeft(), mouse_event.scenePos())
            self.selectRect.setRect(new_rect)

    def mouseReleaseEvent(self, mouse_event):
        '''
            Este método define as acoes realizadas quando um evento do tipo
            mouseRelease e detectado no diagrama grafico. Neste caso conecta
            os dois elementos que estão ligados pela linha criada no evento
            mousePress.
        '''
        if self.myMode == self.InsertLine and self.line:
            self.removeItem(self.no)
            inserted = False
            permit1 = True
            permit2 = True
            start_pop = None
            end_pop = None

            start_items = self.items(self.line.line().p1())
            print start_items

            if len(start_items) > 0 and (start_items[0] == self.line or isinstance(start_items[0], GhostR)):
                start_pop = start_items.pop(0)

            if len(start_items) > 1:
                for item in start_items:
                    if isinstance(item, GhostR):
                        start_pop = item
                        start_items.remove(item)
                for item in start_items:
                    if isinstance(item, Edge):
                        start_items.remove(item)
            print "start items"
            print start_items

            if len(start_items) == 0:
                if isinstance(start_pop, GhostR) and start_pop is not None:
                    c_pos = (start_pop.edge.line().p1() + start_pop.edge.line().p2()) / 2
                    start_item = Node(4, self.myLineMenu)
                    self.addItem(start_item)
                    start_item.setPos(c_pos)
                    self.start_item_is_ghost = True
                else:
                    print "checkpoint 1"
                    start_item = Node(4, self.myLineMenu)
                    self.addItem(start_item)
                    start_item.setPos(self.pressPos)

            if len(start_items):
                start_item = start_items[0]

            end_items = self.items(self.line.line().p2())
            print "end_len"
            print len(end_items)
            if len(end_items) and (end_items[0] == self.line or isinstance(end_items[0], GhostR)):
                end_pop = end_items.pop(0)

            for item in end_items:
                if isinstance(item, GhostR):
                    end_pop = item



            if len(end_items) == 0:
                end_item = Node(4, self.myLineMenu)
                self.addItem(end_item)
                end_item.setPos(mouse_event.scenePos())

            if len(end_items):
                if isinstance(end_pop, GhostR):
                    c_pos = (end_pop.edge.line().p1() + end_pop.edge.line().p2()) / 2
                    end_item = Node(4, self.myLineMenu)
                    self.addItem(end_item)
                    end_item.setPos(c_pos)
                    self.ghost = end_pop
                    self.end_item_is_ghost = True
                else:
                    end_item = end_items[0]

            if start_item == end_item or start_item.scenePos() == end_item.scenePos():
                self.removeItem(start_item)
                self.removeItem(self.line)
                self.line = None
                return


            self.removeItem(self.line)
            self.line = None

            if isinstance(start_item, Node) or isinstance(end_item, Node):
                if  not isinstance(start_item, Edge) and start_item.myItemType == Node.Barra and end_item.myItemType == Node.NoConectivo:
                    pos = end_item.scenePos()
                    self.removeItem(end_item)
                    end_item = Node(Node.Religador, self.myRecloserMenu)
                    self.addItem(end_item)
                    end_item.setPos(pos)
                if end_item.myItemType == Node.Barra and start_item.myItemType == Node.NoConectivo:
                    pos = start_item.scenePos()
                    self.removeItem(start_item)
                    start_item = Node(Node.Religador, self.myRecloserMenu)
                    self.addItem(start_item)
                    start_item.setPos(pos)
                print "start e end"
                print start_item.myItemType, end_item.myItemType
                print "lens e lene"
                start_item.update_count
                end_item.update_count
                print start_item.edge_counter, end_item.edge_counter
                if (start_item.edge_counter >= 2 and start_item.myItemType == Node.Religador):
                    permit1 = False
                    print "frase 1"
                if(end_item.edge_counter >= 2 and end_item.myItemType == Node.Religador):
                    permit1 = False
                    print "frase 2"
                if not permit1:
                    print "permit 1 negado!"
                    if isinstance(start_item, Node):
                        if start_item.myItemType == 4 and len(start_item.edges) == 0:
                            self.removeItem(start_item)
                            print "checkpoint 1"
                    if isinstance(end_item, Node):
                        if end_item.myItemType == 4 and len(end_item.edges) == 0:
                            self.removeItem(end_item)
                            print "checkpoint 2"

            print len(start_item.edges), len(end_item.edges)

            # Criação da edge definitiva
            if permit1:
                print "permitido"
                edge = Edge(start_item, end_item, self.myLineMenu)
                if edge.line().length() < 115:
                    if start_item.edge_counter > 1 or start_item.myItemType == Node.Barra:

                        pass
                    elif start_item.myItemType != Node.Religador:
                        print "remova!"
                        self.removeItem(start_item)
                    start_item.edge_counter -= 1
                    if end_item.edge_counter > 1 or end_item.myItemType == Node.Barra:
                        pass

                    elif end_item.myItemType != Node.Religador:
                        print "remova"
                        print "cp 1"
                        self.removeItem(end_item)
                    end_item.edge_counter -= 1
                    return
                else:
                    print "Edge:"
                    print edge
                    self.addItem(edge)
                    edge.set_color(QtCore.Qt.black)
                    self.addItem(edge.GhostRetItem)
                    edge.update_position()
                    print edge.w1, edge.w2
                    print "add ok!"
            else:
                return

            if edge.w1.myItemType == 4:
                aux = edge.w1
                edge.w1 = edge.w2
                edge.w2 = aux

            if self.start_item_is_ghost and not isinstance(start_item, GhostR):
                self.break_edge(start_item)


            # Teste: Se a linha criada for muito
            # pequena, o programa retorna sem nenhuma
            # edge criada. Se o tamanho for satisfatório,
            # o item edge é adicionado a cena.
            # if edge.line().length() < 60:
            #     self.removeItem(edge)
            #     self.removeItem(start_item)
            #     self.removeItem(end_item)
            #     self.removeItem(self.no)
            #     return
            # else:
            #     self.addItem(edge)

            # Se um dos itens conectados for um Node, a flag
            # inserted é setada

            # Realiza o update da posição da edge,
            # assim como seu elipse fantasma associado.
            # edge.update_position()
            # self.addItem(edge.GhostRetItem)
            # edge.update_ret()
            # self.update(0, 0, 800, 800)

            # Se a conexão for entre dois nós ou entre uma linha
            # e um nó, a linha é separada
            # if inserted is False and self.no is not None:
            #     self.break_edge()
            #     print "oi 1"
            #     new_node = Node(4, self.myLineMenu)
            #     self.addItem(new_node)
            #     new_node.setPos(mouse_event.scenePos())
            #     new_edge = Edge(self.no, new_node, self.myLineMenu)
            #     self.addItem(new_edge)
            #     new_edge.update_position()
            #     self.addItem(new_edge.GhostRetItem)
            #     new_edge.update_ret()
            #     self.update(0, 0, 800, 800)

            # if self.no is not None and inserted is True and self.ghost is not None:
            #     self.break_edge(edge.w1,edge.w2)
            #     print "opa"
            for item in self.selectedItems():
                item.setSelected(False)

            self.no = None

        elif self.myMode == self.SelectItems and self.selectRect:
            path = QtGui.QPainterPath()
            path.addRect(self.selectRect.rect())
            self.setSelectionArea(path)
            self.removeItem(self.selectRect)
            self.selectRect = None
        self.line = None
        self.itemInserted.emit(3)
        self.ghost = None
        super(SceneWidget, self).mouseReleaseEvent(mouse_event)

        #     Problema quando tenta-se modificar o texto dos componentes
        #     def keyPressEvent(self, event):
        #         key = event.key()
        #         if key == QtCore.Qt.Key_Up:
        #             for item in self.selectedItems():
        #                 item.moveBy(0, -5)
        #         elif key == QtCore.Qt.Key_Down:
        #             for item in self.selectedItems():
        #                 item.moveBy(0, 5)
        #         elif key == QtCore.Qt.Key_Left:
        #             for item in self.selectedItems():
        #                 item.moveBy(-5, 0)
        #         elif key == QtCore.Qt.Key_Right:
        #             for item in self.selectedItems():
        #                 item.moveBy(5, 0)
        #         elif key == QtCore.Qt.Key_Space or key == QtCore.Qt.Key_Enter:
        #             pass
        #         elif key == QtCore.Qt.Key_Control:
        #             self.keyControlIsPressed = True
        #             print 'Ctrl pressed'
        #         elif key == QtCore.Qt.Key_Delete:
        #             self.delete_item()
        #         else:
        #             pass
        #             #super(SceneWidget, self).keyPressEvent(self, event)
        #         return
    def break_edge(self, end_newline):
        print "break!"
        self.removeItem(self.ghost.edge.GhostRetItem)
        self.removeItem(self.ghost.edge)
        self.ghost.edge.w1.remove_edge(self.ghost.edge)
        self.ghost.edge.w2.remove_edge(self.ghost.edge)
        new_edge_1 = Edge(self.ghost.edge.w1, end_newline, self.myLineMenu)
        new_edge_2 = Edge(self.ghost.edge.w2, end_newline, self.myLineMenu)
        self.addItem(new_edge_1)
        self.addItem(new_edge_2)
        self.addItem(new_edge_1.GhostRetItem)
        self.addItem(new_edge_2.GhostRetItem)
        new_edge_1.update_position()
        new_edge_2.update_position()
        new_edge_1.update_ret()
        new_edge_2.update_ret()




    def set_item_type(self, type):
        '''
            Define em qual tipo de item sera inserido no diagrama grafico assim
            que um evento do tipo mousePress for detectado, podendo ser:
            Node.Subestacao
            Node.Religador
            Node.Barra
            Node.Agent
        '''
        self.myItemType = type

    def set_mode(self, mode):
        '''
            Define em qual modo
        '''
        self.myMode = mode

    def create_actions(self):
        '''
            Este metodo cria as ações que serão utilizadas nos menus dos itens
            gráficos.
        '''
        self.propertysAction = QtGui.QAction(
            'Propriedades', self, shortcut='Enter',
            triggered=self.launch_dialog)
        self.deleteAction = QtGui.QAction(
            'Excluir Item', self, shortcut='Delete',
            triggered=self.delete_item)
        self.increaseBusAction = QtGui.QAction(
            'Aumentar Barra', self, shortcut='Ctrl + a',
            triggered=self.increase_bus)
        self.decreaseBusAction = QtGui.QAction(
            'Diminuir Barra', self, shortcut='Ctrl + d',
            triggered=self.decrease_bus)
        self.alignHLineAction = QtGui.QAction(
            'Alinha Linha H', self, shortcut='Ctrl + h',
            triggered=self.align_line_h)
        self.alignVLineAction = QtGui.QAction(
            'Alinhar Linha V', self, shortcut='Ctrl + v',
            triggered=self.align_line_v)

    def create_menus(self):
        '''
            Este metodo cria os menus de cada um dos itens gráficos: religador,
            subestação, barra e linha.
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

    def delete_item(self):
        '''
            Este método implementa a ação de exclusão de um item gráfico do
            diagrama.
        '''
        for item in self.selectedItems():
            if isinstance(item, Node):
                item.remove_edges()
            if isinstance(item, Edge):
                item.w1.remove_edge(item)
                item.w2.remove_edge(item)
                if item.w1.myItemType == Node.NoConectivo:
                    item.w1.remove_edges()
                    self.removeItem(item.w1)
                if item.w2.myItemType == Node.NoConectivo:
                    
                    item.w2.remove_edges()
                    self.removeItem(item.w2)
                self.removeItem(item.GhostRetItem)
            self.removeItem(item)


    def launch_dialog(self):
        '''
            Este método inicia os diálogos de configuração de cada um dos itens
            gráficos do diagrama.
        '''
        dialog = RecloserDialog()

    def increase_bus(self, ):
        '''
            Este método implementa a açao de aumentar o tamanho do item gráfico
            barra.
        '''
        for item in self.selectedItems():
            if isinstance(item, Node):
                item.prepareGeometryChange()
                item.setRect(
                    item.rect().x(), item.rect().y(), item.rect().width(),
                    item.rect().height() * 1.25)

    def decrease_bus(self):
        '''
            Este método implementa a ação de aumentar o tamanho do item gráfico
            barra.
        '''
        for item in self.selectedItems():
            if isinstance(item, Node):
                item.prepareGeometryChange()
                item.setRect(
                    item.rect().x(), item.rect().y(), item.rect().width(),
                    item.rect().height() * 0.75)

    def align_line_h(self):
        for item in self.selectedItems():
            if isinstance(item, Edge):
                pos_y = item.w1.y()
                item.w2.setY(pos_y)
                item.update_position()
                item.update_ret()

    def align_line_v(self):
        for item in self.selectedItems():
            if isinstance(item, Edge):
                pos_x = item.w1.x()
                item.w2.setX(pos_x)
                item.update_position()
                item.update_ret()

    def h_align(self):
        y_pos_list = []
        # y_check_pos_list=[]
        # done = 0
        # dif = 0
        for item in self.selectedItems():
            if isinstance(item, Node):
                y_pos_list.append(item.pos().y())
        max_pos = max(y_pos_list)
        min_pos = min(y_pos_list)
        mean_pos = max_pos - abs(max_pos - min_pos) / 2.0

        for item in self.selectedItems():
            if isinstance(item, Node):
                if item.Fixed is True:
                    mean_pos = item.pos().y()

        for item in self.selectedItems():
            if isinstance(item, Node):
                item.setY(mean_pos)

        for item in self.selectedItems():
            if isinstance(item, Edge):
                item.update_position()

    def v_align(self):
        x_pos_list = []
        for item in self.selectedItems():
            if isinstance(item, Node):
                x_pos_list.append(item.pos().x())
        max_pos = max(x_pos_list)
        min_pos = min(x_pos_list)
        mean_pos = max_pos - abs(max_pos - min_pos) / 2.0

        for item in self.selectedItems():
            if isinstance(item, Node):
                item.setX(mean_pos)

        for item in self.selectedItems():
            if isinstance(item, Edge):
                item.update_position()

    def set_grid(self):
        if self.myBackgroundSytle == self.GridStyle:
            self.setBackgroundBrush(QtGui.QBrush(
                QtCore.Qt.white, QtCore.Qt.NoBrush))
            self.myBackgroundSytle = self.NoStyle
        elif self.myBackgroundSytle == self.NoStyle:
            self.setBackgroundBrush(QtGui.QBrush(
                QtCore.Qt.lightGray, QtCore.Qt.CrossPattern))
            self.myBackgroundSytle = self.GridStyle


class ViewWidget(QtGui.QGraphicsView):
    '''
        Esta classe implementa o container QGraphicsView
        onde residirá o objeto QGraphicsScene.
    '''
    def __init__(self, scene):

        super(ViewWidget, self).__init__(scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

    def wheelEvent(self, event):
        self.scale_view(math.pow(2.0, -event.delta() / 240.0))

    def scale_view(self, scale_factor):
        factor = self.matrix().scale(scale_factor, scale_factor).mapRect(
            QtCore.QRectF(0, 0, 1, 1)).width()
        if factor < 0.5 or factor > 3:
            return
        self.scale(scale_factor, scale_factor)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    scene = SceneWidget()
    widget = ViewWidget(scene)
    widget.show()
    sys.exit(app.exec_())
