# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Ellipse, Color
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout

WHITE = Color(1., 1., 1.)


class NodeWidget(Widget):
    def __init__(self, **kwargs):
        node = kwargs.pop('node')
        self.node = node

        super(self.__class__, self).__init__(**kwargs)

        self.size = (10, 10)
        color = Color(*node.color) if node.color else WHITE
        self.circle = Ellipse(pos=self.pos, size=self.size)

        self.canvas.add(color)
        self.canvas.add(self.circle)

    def on_pos(self, obj, new_pos):
        self.circle.pos = new_pos


class BoardWidget(FloatLayout):
    def __init__(self, size, nodes):
        super(self.__class__, self).__init__(size=size)

        self.widgets = {}
        for n in nodes:
            node_widget = NodeWidget(node=n)
            node_widget.pos = n.pos.to_tuple()
            self.widgets[n] = node_widget
            self.add_widget(node_widget)

    def update(self):
        for n, w in self.widgets.items():
            w.pos = n.pos.to_tuple()


class DashBoard(App):
    def __init__(self, space):
        super(self.__class__, self).__init__()

        self.space = space

    def update(self, _):
        self.space.step_forward()
        self.board.update()

    def build(self):

        self.board_size = self.space.size
        Clock.schedule_interval(self.update, .1)
        print 'map size: %s' % (self.board_size,)
        self.board = BoardWidget(self.board_size, self.space)

        return self.board
